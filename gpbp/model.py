from asyncio import set_child_watcher
import logging
import sys

from numpy import tri
from fiona import prop_type

import geopandas as gpd
from aequilibrae import logger, Project

from gpbp.data_retrieval import subdivisions
from gpbp.data_retrieval.rural_access_index.basic_rai_computation import basic_RAI_data
from gpbp.data_retrieval.trigger_import_amenities import trigger_import_amenities
from gpbp.data_retrieval.trigger_import_building import trigger_building_import
from gpbp.model_creation.raster_to_model import pop_to_model
from gpbp.model_creation.set_source import set_source
from gpbp.model_creation.subdivisions_to_model import add_subdivisions_to_model
from gpbp.model_creation.trigger_network import trigger_network
from gpbp.model_creation.zoning.zone_building import zone_builder
from gpbp.model_creation.population_pyramid import get_population_pyramid

class Model:
    def __init__(self, network_path: str, model_place: str = None):
        # TODO: MAKE SURE THE CLASS WORKS FOR USING THE MODEL AND CREATING IT
        # If the model exists, you would only tell where it is (network_path), and the software
        # would check and populate the model place.  Needs to be implemented
        self.__model_place = model_place
        self.__population_source = 'WorldPop'
        self.__folder = network_path
        self._project = Project()
        self.__osm_data = {}
        self.__starts_logging()

    def create(self):
        """Creates the entire model"""
        
        self.import_subdivisions(2, True)
        self.import_network()
        self.import_population()
        self.build_zoning()
        self.import_population_pyramid()
        self.import_amenities()
        self.import_buildings()

    def set_population_source(self, source='WorldPop'):
        """ Sets the source for the raster population data
         Args:
                *source* (:obj:`str`): Can be 'WorldPop' or 'Meta'. Defaults to WorldPop
        """
        self.__population_source = set_source(source)

    def import_network(self):
        """Triggers the import of the network from OSM and adds subdivisions into the model. 
           If the network already exists in the folder, it will be loaded, otherwise it will be created."""
    
        trigger_network(self._project, self.__folder, self.__model_place)

    def import_subdivisions(self, subdivisions=2, overwrite=False):
        """Imports political subdivisions.

         Args:
                *subdivisions* (:obj:`int`): Number of subdivision levels to import. Defaults to 2
                *overwrite* (:obj:`bool`): Deletes pre-existing subdivisions. Defaults to False

        """
        add_subdivisions_to_model(self._project, self.__model_place, subdivisions, overwrite)

    def import_population(self, overwrite=False):
        """
        Triggers the import of population from raster into the model
        
        Args:
                *overwrite* (:obj:`bool`): Deletes pre-existing population_source_import. Defaults to False
        """

        pop_to_model(self._project, self.__model_place, self.__population_source, overwrite)

    def build_zoning(self, hexbin_size=200, max_zone_pop=10000, min_zone_pop=500, save_hexbins=True):
        """Creates hexagonal bins, and then clusters it regarding the political subdivision.
        
        Args:
             *hexbin_size*(:obj:`int`): size of the hexagonal bins to be created.
             *max_zone_pop*(:obj:`int`): max population living within a zone.
             *min_zone_pop*(:obj:`int`): min population living within a zone.
             *save_hexbins*(:obj:`bool`): saves the hexagonal bins with population. Defaults to True.
        """

        zone_builder(self._project, hexbin_size, max_zone_pop, min_zone_pop, save_hexbins)

    def get_political_subdivisions(self, level: int = None) -> gpd.GeoDataFrame:
        """Return political subdivisions from a country. 
        
        Args: 
             *level*(:obj:`int`): Number of subdivision levels to import. Default imports all levels.
        """

        subd = subdivisions(self._project)
        if level is not None:
            subd = subd[subd.level == level]
        return subd

    def close(self):
        """
        Close the project model.
        """
        self._project.close()

    def import_population_pyramid(self):
        """
        Triggers the import of population pyramid from raster into the model.
        """
        get_population_pyramid(self._project, self.__model_place)

    def import_amenities(self):
        """ Triggers the import of ammenities from OSM. 
            Data will be exported as columns in zones file and as a separate SQL file."""
        
        trigger_import_amenities(self.__model_place, self._project, self.__osm_data)

    def import_buildings(self):
        """ Triggers the import of buildings from both OSM and Microsoft Bing. 
            Data will be exported as columns in zones file and as a separate SQL file."""

        trigger_building_import(self.__model_place, self._project, self.__osm_data)

    def rai_computation(self):

        basic_RAI_data(self._project)

    @property
    def place(self):
        return self.__model_place

    @staticmethod
    def __starts_logging():
        stdout_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s;%(name)s;%(message)s")
        stdout_handler.setFormatter(formatter)
        stdout_handler.name = 'terminal'

        for handler in logger.handlers:
            if handler.name == 'terminal':
                return
        logger.addHandler(stdout_handler)
