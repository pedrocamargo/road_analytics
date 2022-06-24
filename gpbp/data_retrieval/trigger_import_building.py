from aequilibrae import Project
import pandas as pd
import geopandas as gpd

from gpbp.data_retrieval.microsoft_building import microsoft_building
from gpbp.data_retrieval.osm_building_import import osm_building

def trigger_building_import(model_place: str, project: Project, osm_data):

    microsoft_building(model_place, project)

    osm_building(project, osm_data)

