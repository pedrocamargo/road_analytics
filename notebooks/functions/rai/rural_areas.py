import geopandas as gpd
import pandas as pd
import urllib.request
from os.path import join, isfile
from tempfile import gettempdir

from functions.country_borders import get_country_borders

def select_rural_areas(country_name:str):
    
    url = r'https://github.com/pedrocamargo/road_analytics/releases/download/v0.1/global_urban_extent.gpkg'
    
    dest_path = join(gettempdir(), "global_urban_extent.gpkg")
    
    if not isfile(dest_path):
        urllib.request.urlretrieve(url, dest_path)
    
    country_borders = get_country_borders(country_name)
    
    gdf = gpd.GeoDataFrame(pd.DataFrame(country_borders, columns=['geometry']), 
                           geometry='geometry')
    
    urban_areas = gpd.read_file(url, mask=country_borders)
    
    rural_areas = gdf.overlay(urban_areas, how='symmetric_difference')
    
    return rural_areas