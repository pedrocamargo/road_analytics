from turtle import down
import pandas as pd
import geopandas as gpd
import requests
from bs4 import BeautifulSoup
import pycountry

def population_source(model_place: str, source='WorldPop'):

    if source == 'WorldPop':

        pop_path = '/home/jovyan/workspace/road_analytics/gpbp/data/population/all_raster_pop_source.csv'
        df = pd.read_csv(pop_path)
        return df[df.Country.str.upper() == model_place.upper()].data_link.values[0]

    elif source == 'Meta':

        try:
            country_iso = pycountry.countries.get(name=model_place).alpha_3.lower()
        except AttributeError:
            country_iso = pycountry.countries.get(common_name=model_place).alpha_3.lower()

        if ' ' in model_place:
            model_place = model_place.replace(' ', '-')
        else:
            pass

        base_url = 'https://data.humdata.org'

        r = requests.get(base_url + f'/dataset/{model_place.lower()}-high-resolution-population-density-maps-demographic-estimates#')
        soup = BeautifulSoup(r.text, 'html.parser')

        if 'Page not found' in soup.find('h1').text:
            r = requests.get(base_url + f'/dataset/highresolutionpopulationdensitymaps-{country_iso}')
            soup = BeautifulSoup(r.text, 'html.parser')
        else:
            pass

        if len(soup.body.findAll(text=f'{country_iso}_general_2020_geotiff.zip')) > 0:
            downloadable_file = soup.find('a', {"title":f"{country_iso}_general_2020_geotiff.zip"}).parent.find_all('a')[1]['href']
        elif len(soup.body.findAll(text=f"{country_iso}_population_2020_geotiff.zip")) > 0:
            downloadable_file = soup.find('a', {"title":f"{country_iso}_population_2020_geotiff.zip"}).parent.find_all('a')[1]['href']
        elif len(soup.body.findAll(text=f'population_{country_iso}_2018-10-01_geotiff.zip')) > 0:
            downloadable_file = soup.find('a', {"title":f"population_{country_iso}_2018-10-01_geotiff.zip"}).parent.find_all('a')[1]['href']
        elif len(soup.body.findAll(text=f'population_{country_iso}.geotiff.zip')) > 0:
            downloadable_file = soup.find('a', {"title":f"population_{country_iso}.geotiff.zip"}).parent.find_all('a')[1]['href']
        else:
            raise ValueError('No population file found.')

        return base_url + downloadable_file

    else:
        raise ValueError("No population source found.")