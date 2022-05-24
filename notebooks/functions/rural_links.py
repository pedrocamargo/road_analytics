import geopandas as gpd

def links_in_rural_areas(project, rural_areas):
    
    links = project.network.links.data
    links = links[links.modes.str.contains('c')]
    
    geo_links = gpd.GeoDataFrame(links, geometry='geometry')
    
    rural_links = gpd.sjoin(geo_links, rural_areas)[['ogc_fid', 'geometry']]
    
    return rural_links