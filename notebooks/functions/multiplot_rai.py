import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from functions.load_zones import load_zones

def multiplot_rai(pop_1, pop_2, project, division_type='zone'):
    
    fig, ax = plt.subplots(1, 2, constrained_layout=False, frameon=False, figsize=(20,20))
    ax[0].get_xaxis().set_visible(False)
    ax[0].get_yaxis().set_visible(False)
    ax[1].get_xaxis().set_visible(False)
    ax[1].get_yaxis().set_visible(False)
    
    if division_type=='zone' :
        print('Obtaining model zones')
        gdf = load_zones(project)[['zone_id', 'geometry']]
        left_data = pop_1.groupby('zone_id').sum()[['accessible', 'inaccessible']].reset_index()
        left_data = left_data.assign(rai=left_data.accessible/(left_data.accessible+left_data.inaccessible))
        left_gdf = gdf.merge(left_data, on='zone_id')
        right_data = pop_2.groupby('zone_id').sum()[['accessible', 'inaccessible']].reset_index()
        right_data = right_data.assign(rai=right_data.accessible/(right_data.accessible+right_data.inaccessible))
        right_gdf = gdf.merge(right_data, on='zone_id')
    
    elif division_type=='subdivision' :
        print('Obtaining country subdivisions')
        sql = "SELECT division_name, level, Hex(ST_AsBinary(GEOMETRY)) as geom FROM country_subdivisions;"
        subdivisions = gpd.GeoDataFrame.from_postgis(sql, project.conn, geom_col="geom", crs=4326)
        gdf = subdivisions[subdivisions.level == subdivisions.level.max()]
        left_data = pop_1.groupby('division_name').sum()[['accessible', 'inaccessible']].reset_index()
        left_data = left_data.assign(rai=left_data.accessible/(left_data.accessible+left_data.inaccessible))
        left_gdf = gdf.merge(left_data, on='division_name')
        right_data = pop_2.groupby('division_name').sum()[['accessible', 'inaccessible']].reset_index()
        right_data = right_data.assign(rai=right_data.accessible/(right_data.accessible+right_data.inaccessible))
        right_gdf = gdf.merge(right_data, on='division_name')
        
    else:
        raise ValueError('Unknown division_type')
    
    left_divider = make_axes_locatable(ax[0])
    left_cax = left_divider.append_axes("right", size="5%", pad=0.1)
    left_gdf.plot('rai', ax=ax[0], legend=True, cmap='Greens', linewidth=0.1, cax=left_cax)

    right_divider = make_axes_locatable(ax[1])
    right_cax = right_divider.append_axes("right", size="5%", pad=0.1)   
    right_gdf.plot('rai', ax=ax[1], legend=True, cmap='Greens', linewidth=0.1, cax=right_cax)