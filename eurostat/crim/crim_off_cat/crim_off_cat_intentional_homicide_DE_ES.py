# coding: utf-8

import os
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib as mpl
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

dataset_code = "crim_off_cat"
query = dataset_code + "?precision=1&unit=P_HTHAB"
# Read the data
DATA_URL="http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/{:}".format(query) 
jstatfile = dataset_code + ".jstat"

newdata = True
if os.path.exists(jstatfile) and not newdata:
    print("Data retrieved from {:}.".format(jstatfile))
    with open(jstatfile, "r") as f:
        dataset = pyjstat.Dataset.read(f.read())
else:
    dataset = pyjstat.Dataset.read(DATA_URL)
    with open(jstatfile, "w") as f:
        f.write(dataset.write())

df = dataset.write('dataframe')
dfbck = df # backup

#Prepare the data
df["time"] = df.time.astype('int64')

# Filter 
#df = df[df.unit.str.contains("Number")]
df = df[df.iccs.str.contains("Intentional homicide")]
df_DE = df[df.geo.str.contains("Germany")]
df_ES = df[df.geo.str.contains("Spain")]

# Plot
#df_DE.plot.bar('time','value',ax=plt.subplot(121),color="k",label="Germany")
#df_ES.plot.bar('time','value',ax=plt.subplot(122),color="k",label="Spain")
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
plt.rcParams['xtick.major.width'] = 0
plt.rcParams['ytick.major.width'] = 0
plt.rcParams['ytick.major.pad'] = -20
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['legend.fontsize'] = 20
plt.rcParams['axes.titlesize'] = 24
#plt.rcParams["axes.labelweight"] = "bold"
#plt.rcParams["font.weight"] = "bold"
for spine in plt.gca().spines.values():
    spine.set_visible(False)
plt.box(False)
fig, ax = plt.subplots(1, 1, figsize=set_size(width,units="in"))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)

bar_width = 0.40
plt.title("Intentional homicide",fontweight="bold")
year = df_DE.time
ax.bar(year,df_DE.value,width=bar_width-0.1,color='k',label="Germany")
ax.bar(year+bar_width,df_ES.value,width=bar_width-0.1,color='r',label="Spain")
ax.set_ylabel("Offences per 100 000 inhabitants", labelpad=20)
ax.set_xticks(year+bar_width-0.2)
ax.set_xticklabels(year)
ax.grid(which='major', color='w', linestyle='-',linewidth=2)
ax.set_axisbelow(False)
ax.set_ylim(0,1.3)
ax.legend(frameon=False)
fig.tight_layout()
#plt.show()
plt.savefig("crim_off_cat_intentional_homicide_DE_ES.svg")
