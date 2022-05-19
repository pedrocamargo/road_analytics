import pandas as pd
import numpy as np
import geopandas as gpd
from math import sqrt, ceil
from sklearn.cluster import KMeans
import libpysal
import warnings
import sqlite3

def progressive_break(df, zoning, min_zone_size, master_zone_id):
    
    while zoning[zoning.geometry.type=='MultiPolygon'].shape[0] > 0:
        for zid, record in zoning[zoning.geometry.type=='MultiPolygon'].iterrows():
            zone_df = df[df.zone_id==zid]
            with warnings.catch_warnings():
                adj_mtx = libpysal.weights.Queen.from_dataframe(zone_df)
            islands =  np.unique(adj_mtx.component_labels)
            island_pop = {isl:zone_df[adj_mtx.component_labels==isl].population.sum() for isl in islands}
            max_island = max(island_pop.values())
            remove_islands = [k for k, v in island_pop.items() if v < max_island]
            for rmv in remove_islands:
                island_hexbins = zone_df[adj_mtx.component_labels == rmv].hex_id
                if zone_df[df.hex_id.isin(island_hexbins)].population.sum() > min_zone_size:
                    df.loc[df.hex_id.isin(island_hexbins),'zone_id'] = master_zone_id
                    master_zone_id += 1
                    continue

                closeby = []
                for island_geo in zone_df[adj_mtx.component_labels == rmv].geometry:
                    closeby.extend([x for x in df.sindex.nearest(island_geo.bounds, 6)])
                closeby = list(set(closeby))
                if not closeby:
                    continue
                adjacent = df.loc[df.index.isin(closeby),:]
                available = [x for x in adjacent.zone_id.unique() if x != zid]

                same_area = [av for av in available if adjacent.loc[adjacent.zone_id==av, 'state'].values[0] == record.state]
                if same_area:
                    df.loc[df.hex_id.isin(island_hexbins),'zone_id'] = same_area[0]
                else:
                    counts = adjacent.groupby(['zone_id']).count()
                    counts = list(counts[counts.hex_id==counts.hex_id.max()].index)
                    counts = [x for x in counts if x != zid][0]
                    df.loc[df.hex_id.isin(island_hexbins), 'state'] = adjacent.loc[adjacent.zone_id==counts, 'state'].values[0]
                    df.loc[df.hex_id.isin(island_hexbins),'zone_id'] = counts

    new_zoning=df.dissolve(by='zone_id')[['state', 'geometry']]
    pop_total = df[['zone_id', 'population']].groupby(['zone_id']).sum()['population']
    new_zoning = new_zoning.join(pop_total)
    
    new_zoning['final_zone_id'] = np.arange(new_zoning.shape[0]) + 1
    
    return new_zoning