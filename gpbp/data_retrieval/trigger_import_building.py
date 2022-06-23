from os import O_ASYNC
from aequilibrae import Project
import pandas as pd
import geopandas as gpd

import data_retrieval.microsoft_building_import as microsoft_building_import
import data_retrieval.osm_building_import as osm_building_import

def trigger_building_import(model_place: str, project: Project, osm_data):

    microsoft_building_import(model_place, project)

    print('Microsoft Bing builidings loaded into zones.')

    osm_building_import(project, osm_data)

    print('OSM buildings loaded into zones.')
