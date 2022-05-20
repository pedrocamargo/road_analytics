import matplotlib.pyplot as plt

def quick_map(gdf, map_field, title='', path_to_figure=''):
    
    fig, ax = plt.subplots(figsize = (20,20))
    
    gdf.plot(map_field, ax=ax, legend=True)
    if title:
        ax.set_title(title)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    
    if path_to_figure:
        plt.savefig(path_to_figure, dpi=300)
        
    return ax