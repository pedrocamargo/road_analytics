import geopandas as gpd
import pandas as pd
import shapely.wkb
import numpy as np
import sqlite3
from aequilibrae import Project

def country_borders(project):
    mainland_wkb = [x[0] for x in project.conn.execute('Select asBinary(ST_Subdivide(geometry, 2048)) from country_borders')]
    mainland_geo = shapely.wkb.loads(mainland_wkb[0])
    
    try:           
        mainland = gpd.GeoDataFrame(pd.DataFrame({'ids':np.arange(len(mainland_geo)), 'geometry':mainland_geo}))
        mainland.set_crs('epsg:4326', inplace=True)
        mainland.shape[0]
    except TypeError:
        mainland = gpd.GeoDataFrame(pd.DataFrame({'ids':[1], 'geometry':mainland_geo}))
        mainland.set_crs('epsg:4326', inplace=True)
        mainland.shape[0]
            
    return mainland