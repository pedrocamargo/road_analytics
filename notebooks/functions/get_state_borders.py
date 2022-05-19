import time
import re
import requests
from aequilibrae.project.network.osm_utils.osm_params import http_headers, memory
from shapely.geometry import MultiPolygon, Point, LineString
from shapely.ops import polygonize
import pycountry

from functions.admin_level_per_country import admin_level

def state_borders(country_name:str):
  
    try:        
        qry = f'[out:json]; area["boundary"="administrative"]["admin_level"="2"]["int_name"="{country_name}"]-> .searchArea;\
                rel(area.searchArea)["admin_level"="{admin_level[country_name]}"]["boundary"="administrative"];out geom;>;\
                out geom;'
    except:
        qry = f'[out:json]; area["boundary"="administrative"]["admin_level"="2"]["int_name"="{country_name}"]-> .searchArea;\
                rel(area.searchArea)["admin_level"="4"]["boundary"="administrative"];out geom;>;out geom;'
    
    url = "http://overpass-api.de/api/interpreter"
    response = requests.post(url, data={"data": qry}, timeout=180, headers=http_headers)
    res = response.json()
    
    iso_code = pycountry.countries.get(name=country_name).alpha_2
    
    q, states_in_country = {}, {}
    for i in res['elements']:
        try:
            if iso_code in i['tags']['ISO3166-2']:
                states_in_country[i['tags']['ISO3166-2']] = i['tags']['name']
                for x in i['members']:
                    if x['role'] == 'outer':
                        if i['tags']['ISO3166-2'] not in q:
                            q[i['tags']['ISO3166-2']] = [] 
                        q[i['tags']['ISO3166-2']].append(x)

        except:
            pass
        
    sections = {}

    for key, value in q.items():
        sections[key] = []
        for data in value:
            small_area = data['geometry']
            sections[key].append(LineString([Point(p['lon'], p['lat']) for p in small_area]))
    
    return sections, states_in_country