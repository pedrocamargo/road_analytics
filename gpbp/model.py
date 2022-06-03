import logging
import sys

from aequilibrae import logger, Project, Parameters

from gpbp.model_creation.import_from_osm import import_net_from_osm
from gpbp.model_creation.raster_to_model import pop_to_model
from gpbp.model_creation.subdivisions_to_model import add_subdivisions_to_model


class Model:
    def __init__(self, network_path: str, model_place: str = None):
        # TODO: MAKE SURE THE CLASS WORKS FOR USING THE MODEL AND CREATING IT
        # If the model exists, you would only tell where it is (network_path), and the software
        # would check and populate the model place.  Needs to be implemented
        self.__model_place = model_place
        self.__population_source = 'WorldPop'
        self.__folder = network_path
        self.__project = Project()
        self.__starts_logging()

    def create(self):
        """Creates the entire model"""

        self.import_network()
        self.import_population()
        self.import_subdivisions(2, True)
        self.import_population(True)
        self.build_zoning()

    def set_population_source(self, source='WorldPop'):
        """ Sets the source for the raster population data
         Args:
                *source* (:obj:`str`): Can be 'WorldPop' or 'Meta'. Defaults to WorldPop
        """
        pass

    def import_network(self):
        """Triggers the import of the network from OSM and adds subdivisions into the model """
        self.__project.new(self.__folder)

        import_net_from_osm(self.__project, self.__model_place)

    def import_subdivisions(self, subdivisions=2, overwrite=False):
        """XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

         Args:
                *subdivisions* (:obj:`int`): Number of subdivision levels to import. Defaults to 2
                *overwrite* (:obj:`bool`): Deletes pre-existing subdivisions. Defaults to False

        """
        add_subdivisions_to_model(self.__project, self.__model_place, subdivisions, overwrite)

    def import_population(self, overwrite=False):
        """Triggers the import of population from raster into the model"""

        pop_to_model(self.__project, self.__model_place, self.__population_source, overwrite)

    def build_zoning(self, hexbin_size=200, max_zone_pop=10000):
        """TODO: DOCUMENT THIS METHOD AND TIE IT UP TO THE ACTUAL FUNCTION"""
        pass

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
