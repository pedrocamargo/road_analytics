import pandas as pd
import geopandas as gpd
import rasterio
import sqlite3
from os.path import join, isfile
import urllib.request
from tempfile import gettempdir
import numpy as np
from scipy.sparse import coo_matrix

from gpbp.data_retrieval.country_main_area import get_main_area

def population_raster(data_link, field_name, project):
    
    url = data_link

    dest_path = join(gettempdir(), f"pop_{field_name}.tif")
    if not isfile(dest_path):
        urllib.request.urlretrieve(url, dest_path)

    main_area = get_main_area(project)

    dataset = rasterio.open(dest_path)

    minx, miny, maxx, maxy = main_area.bounds
    width = dataset.width
    height = dataset.height
    x_min = dataset.bounds.left
    x_max = dataset.bounds.right
    y_min = dataset.bounds.bottom
    y_max = dataset.bounds.top
    dx = x_max - x_min
    dy = y_max - y_min
    x_size, y_size = dataset.res

    # Computes the  X and Y indices for the XY grid that will represent our raster
    y_idx = []
    for row in range(height):
        y = row * (-y_size) + y_max + (y_size / 2)  #to centre the point
        y_idx.append(y)
    y_idx = np.array(y_idx)

    x_idx = []
    for col in range(width):
        x = col * x_size + x_min + (x_size / 2)  #add half the cell size
        x_idx.append(x)
    x_idx = np.array(x_idx)

    # Read the data and build the population dataset
    data = dataset.read(1)
    mat = coo_matrix(data)
    rows = y_idx[mat.row]
    cols = x_idx[mat.col]
    df = pd.DataFrame({'longitude': cols, 'latitude': rows, 'population': mat.data})
    df = df.loc[df.population >= 0, :]  # Pixels outside the modeled area have negative values
    df = df[(df.longitude > minx) & (df.longitude < maxx) & (df.latitude > miny) &\
                (df.latitude < maxy)]
    df.fillna(0, inplace=True)
    
    gdf_pop = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs=4326)
    
    return gdf_pop