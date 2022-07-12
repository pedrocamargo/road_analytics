import pandas as pd
import numpy as np

def pop_data(country_df):
    
    country_age = np.unique(country_df.Age).tolist()
    
    description_field = []

    for i in range(len(country_age) - 1):
        description_field.append('Women population ' + country_age[i] + ' to ' + country_age[i+1] + ' years old.')
        description_field.append('Men population ' + country_age[i] + ' to ' + country_age[i+1] + ' years old.')
    
    description_field.append('Women population over ' + country_age[-1] + ' years old.')
    description_field.append('Men population over ' + country_age[-1] + ' years old.')
    
    columns_name = ['women_' + row.Age if row.Sex == 'f' else 'men_' + row.Age for _, row in country_df.iterrows()]
            
    return description_field, columns_name
