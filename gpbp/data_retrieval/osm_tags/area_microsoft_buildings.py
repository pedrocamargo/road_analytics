from aequilibrae import Project
import geopandas as gpd
import sqlite3

def area_microsoft_buildings(buildings_by_zone:gpd.GeoDataFrame, zones:gpd.GeoDataFrame, project:Project):
    
    missing_idx = zones.zone_id.tolist()
    
    total_area = buildings_by_zone.groupby('zone_id').sum()['area'].to_dict()
    
    for key in missing_idx:
        if key not in total_area.keys():
            total_area[key] = 0
    
    zoning = project.zoning
    fields = zoning.fields

    #Mudar controle no código
    try:
        fields.add('microsoft_building_area', 'Building area provided by Microsoft Bing', 'INTEGER')
    except:
        pass
    
    list_of_tuples = list(zip(total_area.values(), total_area.keys()))

    qry = f'UPDATE zones SET microsoft_building_area=? WHERE zone_id=?;'
    project.conn.executemany(qry, list_of_tuples)
    project.conn.commit()
