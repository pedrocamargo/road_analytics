import geopandas as gpd
from aequilibrae import Project

from gpbp.data_retrieval.osm_tags.read_microsoft_file import read_bing_file

def microsoft_buildings_by_zone(model_place: str, zones: gpd.GeoDataFrame, project: Project):

    model_gdf = read_bing_file(model_place)

    model_gdf['area'] = model_gdf.geometry.to_crs(3857).area

    buildings_by_zone = gpd.sjoin(model_gdf, zones)

    buildings_by_zone.drop(columns=['index_right'], inplace=True)

    buildings_by_zone.insert(0, column='id', value=list(range(1, len(buildings_by_zone)+1)))

    return buildings_by_zone
