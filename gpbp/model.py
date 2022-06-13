from asyncio import set_child_watcher
import logging
import sys
from fiona import prop_type

import geopandas as gpd
from aequilibrae import logger, Project

from gpbp.data_retrieval import subdivisions
from gpbp.model_creation.import_from_osm import import_net_from_osm
from gpbp.model_creation.raster_to_model import pop_to_model
from gpbp.model_creation.set_source import set_source
from gpbp.model_creation.subdivisions_to_model import add_subdivisions_to_model
from gpbp.model_creation.trigger_network import trigger_network
from gpbp.model_creation.trigger_population import trigger_population
from gpbp.model_creation.zoning.zone_building import zone_builder


class Model:
    def __init__(self, network_path: str, model_place: str = None):
        # TODO: MAKE SURE THE CLASS WORKS FOR USING THE MODEL AND CREATING IT
        # If the model exists, you would only tell where it is (network_path), and the software
        # would check and populate the model place.  Needs to be implemented
        self.__model_place = model_place
        self.__population_source = 'WorldPop'
        self.__folder = network_path
        self._project = Project()
        self.__starts_logging()

    def create(self):
        """Creates the entire model"""

        self.import_network()
        self.import_population()
        self.import_subdivisions(2, True)
        self.build_zoning()

    def set_population_source(self, source='WorldPop'):
        """ Sets the source for the raster population data
         Args:
                *source* (:obj:`str`): Can be 'WorldPop' or 'Meta'. Defaults to WorldPop
        """
        self.__population_source = set_source(source)

    def import_network(self):
        """Triggers the import of the network from OSM and adds subdivisions into the model """
        
        #self._project.new(self.__folder)
        trigger_network(self._project, self.__folder)

        import_net_from_osm(self._project, self.__model_place)

    def import_subdivisions(self, subdivisions=2, overwrite=False):
        """Imports political subdivisions.

         Args:
                *subdivisions* (:obj:`int`): Number of subdivision levels to import. Defaults to 2
                *overwrite* (:obj:`bool`): Deletes pre-existing subdivisions. Defaults to False

        """
        add_subdivisions_to_model(self._project, self.__model_place, subdivisions, overwrite)

    def import_population(self, overwrite=False):
        """Triggers the import of population from raster into the model"""

        trigger_population(self._project)

        pop_to_model(self._project, self.__model_place, self.__population_source, overwrite)

    def build_zoning(self, hexbin_size=200, max_zone_pop=10000, min_zone_pop=500, save_hexbins=True):
        """Creates hexagonal bins, and then clusters it regarding the political subdivision.

        TODO: DOCUMENT THIS METHOD AND TIE IT UP TO THE ACTUAL FUNCTION
        
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

    def close_model(self):
        """
        Close the project model.
        """
        self._project.close()

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
