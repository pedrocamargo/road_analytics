from tabulate import tabulate
import pandas as pd
import numpy as np

def bridge_stats(links):
    
    vehicle_links = links[(links["modes"].str.contains("c")) & (links["modes"].str.contains("t"))]
    bridge_links = vehicle_links[vehicle_links["bridge"].notna()]
    
    print("----- Bridge - Overall Stats -----")
    print(" ")
    table = [["Bridge", len(bridge_links), 
              np.around(bridge_links.sum(numeric_only=True)['distance'], decimals=2)],
             ["Total", len(vehicle_links), 
              np.around(vehicle_links.sum(numeric_only=True)['distance'], decimals=2)]]

    print(tabulate(table, headers=["", "Links", "km"], tablefmt='github', floatfmt=".2f"))
    print(" ")
    if len(bridge_links[bridge_links['toll'].notna()]) == 0:
        print(f"There are no toll bridges in the search area.")
        print("")
    else: 
        print(f"----- Toll Bridge -----")
        print(" ")
        bridge_bridges = bridge_links[bridge_links['toll'] == 'yes']
        table = [[len(bridge_bridges),
                  bridge_bridges.sum(numeric_only=True)['distance']/1000]]

        print(tabulate(table, headers=['links', 'km'], tablefmt='github', floatfmt=".2f"))
        print("")
    
    print("----- Bridge - Link Type -----")
    print("")
    df = pd.DataFrame.from_dict(dict(bridge_links.groupby('link_type').sum(numeric_only=True)['distance']/1000),
                            orient='index', columns=['total_km'])
    df.insert(0, 'links', bridge_links.groupby('link_type').count()['distance'])
    print(tabulate(df, tablefmt="github", floatfmt=(".0f", ".0f", ".2f"), 
                   headers=["Link Type", "Links", 'km']))
    print("")
    
    print("----- Bridge - Pavement Surface -----")
    print("")
    bridge_links.loc[bridge_links['surface'].isna(), 'surface'] = 'unclassified'
    df = pd.DataFrame.from_dict(dict(bridge_links.groupby('surface').sum(numeric_only=True)['distance']/1000),
                            orient='index', columns=['total_km'])
    df.insert(0, 'links', bridge_links.groupby('surface').count()['distance'])
    print(tabulate(df, tablefmt="github", floatfmt=(".0f", ".0f", ".2f"), 
                   headers=["Surface Type", "Links", 'km']))
    print("")