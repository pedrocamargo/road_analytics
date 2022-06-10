import io
import urllib.request
from os.path import join, isfile
from tempfile import gettempdir
import zipfile
import numpy as np
import pandas as pd
import rasterio
from sqlalchemy import over
from aequilibrae.project import Project
import requests
from scipy.sparse import coo_matrix

from gpbp.data.population_file_address import population_source
from notebooks.functions.country_main_area import get_main_area


def pop_to_model(project: Project, model_place: str, source='WorldPop', overwrite=True):
    """
        Function to process raster images in Python
    """
    
    url = population_source(model_place, source)

    if source == 'WorldPop':    
        dest_path = join(gettempdir(), f"pop_{model_place}.tif")
        if not isfile(dest_path):
            urllib.request.urlretrieve(url, dest_path)
        dataset = rasterio.open(dest_path)
    elif source == 'Meta':
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        filename = z.namelist()[0]
        var = z.extract(filename)
        dataset = rasterio.open(var)
    else:
        print('Non-existing source.')

    main_area = get_main_area(project)
    
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
        y = row * (-y_size) + y_max + (y_size / 2)  # to centre the point
        y_idx.append(y)
    y_idx = np.array(y_idx)

    x_idx = []
    for col in range(width):
        x = col * x_size + x_min + (x_size / 2)  # add half the cell size
        x_idx.append(x)
    x_idx = np.array(x_idx)

    # Read the data and build the population dataset
    data = dataset.read(1)
    mat = coo_matrix(data)
    rows = y_idx[mat.row]
    cols = x_idx[mat.col]
    df = pd.DataFrame({'longitude': cols, 'latitude': rows, 'population': mat.data})
    df = df.loc[df.population >= 0, :]  # Pixels outside the modeled area have negative values
    df = df[(df.longitude > minx) & (df.longitude < maxx) & (df.latitude > miny) & (df.latitude < maxy)]
    df.fillna(0, inplace=True)

    if overwrite == False or source == 'Meta':
        overwrite_population(project, df)
    else:
        pass

def overwrite_population(project, df):
    project.conn.execute('Drop table if exists raw_population')
    project.conn.commit()  
    conn = project.conn
    df.to_sql('raw_population', conn, if_exists='replace', index=False)
    conn.execute("select AddGeometryColumn( 'raw_population', 'geometry', 4326, 'POINT', 'XY', 1);")
    conn.execute("UPDATE raw_population SET Geometry=MakePoint(longitude, latitude, 4326)")
    conn.execute("SELECT CreateSpatialIndex( 'raw_population' , 'geometry' );")
    conn.commit()
