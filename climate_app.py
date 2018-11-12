# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 12:27:04 2018

@author: owner
"""

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the previous year with the last date 8/23/2017"""
    # Calculate the date year before from 8/23/2017
    last_12month = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the date and precipitation for last_12_month
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_12month).all()

    # Dict with date as the key and prcp as the value
    precp = {date: prcp for date, prcp in precipitation}
    return jsonify(precp)


@app.route("/api/v1.0/stations")
def stations():
    """Return list of stations."""
    results = session.query(Station.station).all()

    # Unravel results and convert to a json list
    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
    # Calculate the date from a year ago from 8/23/2017
    last_12month = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the station 'USC00519281 for all tobs from last_12month
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= last_12month).all()

    # Unravel results and convert to json a list
    temps = list(np.ravel(results))

    # Return the results
    return jsonify(temps)


@app.route("/api/v1.0/temp/<start>")
def AVG_MIN_MAX (start):

 # Start or arrival date is 8/10/2018. Query for the start date of this date to get Min/Avg/Max temp   
    last_12month_arrival = dt.date(2018, 8, 10) - dt.timedelta(days=365)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= last_12month_arrival).all()
    temps = list(np.ravel(results))
    # Return the results
    return jsonify(temps)

@app.route("/api/v1.0/temp/<start>/<end>")
def AVG_MIN_MAX_Start_END (start,end):
    
    last_12month_arrival = dt.date(2018, 8, 10) - dt.timedelta(days=365)
    last_12month_departure = dt.date(2018, 8, 23) - dt.timedelta(days=365)
    
    """Return TMIN, TAVG, TMAX."""

    # calculate TMIN, TAVG, TMAX with arrival and departure set dates
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= last_12month_arrival).\
        filter(Measurement.date <= last_12month_departure).all()
    # Unravel results to convert to a json list
    temps = list(np.ravel(results))
    return jsonify(temps)

   
if __name__ == '__main__':
    app.run()
