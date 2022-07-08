import sqlite3
from aequilibrae import Project
import geopandas as gpd

from gpbp.data_retrieval.osm_tags.microsoft_buildings_by_zone import microsoft_buildings_by_zone


def microsoft_building(model_place:str, project:Project):

    buildings_by_zone = microsoft_buildings_by_zone(model_place, project)
    
    zoning = project.zoning
    fields = zoning.fields

    fields.add('microsoft_building_count', 'Number of buildings provided by Microsoft Bing', 'INTEGER')
    fields.add('microsoft_building_area', 'Building area provided by Microsoft Bing', 'FLOAT')

    count_buildings = buildings_by_zone.groupby('zone_id').count()
    total_area = buildings_by_zone.groupby('zone_id').sum()
    
    list_of_tuples = [(x, y, z) for x, y, z in zip(count_buildings.area, total_area.area, count_buildings.index)]

    qry= 'UPDATE zones SET microsoft_building_count=?, microsoft_building_area=? WHERE zone_id=?;'
    project.conn.executemany(qry, list_of_tuples)
    project.conn.commit()
 
    qry = 'UPDATE zones SET microsoft_building_area=0, microsoft_building_count=0 WHERE microsoft_building_count IS NULL;'
    project.conn.executemany(qry)
    project.conn.commit()
