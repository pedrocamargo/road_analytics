from tabulate import tabulate
import pandas as pd

def basic_stats(links):
    
    vehicle_links = links[(links["modes"].str.contains("c")) & (links["modes"].str.contains("t"))]
    
    print("----- Links -----")
    print("")
    bridge_links = len(vehicle_links[vehicle_links['bridge'].notna()])
    toll_links = len(vehicle_links[vehicle_links['toll'].notna()])
    tunnel_links = len(vehicle_links[vehicle_links['tunnel'].notna()])
    total_links = len(vehicle_links)
    
    table = [[total_links - bridge_links - toll_links - tunnel_links, bridge_links, toll_links, tunnel_links, total_links]]
    
    print(tabulate(table, headers=["General", "Bridge", "Toll", "Tunnel", "Total"], tablefmt="github", floatfmt=".0f"))
    print("")

    print("----- Total km -----")
    print("")
    bridge_dist = vehicle_links[vehicle_links['bridge'].notna()]['distance'].sum()/1000
    toll_dist = vehicle_links[vehicle_links['toll'].notna()]['distance'].sum()/1000
    tunnel_dist = vehicle_links[vehicle_links['tunnel'].notna()]['distance'].sum()/1000
    total_dist = vehicle_links.distance.sum()/1000
    
    table = [[total_dist - bridge_dist - toll_dist - tunnel_dist,
              bridge_dist, toll_dist, tunnel_dist, total_dist]]
    print(tabulate(table, headers=["General", "Bridge", "Toll", "Tunnel", "Total"], tablefmt="github", floatfmt=".2f"))
    print("")
    
    print("----- Link Type -----")
    print("")
    df = pd.DataFrame.from_dict(dict(vehicle_links.groupby('link_type').sum(numeric_only=True)['distance']/1000),
                            orient='index', columns=['total_km'])
    df.insert(0, 'links', vehicle_links.groupby('link_type').count()['distance'])

    print(tabulate(df, tablefmt="github", floatfmt=(".0f", ".0f", ".2f"), 
                   headers=["Link Type", "Links", 'km']))
    print("")
    
    print("----- Pavement Surfaces -----")
    print("")
    vehicle_links.loc[vehicle_links['surface'].isna(), 'surface'] = 'unclassified'
    df = pd.DataFrame.from_dict(dict(vehicle_links.groupby('surface').sum(numeric_only=True)['distance']/1000),
                            orient='index', columns=['total_km'])
    df.insert(0, 'links', vehicle_links.groupby('surface').count()['distance'])

    print(tabulate(df, tablefmt="github", floatfmt=(".0f", ".0f", ".2f"), 
                   headers=["Surface Type", "Links", 'km']))
    print("")