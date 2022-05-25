import pandas as pd

def rai_per_subdivision(rural_population):
    
    rural_filter = rural_population[rural_population.is_urban == 0]
    
    in_rai = rural_filter[rural_filter.ogc_fid.notna()].groupby(['country_subdivision']).sum()['population'].tolist()
    
    all_rural = rural_filter.groupby(['country_subdivision']).sum()['population'].tolist()
    
    rai_subdivision = []
    
    for i in range(len(in_rai)):
        try:
            rai_subdivision.append(round((in_rai[i]/all_rural[i])*100, 2))
            
        except ZeroDivisionError:
            rai_subdivision.append(0)
    
    dict_subdivisions = dict(zip(rural_filter.groupby('country_subdivision').count().index.tolist(),
                                 rai_subdivision))
    return dict_subdivisions
