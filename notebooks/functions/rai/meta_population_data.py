from functions.rai.urban_areas import select_urban_areas

from functions.rai.import_meta_population import import_meta_population

def meta_population_data(country_name: str, project):
    
    population = import_meta_population(country_name)
    urban_areas = select_urban_areas(project)
    
    if type(population) == str:
        return f'Unable to continue without population information for {country_name}'
    else:
        return population.overlay(urban_areas, how='difference')
