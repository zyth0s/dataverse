# coding: utf-8

from math import log
import copy
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import urllib.request, urllib.error

pd.set_option("display.width",2000)

# Import and prepare data

#base_url = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-"
base_url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
base_name = "COVID-19-geographic-disbtribution-worldwide-"
url   = base_url #[0:-1] + ".csv"
fname =  base_name[0:-1] + ".csv"
urllib.request.urlretrieve(url,fname)
#try:
#    url = base_url + dt.datetime.today().strftime("%Y-%m-%d") + ".csv"
#    fname =  base_name + dt.datetime.today().strftime("%Y-%m-%d") + ".csv"
#    urllib.request.urlretrieve(url,fname)
#except urllib.error.HTTPError as e:
#    url = base_url + dt.datetime.today().strftime("%Y-%m-%d") + "_0.csv"
#    fname = base_name + dt.datetime.today().strftime("%Y-%m-%d") + "_0.csv"
#    urllib.request.urlretrieve(url)

def parse_date(daterep,day,month,year):
    return dt.datetime.strptime(daterep,"%d/%m/%Y").date()

df = pd.read_csv(fname,
                parse_dates={"dates": ["dateRep","day","month","year"]},
                date_parser=parse_date,index_col="dates",
                engine = "python")

df.sort_index(inplace=True)

# Filtering
df_fl = df[df.geoId == "ES"]
country = df_fl["countriesAndTerritories"][0]

print("Total number of cases  in {:} = {:8d}; Population ratio = {:6.3f} / 1 000".format(
        country,df_fl.cases.sum(),
        df_fl.cases.sum()/df_fl.popData2018[-1]*1000
        ))
print("Total number of deaths in {:} = {:8d}; Population ratio = {:6.3f} / 1 000".format(
        country,df_fl.deaths.sum(),
        df_fl.deaths.sum()/df_fl.popData2018[-1]*1000
        ))
print("Confirmed Fatality Ratio (CFR) = {:6.3f} %".format(df_fl.deaths.sum()/df_fl.cases.sum()*100))
print("Doubling time (deaths) = {:} days".format(
        log(2)/log(df_fl.deaths.sum()/df_fl.deaths[:-1].sum())
     ))
print("Doubling time ( cases) = {:} days".format(
        log(2)/log(df_fl.cases.sum()/df_fl.cases[:-1].sum())
     ))

fig = plt.figure()
ax = fig.add_subplot(111) 
## Plot cases
#plt.title("Number of cases confirmed each day in " + country)
#x = df_fl.index[-15:]
#y = df_fl.cases[-15:]
## Plot deaths
plt.title("Number of deaths each day in " + country)
x = df_fl.index[-15:]
y = df_fl.deaths[-15:]

plt.bar(x,y)
plt.gcf().autofmt_xdate()

for xy in zip(x,y):
    ax.annotate('%s' % xy[1], xy=(xy[0],xy[1]), textcoords='data',ha="center")

plt.show()




#_dates = df_es.index
#_dates = [dt.datetime.strptime(d,"%d/%m/%Y").date() for d in df_es.DateRep]
#df_es["dates"] = _dates
#_dates.sort()
#df_es = df_es.assign(dates=[dt.datetime.strptime(d,"%d/%m/%Y").date() for d in df_es.DateRep])
#df_es = df_es.sort_values("dates")
#dates = copy.deepcopy(df_es.dates)
