import pandas as pd
import geopandas as gpd

# from functions.load_hexbins import load_hexbins
from functions.load_zones import load_zones
from functions.urban_population import urban_population
from geopandas import sjoin_nearest

from .population_data import population_data


def basic_RAI_data(project, country_name):
    pop_data = population_data(country_name, project).to_crs(3857)

    links = project.network.links.data
    links = links[links.modes.str.contains('c')]
    links = gpd.GeoDataFrame(links, geometry='geometry', crs=4326).to_crs(3857)

    df = sjoin_nearest(pop_data, links, distance_col='distance_to_link')

    df['accessible'] = df.population
    df.loc[df.distance_to_link > 2000, 'accessible'] = 0
    df['inaccessible'] = df.population
    df.loc[df.distance_to_link <= 2000, 'inaccessible'] = 0

    # Add subdivision info
    sql = "SELECT division_name, level, Hex(ST_AsBinary(GEOMETRY)) as geom FROM country_subdivisions;"
    subdivisions = gpd.GeoDataFrame.from_postgis(sql, project.conn, geom_col="geom", crs=4326)
    subdivisions = subdivisions[subdivisions.level == subdivisions.level.max()]

    df = gpd.sjoin(df, subdivisions)

    # Add zone data
    zones = load_zones(project)[['zone_id', 'geometry']]
    return gpd.sjoin(df, zones)
