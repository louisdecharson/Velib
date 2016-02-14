#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, abort, session
from flask.ext.mongoengine import MongoEngine
from mongoengine import connect
from flask.ext.pymongo import PyMongo

app=Flask(__name__)
app.config["MONGODB_DBNAME"] = 'velib'
connect('velib')

db=MongoEngine(app)

def register_blueprints(app):
    from monvelib.views import stations
    app.register_blueprint(stations)

register_blueprints(app)

# @app.route('/')
# def home():
#     return render_template('index.html')

if __name__=='__main__':
    app.run()
