import pandas as pd
import geopandas as gpd
import requests
from bs4 import BeautifulSoup
import pycountry

def import_meta_population(country_name:str):
    
    try:
        country_iso = pycountry.countries.get(name=country_name).alpha_3.lower()
    except AttributeError:
        country_iso = pycountry.countries.get(common_name=country_name).alpha_3.lower()

    if ' ' in country_name:
        country_name = country_name.replace(' ', '-')
    else:
        pass

    base_url = 'https://data.humdata.org'

    r = requests.get(base_url + f'/dataset/{country_name.lower()}-high-resolution-population-density-maps-demographic-estimates#')
    soup = BeautifulSoup(r.text, 'html.parser')

    if 'Page not found' in soup.find('h1').text:
        r = requests.get(base_url + f'/dataset/highresolutionpopulationdensitymaps-{country_iso}')
        soup = BeautifulSoup(r.text, 'html.parser')
    else:
        pass

    if len(soup.body.findAll(text=f'{country_iso}_general_2020_csv.zip')) > 0:
        downloadable_file = soup.find('a', {"title":f"{country_iso}_general_2020_csv.zip"}).parent.find_all('a')[1]['href']
    elif len(soup.body.findAll(text=f"{country_iso}_population_2020_csv.zip")) > 0:
        downloadable_file = soup.find('a', {"title":f"{country_iso}_population_2020_csv.zip"}).parent.find_all('a')[1]['href']
    elif len(soup.body.findAll(text=f'population_{country_iso}_2018-10-01.csv.zip')) > 0:
        downloadable_file = soup.find('a', {"title":f"population_{country_iso}_2018-10-01.csv.zip"}).parent.find_all('a')[1]['href']
    else:
        return 'No population file found.'
        
    df = pd.read_csv((base_url + downloadable_file), compression='zip')

    if 'population_2020' in df.columns:
        df = df.drop(columns=['population_2015']).rename(columns={'population_2020':'population'})
    elif f'{country_iso}_general_2020' in df.columns:
        df = df.rename(columns={f'{country_iso}_general_2020':'population'})
    else:
        df = df.rename(columns={f'{country_iso}_population_2020':'population'})

    pop_gdf = gpd.GeoDataFrame(df,
                               geometry=gpd.points_from_xy(df.longitude, df.latitude), 
                               crs=4326)
    
    return pop_gdf