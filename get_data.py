#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------ DONNEES.PY --------------

# Python Packages
import urllib.request
import pandas as pd
import time
import re
import json
from pandas.io.json import json_normalize
from time import gmtime, strftime


# R Packages
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
r=robjects.r
from rpy2.robjects.packages import STAP


url = "http://opendata.paris.fr/api/records/1.0/search/?dataset=stations-velib-disponibilites-en-temps-reel&rows=1240&facet=banking&facet=bonus&facet=status&facet=contract_name"

myDataDir="/Users/louisdecharson/Programmation/Python/Velib/data/"

def create_map_with_R(path_to_csv):
    with open('plot.R', 'r') as f:
        string = f.read()
    plot_R = STAP(string, "plot_R")
    plot_R.plotMyMap(path_to_csv)

    # r.assign('path_to_csv', path_to_csv)
    # r['source']("plot.R"


for i in range(0,1):
    response = urllib.request.urlopen(url)
    data=str(response.read()).strip()

    # Remove some strange characters hiding
    data=data[2:-1]
    data=data.replace("\\\'","'")

    json_data=json.loads(data)

    df=json_normalize(json_data['records'])

    # Mise en forme de DF
    longitude = [item[0] for item in df['geometry.coordinates']]
    latitude = [item[1] for item in df['geometry.coordinates']]
    df['longitude']=longitude
    df['latitude'] = latitude

    df.rename(columns={'fields.address': 'address', 'fields.available_bike_stands': 'available_bike_stands','fields.available_bikes' : 'available_bikes', 'fields.bonus' : 'bonus', 'fields.last_update' : 'last_update', 'fields.number' : 'station_number', 'fields.status' : 'status', 'fields.bike_stands' :'bike_stands' }, inplace=True)
    df.drop('fields.banking', axis=1, inplace=True)
    df.drop('fields.contract_name', axis=1, inplace=True)
    df.drop('fields.name', axis=1, inplace=True)


    #Sauvegarde dans un .csv
    myClock=strftime("%Y_%m_%d__%H_%M_%S", gmtime())
    path_to_csv=myDataDir+"veliv_"+myClock+".csv"
    df.to_csv(path_to_csv)
    
    #Lancement du script R.
    create_map_with_R(path_to_csv)
    time.sleep(60)




# for i in range(1,1):
#     try:
#         response = urllib.request.urlopen(url)
#         data=str(response.read()).strip()

#         # Remove some strange characters hiding
#         data=data[2:-1]
#         data=data.replace("\\\'","'")

#         json_data=json.loads(data)

#         df=json_normalize(json_data['records'])

#         # Mise en forme de DF
#         longitude = [item[0] for item in df['geometry.coordinates']]
#         latitude = [item[1] for item in df['geometry.coordinates']]
#         df['longitude']=longitude
#         df['latitude'] = latitude

#         #Sauvegarde dans un .csv
#         df.to_csv("/Users/louisdecharson/Programmation/Python/Velib/data/velib.csv")
#         #Lancement du script R.
#         r=robjects.r
#         r['source']("plot.R")

#     except:
#         e=sys.exc_info()[0]
#         write_to_page( "<p>Error: %s</p>" % e)
    
#     finally:
#         print("done.")
#         # Attente 60 secondes
#         # time.sleep(60)


