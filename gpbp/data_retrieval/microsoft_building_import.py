import sqlite3
from aequilibrae import Project

from gpbp.data.load_zones import load_zones
from data_retrieval.osm_tags.microsoft_buildings_by_zone import microsoft_buildings_by_zone
from data_retrieval.osm_tags.save_microsoft_buildings import save_microsoft_buildings
from data_retrieval.osm_tags.count_microsoft_buildings import count_microsoft_buildings
from data_retrieval.osm_tags.area_microsoft_buildings import area_microsoft_buildings

def microsoft_building_import(model_place:str, project:Project):

    zones = load_zones(project)

    buildings_by_zone = microsoft_buildings_by_zone(model_place, zones, project)
    
    save_microsoft_buildings(buildings_by_zone)
    
    count_microsoft_buildings(buildings_by_zone, zones, project)
    
    area_microsoft_buildings(buildings_by_zone, zones, project)
    
    print('Building data from Microsoft Bing loaded into model.')
