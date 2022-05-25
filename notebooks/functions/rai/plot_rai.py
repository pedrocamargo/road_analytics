import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

from functions.load_zones import load_zones


def plot_rai(rai_data, project, division_type='zone'):
    fig, ax = plt.subplots(constrained_layout=False, frameon=False, figsize=(20,20))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    
    
    if division_type=='zone' :
        print('Obtaining model zones')
        gdf = load_zones(project)[['zone_id', 'geometry']]
        data = rai_data.groupby('zone_id').sum()[['accessible', 'inaccessible']].reset_index()
        data = data.assign(rai=data.accessible/(data.accessible+data.inaccessible))
        gdf = gdf.merge(data, on='zone_id')
    
    elif division_type=='subdivision' :
        print('Obtaining country subdivisions')
        sql = "SELECT division_name, level, Hex(ST_AsBinary(GEOMETRY)) as geom FROM country_subdivisions;"
        subdivisions = gpd.GeoDataFrame.from_postgis(sql, project.conn, geom_col="geom", crs=4326)
        gdf = subdivisions[subdivisions.level == subdivisions.level.max()]
        data = rai_data.groupby('division_name').sum()[['accessible', 'inaccessible']].reset_index()
        data = data.assign(rai=data.accessible/(data.accessible+data.inaccessible))
        gdf = gdf.merge(data, on='division_name')
    else:
        raise ValueError('Unknown division_type')
    
    gdf.plot('rai', ax=ax, legend=True, cmap='Greens', linewidth=0.1)

