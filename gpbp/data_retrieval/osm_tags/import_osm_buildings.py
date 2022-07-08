from shapely.geometry import Point, Polygon
import pandas as pd
import geopandas as gpd
from aequilibrae import Project
from gpbp.data.load_zones import load_zones
from gpbp.data_retrieval.osm_tags.osm_buildings import buildings
from gpbp.data_retrieval.osm_tags.osm_tag_values import building_values

def import_osm_buildings(model_place:str, project:Project, osm_data:dict, zones:gpd.GeoDataFrame):

    df = pd.DataFrame.from_dict(buildings(osm_data, model_place))

    df['geom'] = df.apply(point_or_polygon, axis=1)  #AQUI

    tags = df['tags'].apply(pd.Series)[['building']] 

    tags[f'update_building'] = tags['building'].apply(lambda x: building_values.get(x))

    tags[f'update_building'].fillna(value='others', inplace=True)

    tags.drop(columns=['building'], inplace=True)

    tags.rename(columns={f'update_building': 'building'}, inplace=True)

    merged_df = df.merge(tags, left_index=True, right_index=True)[['type', 'id', 'geom', 'building']]

    gdf = gpd.GeoDataFrame(merged_df, geometry='geom', crs=4326)

    tag_by_zone = gpd.sjoin(gdf, zones)

    tag_by_zone.drop(columns='index_right', inplace=True)

    tag_by_zone['area'] = tag_by_zone.geom.to_crs(3857).area #AQUI

    return tag_by_zone


def point_or_polygon(row): #NÃO TEM ESSA FUNC. DO OUTRO LADO

    if row.type == 'node':

        return Point(row.lon, row.lat)

    else:

        poly = []
        for dct in row.geometry:
            poly.append((dct['lon'], dct['lat']))

        return Polygon(poly)
