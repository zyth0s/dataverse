# coding: utf-8

from math import log
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


print("Doubling time (deaths) = {:} days".format(
        log(2)/log(df.fallecimientos[-1]/df.fallecimientos[-2])
     ))
print("Doubling time (cases) = {:} days".format(
        log(2)/log(df.casos[-1]/df.casos[-2])
     ))


#Plot
fig, ax = plt.subplots(2,1)
fig.suptitle("COVID-19 Spain Growth Rate")
x = df.index[-15:]

y = df.fallecimientos[-15:]
ax[0].set_title("(cumulative) deaths in Spain",y=0.8)
ax[0].plot(x,y,color="r",marker='.',label="Deaths")
double2days = [df.fallecimientos[-3]*2**(i/2) for i in range(3)]
double3days = [df.fallecimientos[-3]*2**(i/3) for i in range(3)]
double5days = [df.fallecimientos[-3]*2**(i/5) for i in range(3)]
ax[0].plot(df.index[-3:],double2days,label="Doubles every 2 days")
ax[0].plot(df.index[-3:],double3days,label="Doubles every 3 days")
ax[0].plot(df.index[-3:],double5days,label="Doubles every 5 days")
ax[0].set_yscale("log")

y = df.casos[-15:]
ax[1].set_title("(cumulative) cases in Spain",y=0.8)
ax[1].plot(x,y,color="k",marker='.',label="Confirmed cases")
double2days = [df.casos[-3]*2**(i/2) for i in range(3)]
double3days = [df.casos[-3]*2**(i/3) for i in range(3)]
double5days = [df.casos[-3]*2**(i/5) for i in range(3)]
ax[1].plot(df.index[-3:],double2days,label="Doubles every 2 days")
ax[1].plot(df.index[-3:],double3days,label="Doubles every 3 days")
ax[1].plot(df.index[-3:],double5days,label="Doubles every 5 days")
ax[1].set_yscale("log")

#plt.gcf().autofmt_xdate()
plt.legend()


for ax in fig.get_axes():
    ax.label_outer()

plt.show()

