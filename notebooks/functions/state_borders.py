import time
import re
import requests
from aequilibrae.project.network.osm_utils.osm_params import http_headers, memory
from shapely.geometry import MultiPolygon, Point, LineString
from shapely.ops import polygonize

def get_state_borders(state_name:str):
    qry = f'[out:json]; relation["boundary"="administrative"]["admin_level"="4"]["name"="{state_name}"];out geom;'
    
    url = "http://overpass-api.de/api/interpreter"
    response = requests.post(url, data={"data": qry}, timeout=180, headers=http_headers)
    
    res = response.json()
    
    q = [x for x in res['elements'][0]['members'] if x['role'] == 'outer']
    sections = []
    for data in q:
        small_area = data['geometry']
        sections.append(LineString([Point(p['lon'], p['lat']) for p in small_area]))

    return MultiPolygon(polygonize(sections))