import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
import matplotlib.lines as mlines

from functions.country_borders import get_country_borders

def plot_network(country_name:str, project):
    
    links = project.network.links.data
    links = links[links.modes.str.contains('c')]

    country_border = get_country_borders(country_name)

    geo_links = gpd.GeoDataFrame(links, geometry='geometry', crs=4326)

    geo_borders = gpd.GeoDataFrame(pd.DataFrame(country_border, columns=['geometry']),
                                   geometry='geometry', crs=4326)

    line_dict = {'motorway':3.3, 'trunk':2.5, 'primary':2.5, 'secondary':1.5}

    road_palette = {'motorway':"#8E1916", 'trunk':"#013a63", 
                    'primary':"#dd8024", 'secondary':"#40916c"}

    color_list = ["#52b788","#74c69d","#95d5b2","#b7e4c7","#89c2d9","#61a5c2","#468faf",
                  "#2a6f97", "#B8191B", "#d5ca7a", "#efb337"]

    for i in geo_links.link_type.unique().tolist(): #adicionar estrutura de controle
        if i not in line_dict:
            line_dict[i] = 0.9
            try:
                road_palette[i] = color_list.pop()
            except ValueError:
                road_palette[i] = 'darkgray'
        pass
    
    # Plot data
    fig, ax = plt.subplots(figsize=(20, 20))

    geo_borders.plot(figsize=(20,20), color='gainsboro', alpha=0.8, ax=ax, edgecolor='black', label='Country Borders', marker='s')

    for ctype, data in geo_links.groupby('link_type'):
        color = road_palette[ctype]
        label = ctype    
        data.plot(color=color,
                  ax=ax,
                  linewidth=line_dict[ctype], 
                  label=label,
                  marker='_')

    cx.add_basemap(ax, crs=4326, source=cx.providers.Stamen.TonerLite) 
    
    line = mlines.Line2D([], [], color='gainsboro', marker='s', markersize=14, label='Country Border', ls='None',
                         markeredgecolor='black', alpha=0.8)

    handles, _ = ax.get_legend_handles_labels()

    ax.legend(loc='best', fontsize=12, title=f"OSM Network Links", framealpha=1, title_fontsize=16, handles=[*handles, line])

    ax.set_axis_off()

    plt.show()