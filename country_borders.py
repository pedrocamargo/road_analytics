import time
import re
import requests
from aequilibrae.project.network.osm_utils.osm_params import http_headers, memory
from shapely.geometry import MultiPolygon, Point, Polygon


def get_country_borders(country_name:str):
    qry = f'[out:json]; relation["boundary"="administrative"]["admin_level"="2"]["int_name"="{country_name}"];out geom;'
    
    url = "http://overpass-api.de/api/interpreter"
    response = requests.post(url, data={"data": qry}, timeout=180, headers=http_headers)
    
    res = response.json()
    
    q = [x for x in res['elements'][0]['members'] if x['role'] == 'outer']
    parts = []
    for data in q:
        small_area = data['geometry']
        if len(small_area) < 3:
            continue
        parts.append(Polygon([Point(p['lon'], p['lat']) for p in small_area]))

    return MultiPolygon(parts) 