import geopandas as gpd
from gpbp.data_retrieval.get_all_subdivisions import subdivisions
from gpbp.model_creation.zoning.export_hex_population import export_hex_population

from gpbp.model_creation.zoning.export_zones import export_zones
from gpbp.model_creation.zoning.create_clusters import create_clusters
from gpbp.model_creation.zoning.hex_builder import hex_builder
from gpbp.model_creation.zoning.zones_with_location import zones_with_location
from gpbp.model_creation.zoning.zones_with_pop import zones_with_population


def zone_builder(project, hexbin_size: int, max_zone_pop: int, min_zone_pop: int, save_hexbins:bool):
    
    sql = "SELECT country_name, Hex(ST_AsBinary('GEOMETRY')) AS geom FROM country_borders;"
    country = gpd.GeoDataFrame.from_postgis(sql, project.conn, geom_col="geom", crs=4326)
    coverage_area = country.to_crs('epsg:3857')

    hexb = hex_builder(coverage_area, hexbin_size, epsg=3857)
    hexb.to_crs('epsg:4326', inplace=True)

    states = subdivisions(project)
    states = states[states.level == states.level.max()]
    
    zones_with_locations = zones_with_location(hexb, states)

    zones_with_pop = zones_with_population(project, zones_with_locations)

    export_hex_population(project, zones_with_pop)
        
    clusters = create_clusters(zones_with_pop, max_zone_pop, min_zone_pop)

    export_zones(clusters, project)
