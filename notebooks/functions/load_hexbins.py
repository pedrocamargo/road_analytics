import geopandas as gpd


def load_hexbins(project):
    sql = "SELECT hex_id, country_subdivision, x, y, Hex(ST_AsBinary(GEOMETRY)) geometry, population FROM hex_pop;"
    return gpd.GeoDataFrame.from_postgis(sql, project.conn, geom_col="geometry", crs=4326)
