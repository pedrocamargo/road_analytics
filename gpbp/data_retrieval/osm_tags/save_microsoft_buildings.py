import sqlite3
from aequilibrae import Project
import geopandas as gpd

def save_microsoft_buildings(gdf: gpd.GeoDataFrame, project:Project):

    project.conn.execute('Drop TABLE IF EXISTS microsoft_buildings;')
    project.conn.execute( 'CREATE TABLE IF NOT EXISTS microsoft_buildings("id" INTEGER, "area" FLOAT, "zone_id" INTEGER);')
    project.conn.execute( "SELECT AddGeometryColumn('microsoft_buildings', 'geometry', 4326, 'MULTIPOLYGON', 'XY' );")

    project.conn.execute( "SELECT CreateSpatialIndex( 'microsoft_buildings' , 'geometry' );")
    project.conn.commit()

    qry = '''INSERT into microsoft_buildings(id, area, zone_id, geometry) VALUES(?, ?, ?, CastToMulti(GeomFromWKB(?, 4326)));'''
    list_of_tuples = [(x,y,z,a) for x,y,z,a in zip(gdf.id, gdf.area, gdf. zone_id, gdf.geometry.to_wkb())]

    project.conn.executemany(qry, list_of_tuples)

    project.conn.commit()