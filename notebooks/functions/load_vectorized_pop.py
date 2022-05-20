import geopandas as gpd
import sqlite3
from os.path import join

def load_vectorized_pop(folder):
    
    popsqlite = sqlite3.connect(join(folder, f'pop.sqlite'))
    popsqlite.enable_load_extension(True)
    popsqlite.load_extension('mod_spatialite')

    sql = "SELECT population, Hex(ST_AsBinary(GEOMETRY)) as geom FROM raw_population;"
    pop_data = gpd.GeoDataFrame.from_postgis(sql, popsqlite, geom_col="geom")
    pop_data.set_crs('epsg:4326', inplace=True)
    
    return pop_data