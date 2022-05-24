import pandas as pd
import geopandas as gpd

#from functions.load_hexbins import load_hexbins
from functions.load_zones import load_zones
from functions.urban_population import urban_population

def rural_population(country_name, project, rural_links):
    
    urban_pop = urban_population(country_name, project)
    
    zones = load_zones(project)[['zone_id', 'geometry']]
    
    buffer_links = rural_links.buffer(0.02)

    geo_buffer = gpd.GeoDataFrame(pd.DataFrame(buffer_links, columns=['geometry']), 
                                  geometry='geometry', crs='epsg:3857')

    geo_buffer['ogc_fid'] = rural_links.ogc_fid.values.tolist()
    
    rural_hexbins = gpd.sjoin(urban_pop, geo_buffer, how='left').set_crs(epsg=3857, allow_override=True)
    
    rural_hexbins = rural_hexbins.drop(columns=['index_right']).drop_duplicates(subset='hex_id')
    
    hex_buffer_and_zones = gpd.sjoin(rural_hexbins, zones, how='left')
    
    return hex_buffer_and_zones