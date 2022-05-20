import pandas as pd
import geopandas as gpd
import numpy as np
import sqlite3
import shapely.wkb

def open_states(project):
    
    
    sql = "SELECT division_name, level, Hex(ST_AsBinary(GEOMETRY)) as geom FROM country_subdivisions;"
    return gpd.GeoDataFrame.from_postgis(sql, project.conn, geom_col="geom", crs=4326)
