import pandas as pd
import geopandas as gpd
import numpy as np
import sqlite3
import shapely.wkb

def open_states(project):
    
    state_wkb = [x[0] for x in project.conn.execute('Select asBinary(geometry) from state_borders')]
    num_states = project.conn.execute('Select COUNT(state_name) from state_borders;').fetchall()[0][0]
    states_names = [i[0] for i in project.conn.execute('SELECT state_name FROM state_borders;').fetchall()]
    state_geo, state_ = [[] for i in range(num_states)], [[] for i in range(num_states)]

    for i in range(num_states):
        state_geo[i] = shapely.wkb.loads(state_wkb[i])
        state_[i] = pd.DataFrame({'ids':np.arange(len(state_geo[i].geoms)), 'state':states_names[i], 
                                  'geometry':state_geo[i]})
        
    all_states = gpd.GeoDataFrame(pd.concat([state_[i] for i in range(num_states)], ignore_index=True))
    all_states.set_crs('epsg:4326', inplace=True);
    
    return all_states