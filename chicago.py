import pandas as pd
import folium
from folium import plugins
import string
import matplotlib.pyplot as plt
from geopy.distance import vincenty


df=pd.read_csv("D:\Documents\PythonProjects\ChicagoCrime\Chicago_Crimes_2012_to_2017.csv")
chi_coordinates=(41.8781,-87.6298)  # Chicago coordinates for the map to start at
df.Latitude=pd.to_numeric(df.Latitude)
df.Longitude=pd.to_numeric(df.Longitude)
ps=pd.read_csv("D:\Documents\PythonProjects\ChicagoCrime\Police_Stations_map.csv")
result=ps.join(ps['LOCATION'].str.strip('()')                               \
                   .str.split(', ', expand=True)                   \
                   .rename(columns={0:'Latitude', 1:'Longitude'}))                 \
##result.Latitude=pd.to_numeric(result.Latitude)
##result.Longitude=pd.to_numeric(result.Longitude)                   
tcrime=df[df["Arrest"]==True]#Where an arrest has occured 
s=tcrime
s=s.dropna()
chimap = folium.Map(location=[41.8781,-87.6298], zoom_start=10)
for i, row in ps.iterrows():
	    folium.Marker(
	        location = [result['Latitude'][i],result['Longitude'][i]],popup=ps['DISTRICT'][i]
	        ).add_to(chimap)

##folium.Marker([41.858373, -87.627356], popup='Mt. Hood Meadows').add_to(chimap)
##folium.Marker([41.801811, -87.630560], popup='Timberline Lodge').add_to(chimap)
chimap.add_children(plugins.HeatMap(zip(s.Latitude, s.Longitude), radius = 10))
chimap.save('chi_crime.html')

def closest_station(pt, others):
    dd=min(others, key = lambda i: vincenty(pt, i).miles)
    return vincenty(pt, dd).miles
dist=[]
for i, row in s.iterrows():
    dist.append(closest_station((s["Latitude"][i],s["Longitude"][i]),
                                zip(result['Latitude'],result['Longitude'])))

s["Closest_Station"]=dist
    


"""""
Source
"""""

prim_type=tcrime["Primary Type"].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Type', fontsize=15, rotation=45)
ax.set_ylabel('Number of Type' , fontsize=15)
ax.set_title('Types of Crime', fontsize=15, fontweight='bold')
prim_type[:len(prim_type)].plot(ax=ax, kind='bar', color='blue')
plt.show()
