import pandas as pd

def rai_per_zone(hex_buffer_and_zones):
    
    rural_filter = hex_buffer_and_zones[hex_buffer_and_zones.is_urban == 0]
    
    in_rai = rural_filter[rural_filter.ogc_fid.notna()].groupby(['zone_id']).sum()['population'].tolist()
    
    all_rural = rural_filter.groupby(['zone_id']).sum()['population'].tolist()
    
    rai_zone = []
    
    for i in range(len(in_rai)):
        try:
            rai_zone.append(round((in_rai[i]/all_rural[i])*100, 2))
            
        except ZeroDivisionError:
            rai_zone.append(0)
    
    dict_zones = dict(zip(rural_filter.groupby('zone_id').count().index.tolist(),
                                 rai_zone))
    return dict_zones