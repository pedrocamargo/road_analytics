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


def get_country_borders(country_name: str):
    pth = join(dirname(dirname(dirname(__file__))), 'model', 'data', 'country_borders.sqlite')
    conn = sqlite3.connect(pth)
    conn.enable_load_extension(True)
    conn.load_extension("mod_spatialite")
    sql = 'Select asBinary(geometry) from country_borders where name=?'
    country_wkb = conn.execute(sql, [country_name]).fetchone()[0]
    polyg = MultiPolygon(shapely.wkb.loads(country_wkb))
    conn.close()

    return polyg
