from numpy import safe_eval
import pandas as pd
import sqlite3
from aequilibrae import Project

from gpbp.data_retrieval.osm_tags.import_osm_amenities import import_osm_amenities

def trigger_import_amenities(model_place:str, project:Project, osm_data: dict):

    df = import_osm_amenities(model_place, project, osm_data)

    zoning = project.zoning
    fields = zoning.fields

    groups = df.groupby(['amenity', 'zone_id']).count()

    for idx, row in groups.iterrows():

        field_name = 'osm_' + idx[0] + '_amenity'
        field_desc = 'osm ' + idx[0] + ' amenity'
        
        try:
            fields.add(field_name, field_desc, 'INTEGER')
        except:
            pass

        single_tuple = (int(row.id), idx[1])

        qry = f'UPDATE zones SET {field_name}=? WHERE zone_id=?;'
        project.conn.execute(qry, single_tuple)
        project.conn.commit()

        qry = f'UPDATE zones SET {field_name}=0 WHERE {field_name} IS NULL;'
        project.conn.execute(qry)
        project.conn.commit()

    project.conn.execute(f'CREATE TABLE IF NOT EXISTS osm_amenities("type" TEXT, "id" INTEGER, "amenity" TEXT, "zone_id" INTEGER);')
    project.conn.execute(f"SELECT AddGeometryColumn('osm_amenities', 'geometry', 4326, 'POINT', 'XY' );")
    project.conn.execute(f"SELECT CreateSpatialIndex( 'osm_amenities' , 'geometry' );")
    project.conn.commit()

    sql = f"INSERT into osm_amenities(type, id, amenity, zone_id, geometry) VALUES(?, ?, ?, ?, CastToPoint(GeomFromWKB(?, 4326)));"

    for _, rec in df.iterrows():
        project.conn.execute(sql, [rec['type'], rec['id'], rec['amenity'], rec['zone_id'], rec.geom.wkb])

    project.conn.commit()