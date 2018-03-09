
# coding: utf-8

# In[1]:


# Three Observable Trends
# 1. The temperature increases as you approach the equator with peaks at -20 degrees and 20 degrees.
# 2. Just below the equator from 0 to -20 there no points with low humidity suggesting this is a very humid region. 
# 3. Cloudiness doesn't seem to have much relationship to latitude. Almost all latitudes had points with various levels of cloudiness. 


# In[2]:


# Import dependencies and set keys
import requests
import pandas as pd
import matplotlib.pyplot as plt
from citipy import citipy
import seaborn as sns
import random
import numpy as np

url = "api.openweathermap.org/data/2.5/weather?"
api_key = "1554a148a00535035214c4ce3c74a8c7"
units = "metric"


# In[3]:


#Import the global cities csv, make a dataframe, and take a random sampling.
worldcities_df = pd.read_csv("worldcities.csv")
worldcities_df.head()
random_sample_df = worldcities_df.sample(n=500)
random_sample_df


# In[4]:


# Define Lists
temp = []
humidity = []
wind = []
cloudiness = []
open_weather_city_number = []
process_number = 0

# Query the API with Coordinates and create lists with Temperature, Humidity, Wind Speed, and Cloudiness Info.

for index, row in random_sample_df.iterrows():
    lat = row["Latitude"]
    lon = row["Longitude"]
    query = f"http://{url}APPID={api_key}&lat={lat}&lon={lon}&units={units}"
    response = requests.get(query).json()
    temp.append(response['main']['temp'])
    humidity.append(response['main']['humidity'])
    wind.append(response['wind']['speed'])
    cloudiness.append(response['clouds']['all'])
    open_weather_city_number.append(response['id'])
    process_number = process_number + 1
    print(f"{process_number}: Currently processing the city with the following information:")
    print(f"City ID Number: {response['id']}")
    print(f"City Name: {row.City}")
    print(f"Query url: {query}")


# In[5]:


random_sample_df["Current Temperature"] = temp
random_sample_df["Current Humidity"] = humidity
random_sample_df["Current Wind Speed"] = wind
random_sample_df["Current Cloudiness"] = cloudiness
random_sample_df.head()


# In[6]:


# Add the OpenWeatherMap City numbers to the dataframe. 
random_sample_df['OpenWeatherMap City Number'] = open_weather_city_number
random_sample_df.head()


# In[7]:


#Temperature Vs Latitude
sns.set()
plt.scatter(random_sample_df["Latitude"], random_sample_df["Current Temperature"])
plt.title("Temperature VS. Latitude")
plt.xlabel("Latitude")
plt.ylabel("Temperature")
plt.xlim(-80,100)
plt.ylim(-40, 50)
plt.savefig("temp_vs_lat.png")
plt.show()


# In[8]:


#Humidity % VS Latitude
plt.scatter(random_sample_df["Latitude"], random_sample_df["Current Humidity"])
plt.title("Humidity VS. Latitude")
plt.xlabel("Latitude")
plt.ylabel("Percentage Humidity")
plt.xlim(-80,100)
plt.ylim(-20, 120)
plt.savefig("humidity_vs_lat.png")
plt.show()


# In[9]:


# Cloudiness % VS Latitude
plt.scatter(random_sample_df["Latitude"], random_sample_df["Current Cloudiness"], s=15)
plt.title("Percent Cloudiness vs Latitude")
plt.xlabel("Latitude")
plt.ylabel("% Cloudiness")
plt.xlim(-60,80)
plt.ylim(-20,120)
plt.savefig("cloudiness_vs_lat")
plt.show()


# In[10]:


#Wind Speed VS Latitude
plt.scatter(random_sample_df["Latitude"], random_sample_df["Current Wind Speed"])
plt.title("Wind Speed vs Latitude")
plt.xlabel("Latitude")
plt.ylabel("Wind Speed in Meters Per Second")
plt.xlim(-80,100)
plt.ylim(-5, 40)
plt.savefig("windspeed_vs_lat")
plt.show()


# In[11]:


random_sample_df.to_csv(path_or_buf="random_global_weather.csv")

