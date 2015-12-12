#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------ DONNEES.PY --------------

import urllib.request
import pandas as pd
import time
import re
import json
from pandas.io.json import json_normalize
import rpy2.robjects as robjects

url = "http://opendata.paris.fr/api/records/1.0/search/?dataset=stations-velib-disponibilites-en-temps-reel&rows=1240&facet=banking&facet=bonus&facet=status&facet=contract_name"

try:
    for i in range(1,1):
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

        #Sauvegarde dans un .csv
        df.to_csv("/Users/louisdecharson/Programmation/Python/Velib/data/velib.csv")
        #Lancement du script R.
        r=robjects.r
        r['source']("plot.R")
        #Attente 60 secondes
        #time.sleep(60)
except:
    e=sys.exc_info()[0]
    write_to_page( "<p>Error: %s</p>" % e )



