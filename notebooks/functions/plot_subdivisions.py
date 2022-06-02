import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx

from functions.country_subdivisions import get_subdivisions

def plot_subdivisions(country_name:str, level=1):
    
    subdivisions = get_subdivisions(country_name)
    
    gdf = gpd.GeoDataFrame(subdivisions, geometry='geometry', crs=4326)
    
    if (gdf.level.max() == 1 or gdf.level.max() == 2) and level == 1: #aqui
        ax = gdf[gdf.level==1].plot(figsize=(20, 20), alpha=0.5, edgecolor='k', cmap='tab20b')
        cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik, crs=4326)

    elif gdf.level.max() == 2 and level == 2:
        ax = gdf[gdf.level==2].plot(figsize=(20, 20), alpha=0.5, edgecolor='k', cmap='tab20')
        cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik, crs=4326)
    
    else:
        raise ValueError('Unavailable level.')