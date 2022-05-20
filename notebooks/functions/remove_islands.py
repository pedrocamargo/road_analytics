import geopandas as gpd

def remove_islands(all_states):
    
    no_island = all_states[all_states['ids'] == 0].copy()
    
    return no_island