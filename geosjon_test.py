import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl
import numpy as np
import mapclassify
import seaborn as sns
import plotly.express as px
from urllib.request import urlopen
import json

geo_json = 'https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_BN_01M_2024_3857.geojson'
geo_json2= 'https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2024_3857_LEVL_3.geojson'
geo_json3 = 'https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2024_3857_LEVL_2.geojson'
geo_df = gpd.read_file(geo_json)
geo_df2 = gpd.read_file(geo_json2)
geo_df3 = gpd.read_file(geo_json3)

print(geo_df2.geom_type.value_counts())

geo_df2.plot(edgecolor="black", facecolor="grey")
plt.show()

pop_df = pd.read_excel('C:/Users/bczekus/Documents/Forecasts/nuts3_pop_density.xlsx')

df2022 = pop_df[pop_df["year"]==2022]
print(df2022.tail(10))
print(df2022["pop_density"].median())
df2022['log_density'] = np.log(df2022['pop_density'])

sns.histplot(df2022["pop_density"])
plt.grid(True)
plt.show()

sns.kdeplot(df2022["pop_density"], fill=True)
plt.show()

poly_data = geo_df2.merge(df2022, right_on="nuts3_id", left_on="NUTS_ID")

it = df2022[df2022['nuts3_id'].str.startswith('IT')]
poly_data_it = geo_df2.merge(it, right_on="nuts3_id", left_on="NUTS_ID", how="left")


#Plotting population density
poly_data.plot(
    column="pop_density", 
    edgecolor="grey", 
    legend=True, 
    cmap='magma_r', 
    scheme="quantiles", 
    k=10)
plt.show()

poly_data.plot(
    column="log_density", 
    edgecolor="grey", 
    legend=True, 
    cmap='magma_r',
    missing_kwds={
        "color": "lightgrey",
        "edgecolor": "red",
        "hatch": "///",
        "label": "Missing values",
    })
plt.show()

#Mapping just for Italy
poly_data_it.plot(
    column="pop_density", 
    edgecolor="grey", 
    legend=True, 
    cmap='OrRd',
    scheme="quantiles",
    k=10)
plt.show()

poly_data_it2 = poly_data_it.dropna()

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
poly_data_it.plot(
    column="pop_density",
    edgecolor="grey",
    legend=True,
    cmap='OrRd',
    scheme="quantiles",
    k=10,
    ax=ax
)

for id, row in poly_data_it.iterrows():
     if pd.notna(row['region_name']):
      centroid = row.geometry.centroid
      ax.text(centroid.x, centroid.y, row['region_name'], fontsize=7, ha='center',va='center')

plt.title("Population Density by Region")
plt.show()

#Plotly interactive choropleth maps
