#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from monvelib.models import Station, Velos, update_stations, createMap 


stations=Blueprint('stations',__name__,template_folder='templates')

class HomeView(MethodView):
    
    def get(self):
        stations=Station.objects.all()
        openStations=0
        closeStations=0
        nbBikes=0
        nbStands=0
        for station in stations:
            last=len(station.velos)-1
            if station.velos[last].status=="OPEN":
                openStations+=1
            else:
                closeStations+=1
            nbBikes+=station.velos[last].bikes
            nbStands+=station.velos[last].stands
        generalStatus=[openStations,closeStations,nbBikes,nbStands]  
        return render_template('index.html',generalStatus=generalStatus)

class MapView(MethodView):

    def get(self):
        import os.path
        if not os.path.isfile("static/img/map.png"):
            createMap()
        return render_template('map.html')

    def post(self):
        createMap()
        return render_template('map.html')
        
        
class ListView(MethodView):

    def get(self):
        stations=Station.objects.all()
        return render_template('stations/list.html',stations=stations)

    def post(self):
        update_stations()
        stations=Station.objects.all()
        return render_template('stations/list.html',stations=stations)
    
class DetailView(MethodView):

    def get(self,slug):
        station=Station.objects.get_or_404(slug=slug)
        lastVelo=len(station.velos)-1
        myUrlMap="https://www.google.com/maps/embed/v1/place?key=AIzaSyCLIuSIWGEbQA8rRFHB_0YtKRMaYDXWDWk&q="+str(station.coord[0])+","+str(station.coord[1])+"&zoom=15"
        return render_template('stations/detail.html',station=station,myUrlMap=myUrlMap,lastVelo=lastVelo)

stations.add_url_rule('/stations/',view_func=ListView.as_view('list'))
stations.add_url_rule('/stations/<slug>/',view_func=DetailView.as_view('detail'))
stations.add_url_rule('/',view_func=HomeView.as_view('index'))
stations.add_url_rule('/map/',view_func=MapView.as_view('map'))
