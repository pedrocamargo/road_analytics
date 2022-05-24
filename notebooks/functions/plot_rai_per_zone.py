import geopandas as gpd
import pandas as pd

from functions.rai_per_zone import rai_per_zone
from functions.load_zones import load_zones


def plot_rai_per_zone(project, rural_population):
    
    zones = load_zones(project)
    
    rai_zones = rai_per_zone(rural_population)
    
    zones['RAI'] = zones['zone_id'].apply(lambda x: rai_zones.get(x))
    
    zones = zones.fillna(value=0)
    
    zones.plot(figsize=(10,8), cmap='Greens', column='RAI', edgecolor='black',
               legend=True, linewidth=0.1)

