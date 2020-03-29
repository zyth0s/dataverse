
# coding: utf-8

# In[1]:


import os
import folium
import pandas as pd
from pyjstat import pyjstat


# In[2]:


m = folium.Map(location=[51.0295293,13.6980529], tiles='Mapbox Bright',zoom_start=4)


# In[3]:


import urllib.request, json 
# For some reason, folium is only able to read 4326 projected geojson
URL_GEOJSON = "https://ec.europa.eu/eurostat/cache/GISCO/distribution/v2/nuts/geojson/NUTS_RG_20M_2006_4326_LEVL_0.geojson"
#URL_GEOJSON = "https://raw.githubusercontent.com/eurostat/Nuts2json/gh-pages/2016/4258/20M/nutsbn_1.json"
with urllib.request.urlopen(URL_GEOJSON) as url:
    geo_json_data = json.loads(url.read().decode())

#geo_json_data = json.load(open("NUTS_RG_60M_2013_3035_LEVL_1.geojson"))
#geo_json_data = json.load(open("NUTS_RG_60M_2013_4326_LEVL_0.geojson"))

#geo_json_data = json.load(open("nuts_rg_60m_2013_lvl_1.geojson"))
#print(json.dumps(geo_json_data, indent=2))


# In[4]:


folium.GeoJson(geo_json_data).add_to(m)
#m


# In[5]:


dataset_code = "crim_hist"
query = dataset_code + "?precision=1&time=1989&geoLevel=country"
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


# In[6]:


# Filters
#df = df[df.iccs.str.contains("Sexual violence")]


# In[7]:


nuts_name = dataset["dimension"]["geo"]["category"]["label"]
name_nuts = {v: k for k, v in nuts_name.items()}


# In[8]:


cntry_codes = []
for i in df.geo:
    cntry_codes.append(name_nuts[i])

df["cntry"] = cntry_codes


# In[9]:


#df.head(30)


# In[10]:


folium.Choropleth(
    geo_data=geo_json_data,
    name='crim_hist',
    data=df,
    columns=['cntry','value'],
    key_on='feature.id',
    fill_color='YlOrRd',
    fill_opacity=0.9,
    line_opacity=0.1,
    legend_name='Number of crimes in 1989 by country',
).add_to(m)

folium.LayerControl().add_to(m)


# In[11]:


m


# In[12]:


m.save("index.html")

