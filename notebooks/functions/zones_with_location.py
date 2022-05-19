import pandas as pd
import geopandas as gpd
from geopandas.tools import sjoin

def zones_with_location(hexb, states):
    
    centroids = gpd.GeoDataFrame(hexb[['hex_id']], geometry=gpd.points_from_xy( hexb['x'], hexb['y']), crs="EPSG:3405")
    centroids.to_crs(4326, inplace=True)
    
    data = sjoin(centroids, states, how="left", predicate="intersects") #relace district by state
    data.drop_duplicates(subset=['hex_id'], inplace=True) 
    data = data[['hex_id','state', 'geometry']] #remove district
    found_centroid = data[['hex_id', 'state']] #remove district
    found_centroid = found_centroid.dropna()
    
    not_found = hexb[~hexb.hex_id.isin(found_centroid.hex_id)]
    not_found_merged = sjoin(not_found, states, how="left", predicate="intersects")  #relace district by state
    not_found_merged = not_found_merged[['hex_id','state_left']] #replace district
    not_found_merged.dropna(inplace=True)
    not_found_merged = not_found_merged.rename(columns={'state_left':'state'})
    
    with_data = pd.concat([not_found_merged, found_centroid])
    
    data_complete = hexb.merge(with_data, on='hex_id', how='outer')
    
    dindex = states.sindex
    empties = data_complete.state_x.isna()
    for idx, record in data_complete[empties].iterrows():
        i -= 1
        geo = record.geometry
        dscrt = [x for x in dindex.nearest(geo.bounds, 10)]
        dist = [states.loc[d, 'geometry'].distance(geo) for d in dscrt]
        m = dscrt[dist.index(min(dist))]
        data_complete.loc[idx, 'state'] = states.loc[m, 'state']
        
    zones_with_location = gpd.GeoDataFrame(data_complete[['hex_id', 'state_x', 'x', 'y']], 
                                           geometry=data_complete['geometry']).rename(columns={'state_x':'state'})

    
    return zones_with_location