from ..functions.urban_areas import select_urban_areas

from ..functions.load_vectorized_pop import load_vectorized_pop


def population_data(country_name: str, project):

    population = load_vectorized_pop(project)
    urban_areas = select_urban_areas(country_name)
    urban_pop = population.overlay(urban_areas, how='intersection')

    return population.loc[~population.hex_id.isin(urban_pop.hex_id.values), :]
