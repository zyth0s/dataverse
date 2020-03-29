# coding: utf-8

# Source: https://apps.who.int/gho/data/node.main.HWFGRP_0040?lang=en

countries = ["Spain", "Germany", "Italy", "France"]

import json

with open("data.json","r") as f:
    data = json.load(f)
    
                
nurses_dict = {}
for country in countries:
    nurses_dict[ country ] = {"years": [], "values": [] }
    for i,dat in enumerate(data["fact"]):
        if dat["dims"]["COUNTRY"] == country:
            if "10 000" in dat["dims"]["GHO"]: # interested in per 10 000 data
                year = int(data["fact"][i]["dims"]["YEAR"])
                nurses_midwives_ph = float(data["fact"][i]["Value"])
                nurses_dict[country]["years"].append(year)
                nurses_dict[country]["values"].append(nurses_midwives_ph)
            

import matplotlib.pyplot as plt
import matplotlib as mpl

def set_size(width, fraction=1,units="mm"):
    """ Set aesthetic figure dimensions to avoid scaling in the final document.

    Parameters
    ----------
    width: float Width in xx
    fraction: float
            Fraction of the width which you wish the figure to occupy

    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    # Width of figure
    fig_width_xx = width * fraction

    # Convert from xx to inches
    #inches_per_pt = 1 / 72.27
    # Convert from xx to inches
    inches_per_xx = 0.03937007874015748
    if units == "mm":
        inches_per_xx = 0.03937007874015748
    else:
        inches_per_xx = 1.0
    # Golden ratio to set aesthetic figure height
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_xx * inches_per_xx
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio

    fig_dim = (fig_width_in, fig_height_in)

    return fig_dim

# Plot
#width = 345
figsize = 'l'
if figsize == 's':
    width = 3.5 # in single column size ACS
    #width = 90 # mm Small column size Elsevier
elif figsize == 'm':
    width = 7   # in double column width ACS
    #width = 140 # mm Full page width Elsevier
elif figsize == 'l':
    width = 9.5 # in Full page width ACS
    #width = 190 # mm Half page width Elsevier
#plt.style.use("seaborn")

plt.rcParams['lines.linewidth'] = 3
plt.rcParams['lines.markersize'] = 10
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.major.width'] = 1
plt.rcParams['ytick.major.width'] = 1
plt.rcParams['xtick.major.size'] = 0
plt.rcParams['ytick.major.size'] = 0
plt.rcParams['ytick.major.pad'] = 5
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['text.color'] = "#222222"
plt.rcParams['xtick.color'] = "#222222"
plt.rcParams['ytick.color'] = "#222222"
plt.rcParams['axes.labelcolor'] = "#222222"
plt.rcParams['grid.color'] = "#cbcbcb"
#plt.rcParams["axes.labelweight"] = "bold"
#plt.rcParams["font.weight"] = "bold"
plt.rcParams['image.cmap'] = 'tab20b'
#colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
#colors = set(plt.get_cmap("tab20c"))
mpl.rcParams['font.family'] = 'Montserrat'

#for spine in plt.gca().spines.values():
#    spine.set_visible(False)
#plt.box(False)
fig, ax = plt.subplots(1, 1, figsize=set_size(width,units="in"))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.grid(axis='y',linestyle='-') #which='major', color='k', linestyle='-',linewidth=2)


plt.suptitle("Nurses and midwives in EU countries hit by COVID-19",fontsize=24,fontweight="bold")
plt.title("Personnel per 10 000 inhabitants",y=0.90)
for country in countries:
    ax.plot(nurses_dict[country]["years"],nurses_dict[country]["values"],marker='o',label=country)

#ax.set_ylabel("Offenses per 100 000 inhabitants")
#ax.set_xticks(year+bar_width-0.2)
#ax.set_xticklabels(year)
#ax.set_axisbelow(False)
#ax.set_ylim(ymin=0.0)
ax.set_xlim(1989-0.1,2018+0.1)
ax.set_ylim(35,159)
ax.tick_params(axis='x',pad=10)
plt.figtext(0.99, 0.01, 'Source: WHO', horizontalalignment='right',fontsize=12)
plt.legend(loc=6,fontsize="xx-large")
#plt.legend(frameon=False,bbox_to_anchor=(1.00, 1),mode='expand',loc=1,borderaxespad=0.)
fig.tight_layout(pad=2.55)
#plt.show()
plt.savefig("nursering_midwivery_personnel.svg")
