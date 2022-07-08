from itertools import count
from numpy import safe_eval
import pandas as pd
import sqlite3
from aequilibrae import Project

from gpbp.data_retrieval.osm_tags.import_osm_data import import_osm_data
from gpbp.data_retrieval.osm_tags.query_writer import query_writer

def trigger_import_amenities(model_place:str, project:Project, osm_data: dict):

    osm_amenities = import_osm_data(model_place, osm_data, project, tag='amenity')

    zoning = project.zoning
    fields = zoning.fields

    count_amenities = osm_amenities.groupby(['amenity', 'zone_id']).count()
    count_amenities['zone_id'] = list(range(1, len(count_amenities)+1))
    
    for value in osm_amenities.building.unique().tolist():
        fields.add('osm_' + value + '_amenity', 'Number of ' + value + ' buildings provided by OSM', 'INTEGER')

    qry = query_writer(count_amenities, tag='amenity', func='set_value', is_area=False)
    list_of_tuples = count_amenities[['type']].unstack().fillna(0).itertuples(index=False, name=None)
    project.conn.executemany(qry, list_of_tuples)
    project.conn.commit()