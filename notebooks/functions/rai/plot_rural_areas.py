import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib import colors as mcolors

def plot_rural_areas(rural_areas):
    
    fig, ax = plt.subplots(constrained_layout=False, frameon=False, figsize=(20,20))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    
    
    rural_areas.plot(ax=ax, color='#5f8065', linewidth=0.4, edgecolor='black')

    line0 = mlines.Line2D([], [], color='black', marker='',
                                  markersize=10, label='LEGEND', ls='None')
    line1 = mlines.Line2D([], [], color='#5f8065', marker='s',
                                      markersize=10, label='Rural Area', ls='None', alpha=1)
    line2 = mlines.Line2D([], [], color='white', marker='s', markeredgecolor='black',
                                      markersize=10, label='Urban Area', ls='None', alpha=1)

    ax.legend(fontsize=12, loc='lower left', handles=[line0, line1, line2], frameon=False)
    