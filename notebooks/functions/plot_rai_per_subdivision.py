import geopandas as gpd
import pandas as pd

from functions.rai_per_subdivision import rai_per_subdivision
from functions.country_subdivisions import get_subdivisions

def plot_rai_per_subdivision(model_place, rural_population):
    
    divisions = get_subdivisions(model_place)
    
    rai_subdivision = rai_per_subdivision(rural_population)
    
    divisions['RAI'] = divisions['name'].apply(lambda x: rai_subdivision.get(x))
    
    divisions = divisions.fillna(value=0)
    
    divisions.plot(figsize=(10,8), cmap='Greens', column='RAI', edgecolor='black',
                   legend=True, linewidth=0.5)

