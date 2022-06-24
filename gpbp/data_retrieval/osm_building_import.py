import sqlite3
from aequilibrae import Project

from gpbp.data_retrieval.osm_tags.import_osm_buildings import import_osm_buildings
from gpbp.data_retrieval.osm_tags.save_osm_amenities import export_tag_info

def osm_building_import(project:Project, osm_data:dict, model_place:str):
        
    df = import_osm_buildings(model_place, project, osm_data)

    zoning = project.zoning
    fields = zoning.fields

    groups = df.groupby(['building', 'zone_id']).count()[['id']]

    groups['area'] = df.groupby(['building', 'zone_id']).sum().round(decimals=2)['area'].tolist()

    for idx, row in groups.iterrows():

        field_name_1 = 'osm_' + idx[0] + '_building'
        field_desc_1 = 'Number of ' + idx[0] + ' buildings provided by OSM'
        field_name_2 = 'osm_' + idx[0] + '_building_area'
        field_desc_2 = idx[0] + ' building area provided by OSM'

        try:
            fields.add(field_name_1, field_desc_1, 'INTEGER')
            fields.add(field_name_2, field_desc_2, 'INTEGER')
        except:
            pass

        single_tuple_1 = (int(row.id), idx[1])
        single_tuple_2 = (int(row.area), idx[1])

        qry = f'UPDATE zones SET {field_name_1}=? WHERE zone_id=?;'
        project.conn.execute(qry, single_tuple_1)
        project.conn.commit()

        qry = f'UPDATE zones SET {field_name_1}=0 WHERE {field_name_1} IS NULL;'
        project.conn.execute(qry)
        project.conn.commit()

        qry = f'UPDATE zones SET {field_name_2}=? WHERE zone_id=?;'
        project.conn.execute(qry, single_tuple_2)
        project.conn.commit()

        qry = f'UPDATE zones SET {field_name_2}=0 WHERE {field_name_2} IS NULL;'
        project.conn.execute(qry)
        project.conn.commit()

    project.conn.execute(f'CREATE TABLE IF NOT EXISTS osm_buildings("type" TEXT, "id" INTEGER, "building" TEXT, \
                            "zone_id" INTEGER, "area" FLOAT);')
    project.conn.execute( f"SELECT AddGeometryColumn('osm_buildings', 'geometry', 4326, 'POINT', 'XY' );")
    project.conn.execute(f"SELECT CreateSpatialIndex( 'osm_buildings' , 'geometry' );")
    project.conn.commit()

    sql = f"INSERT into osm_buildings(type, id, building, zone_id, area, geometry) VALUES(?, ?, ?, ?, ?, CastToPoint(GeomFromWKB(?, 4326)));"

    for _, rec in df.iterrows():
        project.conn.execute(sql, [rec['type'], rec['id'], rec['building'], rec['zone_id'], rec.area, rec.geom.wkb])

    project.conn.commit()
