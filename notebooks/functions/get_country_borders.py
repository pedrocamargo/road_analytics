import geopandas as gpd

def country_borders(file):
    
    country = file[file['ids'] == 0].copy().dissolve(by='ids')
    
    return country