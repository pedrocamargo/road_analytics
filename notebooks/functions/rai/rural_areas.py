import geopandas as gpd
import pandas as pd
import urllib.request
from os.path import join, isfile
from tempfile import gettempdir
import shapely.wkb


def select_rural_areas(project):
    
    url = r'https://github.com/pedrocamargo/road_analytics/releases/download/v0.1/global_urban_extent.gpkg'
    
    dest_path = join(gettempdir(), "global_urban_extent.gpkg")
    
    if not isfile(dest_path):
        urllib.request.urlretrieve(url, dest_path)
    
    
    country_wkb = project.conn.execute('Select asBinary(geometry) from country_borders').fetchone()[0]
    country_borders = shapely.wkb.loads(country_wkb)
        
    gdf = gpd.GeoDataFrame(pd.DataFrame(country_borders, columns=['geometry']), geometry='geometry', crs=4326)
    
    urban_areas = gpd.read_file(url, mask=country_borders)
    
    rural_areas = gdf.overlay(urban_areas, how='symmetric_difference')
    
    return rural_areas