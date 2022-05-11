import pandas as pd
import zipfile
import requests
from io import BytesIO

def check_pop(model_place: str, df_input: pd.DataFrame):
    '''
        Function that receives a population dataframe and compares its total value to a well known population data source.
        In this case, the well known source is a publicly available World Bank dataset, which can be found here: https://data.worldbank.org/indicator/SP.POP.TOTL
    '''
    
    url = "https://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv"
    r = requests.get(url)
    zip_file = BytesIO(r.content)
    with zipfile.ZipFile(zip_file, "r") as f:
        for name in f.namelist():
            if name == 'API_SP.POP.TOTL_DS2_en_csv_v2_4019998.csv':
                with f.open(name) as csv_file:
                    df_source = pd.read_csv(csv_file, skiprows = 4, encoding='utf-8')
                break
    
    source_value = df_source.loc[df_source['Country Name'] == model_place, '2020']
    df = pd.DataFrame({'': ['Vectorized from raster', 'World Bank source'], 'Total population': [int(df_input.population.sum()), int(source_value)]})
    df = df.groupby('').sum()
    df['Total population'] = df.apply(lambda x: "{:,}".format(x['Total population']), axis=1)
    
    return df