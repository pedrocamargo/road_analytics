import sqlite3
import pandas as pd
from aequilibrae import Project

def export_tag_info(df, project: Project, tag:str):

    if tag == 'amenity':
        file_name = 'osm_amenities'

        project.conn.execute(f'CREATE TABLE IF NOT EXISTS {file_name}("type" TEXT, "id" INTEGER, "{tag}" TEXT, "zone_id" INTEGER);')
        project.conn.execute(f"SELECT AddGeometryColumn({file_name}, 'geometry', 4326, 'POINT', 'XY' );")
        project.conn.execute(f"SELECT CreateSpatialIndex( {file_name} , 'geometry' );")
        project.conn.commit()

        sql = f"INSERT into {file_name}(type, id, {tag}, zone_id, geometry) VALUES(?, ?, ?, ?, CastToPoint(GeomFromWKB(?, 4326)));"

        for _, rec in df.iterrows():
            project.conn.execute(sql, [rec['type'], rec['id'], rec[f'{tag}'], rec['zone_id'], rec.geom.wkb])

        project.conn.commit()

    else:
        file_name = 'osm_buildings'

        project.conn.execute(f'CREATE TABLE IF NOT EXISTS {file_name}("type" TEXT, "id" INTEGER, "{tag}" TEXT, \
                                "zone_id" INTEGER, "area" FLOAT);')
        project.conn.execute( f"SELECT AddGeometryColumn({file_name}, 'geometry', 4326, 'POINT', 'XY' );")
        project.conn.execute(f"SELECT CreateSpatialIndex( {file_name} , 'geometry' );")
        project.conn.commit()

        sql = f"INSERT into {file_name}(type, id, {tag}, zone_id, geometry) VALUES(?, ?, ?, ?, CastToPoint(GeomFromWKB(?, 4326)));"

        for _, rec in df.iterrows():
            project.conn.execute(sql, [rec['type'], rec['id'], rec[f'{tag}'], rec['zone_id'], rec.area, rec.geom.wkb])

        project.conn.commit()

        sql = f"INSERT into {file_name}(type, id, {tag}, zone_id, geometry) VALUES(?, ?, ?, ?, CastToMulti(GeomFromWKB(?, 4326)));"
