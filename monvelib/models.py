#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from flask import url_for
from monvelib import db

class Velos(db.EmbeddedDocument):
    last_update=db.DateTimeField(required=True)
    total_stands=db.IntField(required=True)
    stands=db.IntField(required=True)
    bikes=db.IntField(required=True)
    status=db.StringField(required=True)
    
class Station(db.Document):
    # Data on Bike's Stations
    id_station=db.IntField(required=True)
    name=db.StringField(required=True)
    address=db.StringField(required=True)
    postal_code=db.StringField()
    coord=db.ListField(required=True)
    bonus=db.StringField(required=True)
    velos=db.ListField(db.EmbeddedDocumentField('Velos'))
    lastModified=db.DateTimeField(default=datetime.datetime.now)
    
    # Data for Web
    slug=db.StringField(max_length=255,required=True)
    # Statistics Methods
    
    # Web Methods
    def get_absolute_url(self):
        return url_for('station',kwargs={"slug":self.slug})

    def __unicode__(self):
        return self.name

    # Meta
    meta = {
        'allow_inheritance' : True
    }


## S L U G I F Y
## stolen on flask website
import re
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))
####

## U P D A T E   D A T A B A S E
## ------------------------------
def update_stations():
    import urllib.request
    import pandas as pd
    import time
    import json
    import pymongo
    import os
    from pandas.io.json import json_normalize
    from time import gmtime, strftime
    import datetime

    url = "http://opendata.paris.fr/api/records/1.0/search/?dataset=stations-velib-disponibilites-en-temps-reel&rows=1240&facet=banking&facet=bonus&facet=status&facet=contract_name"
    response=urllib.request.urlopen(url)
    data=str(response.read())
    data=data.strip() # the json file is not so clean
    data=data[2:-1] # the json file is not so clean
    data=data.replace("\\\'","'") # the json file is not so clean
    json_data=json.loads(data)
    for station in json_data['records']:
        station_fields=station['fields']
    
        myStation=Station()
        mesVelos=Velos()
        
        id_station=station_fields['number']
        name=station_fields['name']
        address=station_fields['address']
        v_address=address.split("-")
        if len(v_address)>1:
            postal_code=v_address[len(v_address)-1][1:6]
        else:
            postal_code="NA"
        coord=station_fields['position']
        bonus=station_fields['bonus']
        slug=str(id_station)
        
        mesVelos.last_update=station_fields['last_update']
        mesVelos.total_stands=station_fields['bike_stands']
        mesVelos.bikes=station_fields['available_bikes']
        mesVelos.stands=station_fields['available_bike_stands']
        mesVelos.status=station_fields['status']
        
        Station.objects(id_station=id_station).update_one(
            set__id_station=id_station,
            set__name=name,
            set__address=address,
            set__postal_code=postal_code,
            set__coord=coord,
            set__bonus=bonus,
            set__slug=slug,
            upsert=True)

        myStation=Station.objects.get(id_station=id_station)
        myStation.velos.append(mesVelos)
        myStation.save()

## C R E A T E   M A P
# --------------------
def createMap():
    import rpy2.robjects as robjects
    r=robjects.r
    r['source']("myplot.R")
