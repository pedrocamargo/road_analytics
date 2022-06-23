import imp
import io
import geopandas as gpd
import zipfile
import requests
from os.path import join
from tempfile import tempdir
from bs4 import BeautifulSoup

def read_bing_file(model_place: str):

    url = 'https://github.com/microsoft/GlobalMLBuildingFootprints'

    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        downloadable_link = soup.find('td', string=f'{model_place}').find_next_siblings()[1].find('a')['href']

    except AttributeError:
        print('There is no available data for the country in Bing database.')
        return

    r = requests.get(downloadable_link)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    filename = z.namelist()[0]
    var = join(tempdir, z.extract(filename))

    return gpd.read_file(var)


