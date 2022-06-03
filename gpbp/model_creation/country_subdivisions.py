import geopandas as gpd
import pandas as pd
import urllib.request
from os.path import join, isfile
from tempfile import gettempdir


def get_subdivisions(country_name:str):
    
    url = 'https://github.com/pedrocamargo/road_analytics/releases/download/v0.1/subdivisions.gpkg'

    dest_path = join(gettempdir(), "subdivisions.gpkg")
    if not isfile(dest_path):
        urllib.request.urlretrieve(url, dest_path)
    level1 = gpd.read_file(dest_path, layer='level_1')
    level1 = level1[level1.country==country_name].assign(level=1)
    level2 = gpd.read_file(dest_path, layer='level_2')
    level2 = level2[level2.country==country_name].assign(level=2)

    return pd.concat([level1, level2])