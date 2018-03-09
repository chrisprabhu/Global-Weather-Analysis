
# coding: utf-8

# In[1]:


# Three Observable Trends
# 1. The temperature increases as you approach the equator with peaks at -20 degrees and 20 degrees.
# 2. Just below the equator from 0 to -20 there no points with low humidity suggesting this is a very humid region. 
# 3. Windspeed noticeabley increases as you move away from the equator. 


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


#Generate a list of random cities using random coordinates and the nearest city to those coordinates:

cities_list = []

while len(cities_list) < 1000:
    city = citipy.nearest_city(random.randrange(-90,90), random.randrange(-180,180)).city_name
    if city not in cities_list:
        cities_list.append(city)


# In[4]:


# Define Lists
temp = []
humidity = []
wind = []
cloudiness = []
open_weather_city_number = []
lat = []
lon = []
used_cities = []
process_number = 0
url = "api.openweathermap.org/data/2.5/weather?q="

# Query the API with Coordinates and create lists with Temperature, Humidity, Wind Speed, and Cloudiness Info.

for city in cities_list:
    if len(temp) < 500:
        query = f"http://{url}{city}&APPID={api_key}&units={units}"
        response = requests.get(query).json()
        
        #Add weather date to their appropriate lists:
        try:
            temp.append(response['main']['temp'])
            humidity.append(response['main']['humidity'])
            wind.append(response['wind']['speed'])
            cloudiness.append(response['clouds']['all'])
            open_weather_city_number.append(response['id'])
            lat.append(response['coord']['lat'])
            lon.append(response['coord']['lon'])
            used_cities.append(city)
            # Print the current process's information:
            process_number = process_number + 1
            print(f"{process_number}: Currently processing the city with the following information:")
            print(f"City ID Number: {response['id']}")
            print(f"City Name: {city}")
            print(f"Query url: {query}")
        except KeyError:
            print([response,city])


# In[5]:


random_sample_df = pd.DataFrame(data = used_cities, columns = ["Cities"])


# In[6]:


random_sample_df["Current Temperature"] = temp
random_sample_df["Current Humidity"] = humidity
random_sample_df["Current Wind Speed"] = wind
random_sample_df["Current Cloudiness"] = cloudiness
random_sample_df["Latitude"] = lat
random_sample_df["Longitude"] = lon
random_sample_df.head()


# In[7]:


# Add the OpenWeatherMap City numbers to the dataframe. 
random_sample_df['OpenWeatherMap City Number'] = open_weather_city_number
random_sample_df.head()


# In[8]:


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


# In[9]:


#Humidity % VS Latitude
plt.scatter(random_sample_df["Latitude"], random_sample_df["Current Humidity"])
plt.title("Humidity VS. Latitude")
plt.xlabel("Latitude")
plt.ylabel("Percentage Humidity")
plt.xlim(-80,100)
plt.ylim(-20, 120)
plt.savefig("humidity_vs_lat.png")
plt.show()


# In[10]:


# Cloudiness % VS Latitude
plt.scatter(random_sample_df["Latitude"], random_sample_df["Current Cloudiness"], s=15)
plt.title("Percent Cloudiness vs Latitude")
plt.xlabel("Latitude")
plt.ylabel("% Cloudiness")
plt.xlim(-60,80)
plt.ylim(-20,120)
plt.savefig("cloudiness_vs_lat")
plt.show()


# In[11]:


#Wind Speed VS Latitude
plt.scatter(random_sample_df["Latitude"], random_sample_df["Current Wind Speed"])
plt.title("Wind Speed vs Latitude")
plt.xlabel("Latitude")
plt.ylabel("Wind Speed in Meters Per Second")
plt.xlim(-80,100)
plt.ylim(-5, 40)
plt.savefig("windspeed_vs_lat")
plt.show()


# In[12]:


random_sample_df.to_csv(path_or_buf="random_global_weather.csv")

