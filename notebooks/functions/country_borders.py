import time
import re
import requests
from aequilibrae.project.network.osm_utils.osm_params import http_headers, memory
from shapely.geometry import MultiPolygon, Point, LineString
from shapely.ops import polygonize
from os.path import dirname, join
import pandas as pd
import shapely.wkb
import sqlite3


def get_country_borders(country_name:str):
    qry = f'[out:json]; relation["boundary"="administrative"]["admin_level"="2"]["int_name"="{country_name}"];out geom;'
    
    url = "http://overpass-api.de/api/interpreter"
    response = requests.post(url, data={"data": qry}, timeout=180, headers=http_headers)
    
    res = response.json()
    
    q = [x for x in res['elements'][0]['members'] if x['role'] == 'outer']
    sections = []
    for data in q:
        small_area = data['geometry']
        if len(small_area) < 3:
            continue

        sections.append(LineString([Point(p['lon'], p['lat']) for p in small_area]))

    polyg = MultiPolygon(polygonize(sections))
    if polyg.area == 0:
        pth = join(dirname(dirname(dirname(__file__))), 'model', 'data', 'country_borders.sqlite')
        conn = sqlite3.connect(pth)
        conn.enable_load_extension(True)
        conn.load_extension("mod_spatialite")
        country_wkb = conn.execute('Select asBinary(geometry) from country_borders where name=?', [country_name]).fetchone()[0]
        polyg =  MultiPolygon(shapely.wkb.loads(country_wkb))
        conn.close()
        
    return polyg