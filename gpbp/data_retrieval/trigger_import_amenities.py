from numpy import safe_eval
import pandas as pd
import sqlite3
from aequilibrae import Project

from data_retrieval.osm_tags.adjust_osm_frame import import_osm_frame
from data_retrieval.osm_tags.save_osm_amenities import export_amenitites_dataframe
from gpbp.data_retrieval.osm_tags.save_osm_amenities import export_tag_info

def trigger_import_amenities(project:Project, osm_data = self.__osm_data):

    df = import_osm_frame(project, tag='amenity')

    zoning = project.zoning
    fields = zoning.fields

    groups = df.groupby(['amenity', 'zone_id']).count()

    for idx, row in groups.iterrows():

        field_name = 'osm_' + idx[0] + '_amenity'
        field_desc = 'osm ' + idx[0] + ' amenity'

        fields.add(field_name, field_desc, 'INTEGER')

        single_tuple = (int(row.id), idx[1])

        qry = f'UPDATE zones SET {field_name}=? WHERE zone_id=?;'
        project.conn.execute(qry, single_tuple)
        project.conn.commit()

        qry = f'UPDATE zones SET {field_name}=0 WHERE {field_name} IS NULL;'
        project.conn.execute(qry)
        project.conn.commit()

    print('OSM amenities loaded into zones.')

    export_tag_info(df, project, tag='amenity')

    print('OSM amenities saved into osm_amenities file.')