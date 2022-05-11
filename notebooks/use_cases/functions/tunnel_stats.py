from tabulate import tabulate
import pandas as pd
import numpy as np

def tunnel_stats(links):
    
    vehicle_links = links[(links["modes"].str.contains("c")) & (links["modes"].str.contains("t"))]
    tunnel_links = vehicle_links[vehicle_links["tunnel"].notna()]
    
    print("----- Tunnels - Overall stats -----")
    print(" ")
    table = [["Tunnels", len(tunnel_links), 
              np.around(tunnel_links.sum(numeric_only=True)['distance']/1000, decimals=2)],
             ["Total", len(vehicle_links), 
              np.around(vehicle_links.sum(numeric_only=True)['distance']/1000, decimals=2)]]

    print(tabulate(table, headers=["", "Links", "km"], tablefmt='github', floatfmt=".2f"))
    print(" ")
    
    if len(tunnel_links.tunnel.value_counts()) == 0:
        print(f"There are no toll tunnels in the search area.")
        print("")
    else: 
        print(f"----- Toll tunnels -----")
        print(" ")
        toll_tunnels = tunnel_links[tunnel_links['toll'] == 'yes']
        table = [[len(toll_tunnels),
                  toll_tunnels.sum(numeric_only=True)['distance']/1000]]

        print(tabulate(table, headers=['links', 'total_km'], tablefmt='github', floatfmt=(".0f", ".2f")))
        print("")
        
    print("----- Tunnels - Link Type -----")
    print("")
    df = pd.DataFrame.from_dict(dict(tunnel_links.groupby('link_type').sum(numeric_only=True)['distance']/1000),
                            orient='index', columns=['total_km'])
    df.insert(0, 'links', tunnel_links.groupby('link_type').count()['distance'])

    print(tabulate(df, tablefmt="github", floatfmt=(".0f", ".0f",".2f"), 
                   headers=["Link Type", "Links", 'Total km']))
    print("")
    
    print("----- Tunnels - Pavement Surfaces -----")
    print("")
    tunnel_links.loc[tunnel_links['surface'].isna(), 'surface'] = 'unclassified'
    df = pd.DataFrame.from_dict(dict(tunnel_links.groupby('surface').sum(numeric_only=True)['distance']/1000),
                            orient='index', columns=['total_km'])
    df.insert(0, 'links', tunnel_links.groupby('surface').count()['distance'])

    print(tabulate(df, tablefmt="github", floatfmt=(".0f", ".0f", ".2f"), 
                   headers=["Surface Type", "Links", 'Total km']))
    print("")