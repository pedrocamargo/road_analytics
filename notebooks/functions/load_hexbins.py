import shapely.wkb
from aequilibrae import Project
import pandas as pd
import sqlite3
import geopandas as gpd

def load_hexbins(project):
    
    hexbins_file = [x for x in project.conn.execute('SELECT hex_bins, state, x, y, asBinary(geometry), population\
                                                     FROM hex_pop;')]
    hexbins = pd.DataFrame(hexbins_file, columns=['hex_id', 'state', 'x', 'y', 'geometry', 'population'])
    hexbins['geometry'] = hexbins['geometry'].apply(lambda x:shapely.wkb.loads(x))
    hexbins = gpd.GeoDataFrame(hexbins, geometry='geometry')
    
    return hexbins