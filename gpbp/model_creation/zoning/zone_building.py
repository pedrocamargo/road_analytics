import geopandas as gpd
from aequilibrae import Project

from gpbp.model_creation.zoning.hex_builder import hex_builder


def zone_builder(project: Project, hexbin_size: int, max_zone_pop: int):
    sql = "select country_name, Hex(ST_AsBinary('geometry')) from country_borders"
    country = gpd.GeoDataFrame.from_postgis(sql, project.conn, geom_col="geometry", crs=4326)

    coverage_area = country.to_crs('epsg:3857')

    hexb = hex_builder(coverage_area, hexbin_size, epsg=3857)
    hexb.to_crs('epsg:4326', inplace=True)
