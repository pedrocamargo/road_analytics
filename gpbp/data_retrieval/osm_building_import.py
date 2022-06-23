import sqlite3
from aequilibrae import Project

from gpbp.data.load_zones import load_zones
from data_retrieval.osm_tags.adjust_osm_frame import import_osm_frame
from gpbp.data_retrieval.osm_tags.save_osm_amenities import export_tag_info

def osm_building_import(project, osm_data):
        
    df = import_osm_frame(project, osm_data, tag='building')

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

    export_tag_info(df, project, tag='building')
