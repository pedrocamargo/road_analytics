from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
from aequilibrae import Project
from gpbp.data.load_zones import load_zones
from gpbp.data_retrieval.osm_tags.osm_amenities import amenities
from gpbp.data_retrieval.osm_tags.osm_tag_values import amenity_values

def import_osm_amenities(model_place:str, project:Project, osm_data:dict):

    df = pd.DataFrame.from_dict(amenities(osm_data, model_place))  # MUDA

    df['geom'] = df.apply(lambda x: Point(x.lon, x.lat), axis=1)

    tags = df['tags'].apply(pd.Series)[['amenity']]

    tags['update_amenity'] = tags['amenity'].apply(lambda x: amenity_values.get(x))

    tags['update_amenity'].fillna(value='others', inplace=True)

    tags.drop(columns=['amenity'], inplace=True)

    tags.rename(columns={'update_amenity': 'amenity'}, inplace=True)

    merged_df = df.merge(tags, left_index=True, right_index=True)[['type', 'id', 'geom', 'amenity']]

    zones = load_zones(project)

    gdf = gpd.GeoDataFrame(merged_df, geometry='geom', crs=4326)

    tag_by_zone = gpd.sjoin(gdf, zones)

    tag_by_zone.drop(columns='index_right', inplace=True)

    return tag_by_zone
