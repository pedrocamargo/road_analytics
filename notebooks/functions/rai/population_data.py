from .urban_areas import select_urban_areas

from ..load_vectorized_pop import load_vectorized_pop


def population_data(country_name: str, project):

    population = load_vectorized_pop(project)
    urban_areas = select_urban_areas(project)
    return population.overlay(urban_areas, how='difference')
