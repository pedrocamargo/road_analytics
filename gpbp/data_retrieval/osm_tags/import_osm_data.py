from shapely.geometry import Point, Polygon
import pandas as pd
import geopandas as gpd
from aequilibrae import Project
from gpbp.data.load_zones import load_zones
from gpbp.data_retrieval.osm_tags.osm_buildings import buildings
from gpbp.data_retrieval.osm_tags.osm_amenities import amenities
from gpbp.data_retrieval.osm_tags.osm_tag_values import building_values, amenity_values


def import_osm_data(tag:str, model_place:str, osm_data:dict, project:Project):
    
    if tag == 'building':
        df = pd.DataFrame.from_dict(buildings(osm_data, model_place))
        df['geometry'] = df.apply(point_or_polygon, axis=1)  # AQUI
        tag_value = building_values
    elif tag == 'amenity':
        df = pd.DataFrame.from_dict(amenities(osm_data, model_place))
        df['geometry'] = df.apply(lambda x: Point(x.lon, x.lat), axis=1)
        tag_value = amenity_values
    else:
        raise ValueError (f'No data with {tag} tag was imported.')

    tags = df['tags'].apply(pd.Series)[[tag]]

    tags[f'update_{tag}'] = tags[tag].apply(lambda x: tag_value.get(x))

    tags[f'update_{tag}'].fillna(value='others', inplace=True)

    tags.drop(columns=[tag], inplace=True)

    tags.rename(columns={f'update_{tag}': tag}, inplace=True)

    merged_df = df.merge(tags, left_index=True, right_index=True)[['type', 'id', 'geometry', tag]]

    gdf = gpd.GeoDataFrame(merged_df, geometry='geometry', crs=4326)

    gdf['geom'] = gdf.geometry.to_wkb()

    zones = load_zones(project)

    tag_by_zone = gpd.sjoin(gdf, zones)

    tag_by_zone.drop(columns='index_right', inplace=True)

    if tag == 'building':
        tag_by_zone['area'] = tag_by_zone.geom.to_crs(3857).area
        table_name = 'osm_buildings'
        geom_type = 'MULTIPOLYGON'
        #list_of_tuples = [(x, y, z, a, b, c) for x, y, z, a, b, c in zip(df.type, df.id, df.building, df.zone_id, df.area, df.geom.wkb)]
        list_of_tuples = list(tag_by_zone[['type', 'id', 'building', 'zone_id', 'area', 'geom']].fillna(0).itertuples(index=False, name=None))
        qry = f"INSERT into osm_buildings(type, id, building, zone_id, area, geometry) VALUES(?, ?, ?, ?, ?, CastToMulti(GeomFromWKB(?, 4326)));"
        print('Saving OSM buildings.')
    else:
        table_name = 'osm_amenities'
        geom_type = 'POINT'
        qry = f"INSERT into osm_amenities(type, id, amenity, zone_id, geometry) VALUES(?, ?, ?, ?, CastToPoint(GeomFromWKB(?, 4326)));"
        #list_of_tuples = [(x, y, z, a, b) for x, y, z, a, b in zip(df.type, df.id, df.amenity, df.zone_id, df.geom.wkb)]
        list_of_tuples = list(tag_by_zone[['type', 'id', 'amenity', 'zone_id', 'geom']].fillna(0).itertuples(index=False, name=None))
        print('Saving OSM amenities.')

    project.conn.execute(f'CREATE TABLE IF NOT EXISTS {table_name}("type" TEXT, "id" INTEGER, "amenity" TEXT, "zone_id" INTEGER);')
    project.conn.execute(f"SELECT AddGeometryColumn('{table_name}', 'geometry', 4326, '{geom_type}', 'XY' );")
    project.conn.execute(f"SELECT CreateSpatialIndex('{table_name}', 'geometry' );")
    project.conn.commit()

    project.conn.executemany(qry, list_of_tuples)
    project.conn.commit()

    return tag_by_zone

def point_or_polygon(row):  # NÃO TEM ESSA FUNC. DO OUTRO LADO

    if row.type == 'node':

        return Point(row.lon, row.lat)

    else:

        poly = []
        for dct in row.geometry:
            poly.append((dct['lon'], dct['lat']))

        return Polygon(poly)
