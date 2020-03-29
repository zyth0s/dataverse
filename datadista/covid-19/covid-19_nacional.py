# coding: utf-8

import copy
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import urllib.request, urllib.error
import numpy as np

pd.set_option("display.width",2000)

# Import and prepare data

url = "https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/nacional_covid19.csv"
base_name = "COVID-19-nacional"
fname =  base_name + ".csv"
urllib.request.urlretrieve(url,fname)
#try:
#    url = base_url + dt.datetime.today().strftime("%Y-%m-%d") + ".csv"
#    fname =  base_name + dt.datetime.today().strftime("%Y-%m-%d") + ".csv"
#    urllib.request.urlretrieve(url,fname)
#except urllib.error.HTTPError as e:
#    url = base_url + dt.datetime.today().strftime("%Y-%m-%d") + "_0.csv"
#    fname = base_name + dt.datetime.today().strftime("%Y-%m-%d") + "_0.csv"
#    urllib.request.urlretrieve(url)

def parse_date(fecha):
    return dt.datetime.strptime(fecha,"%Y-%m-%d").date()

df = pd.read_csv(fname,
                parse_dates={"dates": ["fecha"]},
                date_parser=parse_date,index_col="dates")

df.sort_index(inplace=True)


print("Total number of cases  = {:}".format(df.casos[-1]))
print("Total number of deaths = {:}".format(df.fallecimientos[-1]))
print("CFR = {:6.3f} %".format(df.fallecimientos[-1]/df.casos[-1]*100))

#fig = plt.figure()
#ax = fig.add_subplot(112) 
fig, ax = plt.subplots(4,1)
fig.suptitle("COVID-19 Spain Dashboard")
x = df.index[-15:]
## Plot cases
#plt.title("Number of cases confirmed each day in " + country)
#x = df_fl.index[-15:]
#y = df_fl.cases[-15:]
## Plot deaths
y = df.fallecimientos[-15:]
ax[0].set_title("(cumulative) deaths in Spain",y=0.8)
ax[0].bar(x,y,color="r")
for xy in zip(x,y):
    ax[0].annotate('%s' % int(xy[1]), xy=xy, textcoords='data',ha="center")
## Plot UCI patients
y = df.ingresos_uci[-15:]
ax[1].set_title("UCI (cumulative) patients in Spain",y=0.8)
ax[1].bar(x,y,color="brown")
for xy in zip(x,y):
    ax[1].annotate('%s' % int(xy[1]), xy=xy, textcoords='data',ha="center")
## Plot hospitalized patients 
y = df.hospitalizados[-15:]
ax[2].set_title("(cumulative) hospitalized patients in Spain",y=0.8)
ax[2].bar(x,y,color="orange")
for xy in zip(x,y):
    ax[2].annotate('%s' % xy[1], xy=xy, textcoords='data',ha="center")
## Plot curated patients
y = df.altas[-15:]
ax[3].set_title("(cumulative) curated patients in Spain",y=0.8)
ax[3].bar(x,y,color="g")
for xy in zip(x,y):
    ax[3].annotate('%s' % int(xy[1]), xy=xy, textcoords='data',ha="center")

#plt.gcf().autofmt_xdate()


for ax in fig.get_axes():
    ax.label_outer()

plt.show()

