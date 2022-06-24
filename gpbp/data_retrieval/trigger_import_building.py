from aequilibrae import Project
import pandas as pd
import geopandas as gpd

from gpbp.data_retrieval.microsoft_building import microsoft_building
from gpbp.data_retrieval.osm_building_import import osm_building_import

def trigger_building_import(model_place: str, project: Project, osm_data: dict):

    microsoft_building(project, model_place)

    osm_building_import(project, osm_data, model_place)

