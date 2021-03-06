import pandas as pd
import geopandas as gpd

from functions.population_data import pop_data
from functions.load_zones import load_zones
from functions.population_raster import population_raster

def get_population_pyramid(model_place:str, project):
    
    pop_path = f'../model/population/all_raster_pop_age_and_sex_source.csv'
    
    population_df = pd.read_csv(pop_path)
    
    country_df = population_df[population_df.Country == model_place].copy()#[:6]
    
    description_field, columns_name = pop_data(country_df)
    
    country_df['desc_field'] = description_field
    country_df['field_name'] = columns_name
    
    zoning = project.zoning
    fields = zoning.fields
    
    zones = load_zones(project)
    
    for index, row in country_df.iterrows():
        
        gdf_pop = population_raster(row.data_link, row.field_name, project)
        
        pop_per_zone = zones.sjoin(gdf_pop).groupby('zone_id').sum().astype(int)

        dict_pop = pop_per_zone['population'].to_dict()

        missing_idx = zones.index.tolist()

        for i in range(1, len(zones)+1):
            if i not in missing_idx:
                dict_pop[i] = 0

        list_of_tuples = list(zip(dict_pop.keys(), dict_pop.values()))

        fields.add(row.field_name, row.desc_field, 'INTEGER')

        qry = f'UPDATE zones SET {row.field_name}=? WHERE zone_id=?;'
        project.conn.executemany(qry, list_of_tuples)
        project.conn.commit()

        print(f'Obtained {row.desc_field}')
    
    