import geopandas as gpd
import sqlite3
from os.path import join
from geopandas.tools import sjoin

def zones_with_population(folder, zones_from_locations):
    
    popsqlite = sqlite3.connect(join(folder, f'pop.sqlite')) 
    popsqlite.enable_load_extension(True)
    popsqlite.load_extension('mod_spatialite')

    sql = "SELECT population, Hex(ST_AsBinary(GEOMETRY)) as geom FROM raw_population;"
    pop_data = gpd.GeoDataFrame.from_postgis(sql, popsqlite, geom_col="geom")
    pop_data.set_crs('epsg:4326', inplace=True)
    
    pop_to_zone = sjoin(pop_data, zones_from_locations, how="left", predicate="within")
    
    pop_per_zone = pop_to_zone.groupby(['hex_id']).sum()[['population']].reset_index()
    pop_per_zone.loc[:, 'hex_id'] = pop_per_zone.hex_id.astype(int)
    pop_per_zone.sort_values(['hex_id'], inplace=True)

    zones_with_pop = zones_from_locations.merge(pop_per_zone, on='hex_id', how='left')
    zones_with_pop.population.fillna(0, inplace=True)

    zones_with_pop = zones_with_pop.drop_duplicates(subset=['geometry'])

    return zones_with_pop