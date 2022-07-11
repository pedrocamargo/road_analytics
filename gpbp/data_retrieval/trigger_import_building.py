from aequilibrae import Project
import pandas as pd
import geopandas as gpd

#from gpbp.data_retrieval.osm_building_import import osm_building_import
from gpbp.data_retrieval.osm_tags.import_osm_data import import_osm_data
from gpbp.data_retrieval.osm_tags.microsoft_buildings_by_zone import microsoft_buildings_by_zone
from gpbp.data_retrieval.osm_tags.query_writer import query_writer


def trigger_building_import(model_place: str, project: Project, osm_data: dict):

    zoning = project.zoning
    fields = zoning.fields

    try:
        microsoft_buildings = microsoft_buildings_by_zone(model_place, project)

        fields.add('microsoft_bld_count', 'Number of buildings provided by Microsoft Bing', 'INTEGER')
        fields.add('microsoft_bld_area', 'Building area provided by Microsoft Bing', 'FLOAT')

        count_microsoft_buildings = microsoft_buildings.groupby('zone_id').count()
        total_microsoft_area = microsoft_buildings.groupby('zone_id').sum()

        list_of_tuples = [(x, y, z) for x, y, z in zip(count_microsoft_buildings.area, total_microsoft_area.area, count_microsoft_buildings.index)]

        qry = 'UPDATE zones SET microsoft_bld_area=0, microsoft_bld_count=0 WHERE microsoft_building_count IS NULL;'
        project.conn.executemany(qry)
        project.conn.commit()

        qry = 'UPDATE zones SET microsoft_bld_count=?, microsoft_bld_area=? WHERE zone_id=?;'
        project.conn.executemany(qry, list_of_tuples)
        project.conn.commit()
    
    except ValueError:
        pass

    osm_buildings = import_osm_data(model_place, osm_data, project, tag='building')

    count_osm_buildings = osm_buildings.groupby(['building', 'zone_id']).count()
    count_osm_buildings['zone_id'] = list(range(1, len(count_osm_buildings)+1))
    area_osm_buildings = osm_buildings.groupby(['building', 'zone_id']).sum().round(decimals=2)
    area_osm_buildings['zone_id'] = list(range(1, len(area_osm_buildings)+1))

    for value in osm_buildings.building.unique().tolist():
        fields.add('osm_' + value + '_bld', 'Number of ' + value + ' buildings provided by OSM', 'INTEGER')
        fields.add('osm_' + value + '_bld_area', value + ' building area provided by OSM', 'FLOAT')

    qry = query_writer(count_osm_buildings, tag='building', func='set_value', is_area=False)
    list_of_tuples = count_osm_buildings[['type']].unstack().fillna(0).itertuples(index=False, name=None)
    project.conn.executemany(qry, list_of_tuples)
    project.conn.commit()

    qry = query_writer(count_osm_buildings, tag='building', func='set_value', is_area=True)
    list_of_tuples = count_osm_buildings[['type']].unstack().fillna(0).itertuples(index=False, name=None)
    project.conn.executemany(qry, list_of_tuples)
    project.conn.commit()
