# coding: utf-8

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pyjstat import pyjstat

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

# Main data set
dataset_code = "crim_hist"
query = dataset_code + "?precision=1&geoLevel=country"
# Read the data
DATA_URL="http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/{:}".format(query) 
jstatfile = dataset_code + ".jstat"

newdata = False
if os.path.exists(jstatfile) and not newdata:
    print("Retrieving data from {:}... ".format(jstatfile), end='')
    with open(jstatfile, "r") as f:
        dataset = pyjstat.Dataset.read(f.read())
    print("done.")
else:
    print("Retrieving data from {:}... ".format(DATA_URL), end='')
    dataset = pyjstat.Dataset.read(DATA_URL)
    with open(jstatfile, "w") as f:
        f.write(dataset.write())
    print("done.")

df = dataset.write('dataframe')
dfbck = df # backup

# Secondary data sets
## 
#dataset_code = "demo_r_d2jan"
#query = dataset_code + "?geoLevel=country&precision=1&sex=T&age=TOTAL"
## Read the data
#DATA_URL="http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/{:}".format(query) 
#jstatfile = dataset_code + ".jstat"
#
#if os.path.exists(jstatfile) and not newdata:
#    print("Retrieving data from {:}... ".format(jstatfile), end='')
#    with open(jstatfile, "r") as f:
#        dataset = pyjstat.Dataset.read(f.read())
#    print("done.")
#else:
#    print("Retrieving data from {:}... ".format(DATA_URL), end='')
#    dataset = pyjstat.Dataset.read(DATA_URL)
#    with open(jstatfile, "w") as f:
#        f.write(dataset.write())
#    print("done.")
#
#df2 = dataset.write('dataframe')
#df2bck = df # backup


#Prepare the data
df["time"] = df.time.astype('int64')

countries = set(df.geo) # Unique country set (not repeated)

# Filter 

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
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['xtick.major.width'] = 1
plt.rcParams['ytick.major.width'] = 1
plt.rcParams['ytick.major.pad'] = 0
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['legend.fontsize'] = 20
plt.rcParams['axes.titlesize'] = 24
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["font.weight"] = "bold"
plt.set_cmap("tab20c")
for spine in plt.gca().spines.values():
    spine.set_visible(False)
plt.box(False)
fig, ax = plt.subplots(7, 5, figsize=(12,12),sharey=True,sharex=True)
#ax.spines["top"].set_visible(False)
#ax.spines["right"].set_visible(False)
#ax.spines["bottom"].set_visible(False)
#ax.spines["left"].set_visible(False)

plt.suptitle("Police recorded crime",fontweight="bold")
num = 0
for country in countries:
    num += 1
    df_tmp = df[df.geo == country]
    df_tmp.sort_values(by=["time"])
    df_tmp = df_tmp[np.isfinite(df_tmp.value)]
    years = df_tmp.time
    #print(country,df2[(df2.time == years[0]) & (df2.geo == country)].value)
    #if "France" in country:
    #    if not "metropolitan" in country:
    #        continue
    col = num // 5 - 1
    row = num % 5 - 1
    ax[col][row].plot(years,df_tmp.value,label=country)
    ax[col][row].legend(frameon=False,fontsize=6,borderaxespad=0.)
#ax.set_ylabel("Offences per 100 000 inhabitants", labelpad=20)
#ax.set_xticks(year+bar_width-0.2)
#ax.set_xticklabels(year)
#ax.grid(which='major', color='w', linestyle='-',linewidth=2)
#ax.set_axisbelow(False)
#plt.legend(frameon=False,bbox_to_anchor=(1.00, 1),mode='expand',loc=1,fontsize=6,borderaxespad=0.)
#fig.tight_layout(w_pad=5)
#plt.show()
plt.savefig("hist_crime_EU.svg")
