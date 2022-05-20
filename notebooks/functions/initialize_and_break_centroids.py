import pandas as pd
import geopandas as gpd
from math import sqrt, ceil
from sklearn.cluster import KMeans
import warnings
import sqlite3
import numpy as np

def initialize_and_break(hexbins, max_zone_size):
    
    hexbins['zone_id'] = -1
    list_state = list(hexbins.state.unique())
    data_store = []
    master_zone_id = 1
    for i, state in enumerate(list_state):
        df = hexbins[hexbins.state==state].copy()
        df.loc[:, 'zone_id'] = master_zone_id + i
        data_store.append(df[['hex_id', 'x', 'y', 'population', 'state', 'zone_id']])
    
    for cnt, df in enumerate(data_store):
        t = df.groupby(['zone_id']).sum()
        t = t.loc[t.population>max_zone_size]
        zone_sizes = t['population'].to_dict()
        zones_to_break = len(zone_sizes)
        counter = 0
        threshold = 500
        thrsh = 500
        #if cnt % 25 == 0:
            #print(f'Done {cnt}/{len(data_store)} states')
        while zones_to_break > 0:
            counter += 1
            zone_to_analyze = min(zone_sizes)
            zone_pop = zone_sizes.pop(zone_to_analyze)
            zones_to_break -= 1
            if zone_pop < max_zone_size:
                continue
            fltr = df.zone_id==zone_to_analyze
            segments = max(2, ceil(sqrt(zone_pop/max_zone_size)))
            prov_pop = df.loc[fltr, :]
            segments = min( prov_pop.shape[0], segments)
            if prov_pop.shape[0] < 2:
                continue

            kmeans = KMeans(n_clusters=segments, random_state=0)
            centr_results = kmeans.fit_predict(X=prov_pop[['x', 'y']].values, sample_weight=prov_pop.population.values)
            df.loc[fltr, 'zone_id'] = centr_results[:] + master_zone_id

            t = df.groupby(['zone_id']).sum()
            ready= t.loc[t.population<=max_zone_size].shape[0]
            avg = int(np.nansum(t.loc[t.population<=max_zone_size, 'population'])/max(1, ready))
            t = t.loc[t.population>max_zone_size]
            zone_sizes = t['population'].to_dict()
            zones_to_break = len(zone_sizes)
            master_zone_id += segments + 1
            #if counter % 50 == 0:
                #print(f'Queue for analysis: {zones_to_break} (Done: {ready} ({avg} people/zone))')
    
    df = pd.concat(data_store)[['hex_id', 'zone_id']]
    df = pd.merge(hexbins[['hex_id', 'x', 'y', 'population', 'state', 'geometry']], df, on='hex_id')
    df = gpd.GeoDataFrame(df[['hex_id', 'x', 'y', 'population', 'state', 'zone_id']], 
                          geometry=df['geometry'])

    zoning=df.dissolve(by='zone_id')[['state', 'geometry']]
    pop_total = df[['zone_id', 'population']].groupby(['zone_id']).sum()['population']
    zoning = zoning.join(pop_total)
    
    return df, zoning, master_zone_id