from tabulate import tabulate
import pandas as pd
import numpy as np

def toll_stats(links):
    
    vehicle_links = links[(links["modes"].str.contains("c")) & (links["modes"].str.contains("t"))]
    toll_links = vehicle_links[vehicle_links["toll"].notna()]
    
    if len(toll_links.toll.value_counts()) != 0:
        print("----- Tolls - Overall Statistics -----")
        print(" ")
        table = [["Tolls", len(toll_links), 
                  np.around(toll_links.sum(numeric_only=True)['distance']/1000, decimals=2)],
                 ["Total", len(vehicle_links), 
                  np.around(vehicle_links.sum(numeric_only=True)['distance']/1000, decimals=2)]]

        print(tabulate(table, headers=["", "Links", "km"], tablefmt='github', floatfmt=".2f"))
        print(" ")

        print("----- Tolls - Link Type -----")
        print("")
        df = pd.DataFrame.from_dict(dict(toll_links.groupby('link_type').sum(numeric_only=True)['distance']/1000),
                                orient='index', columns=['km'])
        df.insert(0, 'links', toll_links.groupby('link_type').count()['distance'])
        print(tabulate(df, tablefmt="github", floatfmt=(".0f", ".0f", ".2f"), 
                       headers=["Link Type", "Links", 'km']))
        print("")

        print("----- Tolls - Pavement Surfaces -----")
        print("")
        toll_links.loc[toll_links['surface'].isna(), 'surface'] = 'unclassified'
        df = pd.DataFrame.from_dict(dict(toll_links.groupby('surface').sum(numeric_only=True)['distance']/1000),
                                orient='index', columns=['km'])
        df.insert(0, 'links', toll_links.groupby('surface').count()['distance'])

        print(tabulate(df, tablefmt="github", floatfmt=(".0f", ".0f", ".2f"), 
                       headers=["Surface Type", "Links", 'km']))
        print("")
        
    else:
        if type(model_place) == str:
            print(f"There are no tolls in {model_place}.")
        else:
            print(f"There are no tolls in the search area.")
    print("")
            