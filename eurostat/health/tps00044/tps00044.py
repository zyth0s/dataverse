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

dataset_code = "tps00044"
query = dataset_code + "?precision=1&isco08=OC221&geo=DE&geo=ES&geo=FR&geo=IT&unit=P_HTHAB&wstatus=PRACT"
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
dfbck = df.copy() # backup

#Prepare the data
df["time"] = df.time.astype('int64')

countries = list(set(df.geo))

# Filter 
#df = df[df.unit.str.contains("Number")]
#df = df[df.iccs.str.contains("Intentional homicide")]
#df_DE = df[df.geo.str.contains("Germany")]
#df_ES = df[df.geo.str.contains("Spain")]

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


plt.suptitle("Practising physicians in EU countries hit by COVID-19",fontsize=24,fontweight="bold")
plt.title("Physicians per 100 000 inhabitants",y=0.91)
years = df.query("geo == 'Spain'").time
total = np.zeros(len(years),dtype='float64')
for country in countries:
    df_tmp = df[df.geo == country]
    # Methodology for missing data
    for i,value in enumerate(df_tmp.value):
        df_tmp.value.iat[i] = 0
        #if not np.isfinite(value):
        #    if i == 0:
        #        if np.isfinite(df_tmp.value.iat[i+1]):
        #            df_tmp.value.iat[i] = df_tmp.value.iat[i+1]
        #        else:
        #            print("Error")
        #    else:
        #        if np.isfinite(df_tmp.value.iat[i-1]):
        #            df_tmp.value.iat[i] = df_tmp.value.iat[i-1]
        #        else:
        #            print("Error")
    total += df_tmp.value.values

total = total/len(countries)
#ax.plot(years,total,color="#990000",marker='o')
for country in countries:
    ax.plot(years,df[df.geo == country].value.values,marker='o',label="{:7s}".format(country[0:7]))

#ax.set_ylabel("Offenses per 100 000 inhabitants")
#ax.set_xticks(year+bar_width-0.2)
#ax.set_xticklabels(year)
#ax.set_axisbelow(False)
#ax.set_ylim(ymin=0.0)
ax.set_xlim(years.min()-0.1,years.max()+0.1)
ax.tick_params(axis='x',pad=10)
plt.figtext(0.99, 0.01, 'Source: Eurostat ({:})'.format(dataset_code), horizontalalignment='right',fontsize=12)
plt.legend(fontsize="xx-large",bbox_to_anchor=(0.95, 0.4))
#plt.legend(frameon=False,bbox_to_anchor=(1.00, 1),mode='expand',loc=1,borderaxespad=0.)
fig.tight_layout(pad=2.55)
#plt.show()
plt.savefig("practising_physicians.svg")
