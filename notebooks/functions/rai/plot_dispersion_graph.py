import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def plot_dispersion_graph(pop_1, pop_2, project, division_type='zone'):

    if division_type=='zone' :
        print('Obtaining model zones')
        df_1 = pop_1.groupby('zone_id').sum()[['accessible', 'inaccessible']].reset_index()
        df_1 = df_1.assign(wp_rai=df_1.accessible/(df_1.accessible+df_1.inaccessible))        
        df_2 = pop_2.groupby('zone_id').sum()[['accessible', 'inaccessible']].reset_index()
        df_2 = df_2.assign(meta_rai=df_2.accessible/(df_2.accessible+df_2.inaccessible))
        aux_dict = dict(zip(df_2.zone_id.tolist(), df_2.meta_rai.tolist()))
        df_1['meta_rai'] = df_1['zone_id'].apply(lambda x:aux_dict.get(x))

    elif division_type=='subdivision' :
        print('Obtaining country subdivisions')
        df_1 = pop_1.groupby('division_name').sum()[['accessible', 'inaccessible']].reset_index()
        df_1 = df_1.assign(wp_rai=df_1.accessible/(df_1.accessible+df_1.inaccessible))        
        df_2 = pop_2.groupby('division_name').sum()[['accessible', 'inaccessible']].reset_index()
        df_2 = df_2.assign(meta_rai=df_2.accessible/(df_2.accessible+df_2.inaccessible))
        aux_dict = dict(zip(df_2.division_name.tolist(), df_2.meta_rai.tolist()))
        df_1['meta_rai'] = df_1['division_name'].apply(lambda x:aux_dict.get(x))
    else:
        raise ValueError('Unknown division_type')
    
    df_1.plot.scatter('meta_rai', 'wp_rai')