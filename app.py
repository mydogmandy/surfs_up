# Importing dependencies:
import datetime as dt
import numpy as np 
import pandas as pd 
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base 
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func 
from flask import Flask, jsonify 

# Create connection between data and web:
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True) 
Measurement = Base.classes.measurement 
Station = Base.classes.station 
session = Session(engine) 
app = Flask (__name__) 

# Adding welcome route:
@app.route('/')
def welcome():
    return('''
    Welcome to the Climate Analysis API!<br>
    <br>
    Available Routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/temp/start/end
    ''')

# Adding precipitation route
# Use '127.0.0.1:5000/api/v1.0/precipitation' to view data:
@app.route('/api/v1.0/precipitation')
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Adding stations route
# Use '127.0.0.1:5000/api/v1.0/station' to view data:
@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

# Adding temperature observations route
# Use '127.0.0.1:5000/api/v1.0/tobs' to view data:
@app.route('/api/v1.0/tobs')
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
filter(Measurement.station == 'USC00519281').\
filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# Adding minimum, average, and maximum temperatures
@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')
def api(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
#'if not end:' code referenced in module commented out
    results = session.query(*sel).\
filter(Measurement.date >= start).\
filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
if __name__ == '__main__':
    app.run()