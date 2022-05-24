import geopandas as gpd
import sqlite3

def load_zones(project):
    
    sql = "SELECT zone_id, population, Hex(ST_AsBinary(GEOMETRY)) geometry FROM zones;"
    zones  = gpd.GeoDataFrame.from_postgis(sql, project.conn, geom_col="geometry", crs=3857)
    zones.to_crs(3857, inplace=True)
    
    return zones