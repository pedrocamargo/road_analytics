from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
from aequilibrae import Project
from gpbp.data.load_zones import load_zones
from gpbp.data_retrieval.osm_tags.osm_amenities import amenities
from gpbp.data_retrieval.osm_tags.osm_tag_values import amenity_values

def import_osm_amenities(tag:str, project:Project):

    df = pd.DataFrame.from_dict(amenities()) #aqui não vai dar certo.

    df['geom'] = df.apply(lambda x: Point(x.lon, x.lat), axis=1)

    df = df[['type', 'id', 'geom', tag]]

    tags = df['tags'].apply(pd.Series)[[tag]]

    tags[f'update_{tag}'] = tags[tag].apply(lambda x: amenity_values.get(x))

    tags[f'update_{tag}'].fillna(value='others', inplace=True)

    tags.drop(columns=[tag], inplace=True)

    tags.rename(columns={f'update_{tag}': tag}, inplace=True)

    merged_df = df.merge(tags, left_index=True, right_index=True)

    zones = load_zones(project)

    gdf = gpd.GeoDataFrame(merged_df, geometry='geom', crs=4326)

    tag_by_zone = gpd.sjoin(gdf, zones)

    tag_by_zone.drop(columns='index_right', inplace=True)

    return tag_by_zone