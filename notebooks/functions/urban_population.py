import pandas as pd
import geopandas as gpd

from functions.load_hexbins import load_hexbins
from functions.urban_areas import select_urban_areas

def urban_population(country_name:str, project):
    
    hexbins = load_hexbins(project)[['hex_id', 'country_subdivision', 'geometry', 'population']].\
              set_crs(epsg=3857, allow_override=True)
    
    urban_areas = select_urban_areas(country_name)
    
    urban_pop = hexbins.overlay(urban_areas, how='intersection')
    
    urban_hex = urban_pop.hex_id.values.tolist()
    
    hexbins['is_urban'] = 0
    
    hexbins.loc[hexbins.hex_id.isin(urban_hex), 'is_urban'] = 1
    
    return hexbins