from shapely.geometry import MultiPolygon
from shapely.ops import polygonize
import sqlite3
import pandas as pd

def export_hex_population(project, zones_with_pop):
    
    project.conn.execute('CREATE TABLE IF NOT EXISTS hex_pop ("hex_bins" TEXT, "state" TEXT, "x" FLOAT, "y" FLOAT, "population" FLOAT);')
    project.conn.execute("SELECT AddGeometryColumn('hex_pop', 'geometry', 4326, 'MULTIPOLYGON', 'XY' );")
    project.conn.execute("SELECT CreateSpatialIndex('hex_pop' , 'geometry');")
    project.conn.commit()
    
    for index, row in zones_with_pop.iterrows():
    
        project.conn.execute('INSERT into hex_pop(hex_bins, state, x, y, geometry, population) \
                              VALUES(?, ?, ?, ?, GeomFromWKB(?, 4326), ?);',
                             [row['hex_id'], row['state'], row['x'], row['y'], 
                              MultiPolygon(polygonize(row['geometry'])).wkb, row['population']])
        project.conn.commit()