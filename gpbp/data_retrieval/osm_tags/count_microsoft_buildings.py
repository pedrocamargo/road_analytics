from aequilibrae import Project
import geopandas as gpd
import sqlite3


def count_microsoft_buildings(buildings_by_zone: gpd.GeoDataFrame, zones: gpd.GeoDataFrame, project: Project):

    missing_idx = zones.zone_id.tolist()

    count_buildings = buildings_by_zone.groupby('zone_id').count()['area'].to_dict()

    for key in missing_idx:
        if key not in count_buildings.keys():
            count_buildings[key] = 0

    zoning = project.zoning
    fields = zoning.fields

    try:
        fields.add('microsoft_building_count', 'Number of buildings provided by Microsoft Bing', 'INTEGER')
    except:
        pass

    list_of_tuples = list(zip(count_buildings.values(), count_buildings.keys()))

    qry = f'UPDATE zones SET microsoft_building_count=? WHERE zone_id=?;'
    project.conn.executemany(qry, list_of_tuples)
    project.conn.commit()
