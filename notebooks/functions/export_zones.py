from shapely.geometry import MultiPolygon
from shapely.ops import polygonize
import pandas as pd
import sqlite3

def export_zones(zoning, project):
    
    for index, row in zoning.iterrows():

        project.conn.execute('CREATE TABLE IF NOT EXISTS zoning_pop("zone_id" INTEGER, "state" TEXT, "population" FLOAT,\
                                                            "final_zone_id" INTEGER);')
        project.conn.execute("SELECT AddGeometryColumn( 'zoning_pop', 'geometry', 4326, 'MULTIPOLYGON', 'XY' );")
        project.conn.execute("SELECT CreateSpatialIndex( 'zoning_pop' , 'geometry' );")
        project.conn.commit()

        project.conn.execute('INSERT into zoning_pop(zone_id, state, geometry, population, final_zone_id)\
                                  VALUES(?, ?, GeomFromWKB(?, 4326), ?, ?);',
                                 [index, row['state'], MultiPolygon(polygonize(row['geometry'])).wkb, 
                                  row['population'], row['final_zone_id']])
        project.conn.commit()
