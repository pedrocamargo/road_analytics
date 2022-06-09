from re import sub
import geopandas as gpd
import pandas as pd
import urllib.request
from os.path import join, isfile
from tempfile import gettempdir


def get_subdivisions(country_name:str, subdivisions:int):
    
    url = 'https://github.com/pedrocamargo/road_analytics/releases/download/v0.1/subdivisions.gpkg'

    dest_path = join(gettempdir(), "subdivisions.gpkg")
    if not isfile(dest_path):
        urllib.request.urlretrieve(url, dest_path)
    
    for i in range(1, subdivisions+1):
        globals()[f'level{i}'] = gpd.read_file(dest_path, layer=f'level_{i}')
        globals()[f'level{i}'] = globals()[f'level{i}'][globals()[f'level{i}'].country==country_name].assign(level=i)

    return pd.concat([globals()[f'level{i}'] for i in range(1, subdivisions+1)])
