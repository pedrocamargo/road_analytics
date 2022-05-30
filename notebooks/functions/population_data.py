import pandas as pd

def pop_data(country_df):
    
    country_age = country_df.Age.tolist()
    
    description_field = []

    for i in range(len(country_age)):
        if country_df.Sex.tolist()[i] == 'f':
            try:
                description_field.append('Women population ' + country_age[i] + ' to ' +\
                                                   country_age[i+2] + ' years old.')
            except IndexError:
                description_field.append('Women population over ' + country_age[i] + ' years old.')
        else:
            try:
                description_field.append('Men population ' + country_age[i] + ' to ' +\
                                                   country_age[i+2] + ' years old.')
            except IndexError:
                description_field.append('Men population over ' + country_age[i] + ' years old.')

    
    columns_name = ['women_'+ country_age[i] if country_df.Sex.tolist()[i] == 'f' else\
                    'men_'+ country_age[i] for i in range(len(country_df))]
            
    return description_field, columns_name
