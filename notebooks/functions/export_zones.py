from shapely.geometry import MultiPolygon
from shapely.ops import polygonize
import pandas as pd
import sqlite3

def export_zones(zone_data, project):
    
    zoning = project.zoning
    for zone_id, row in zone_data.iterrows():
        zone = zoning.new(zone_id)
        zone.geometry = row.geometry
        zone.population = row.population
        zone.save()
        # None means that the centroid will be added in the geometric point of the zone
        # But we could provide a Shapely point as an alternative
        zone.add_centroid(False)
        zone.connect_mode(mode_id="c", connectors=1)
