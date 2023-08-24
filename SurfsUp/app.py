# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
def home():
        """List all available Hawaiian Climate Analysis API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>")

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data)
# Put data into a dictionary using date as the key and prcp as the value

@app.route("/api/v1.0/precipitation")
def prcp():
        """Precipitation Data from the last 12 months"""
        
        # Designate the date to be used in the query
        year_prev = dt.date(2017,8,23) - dt.timedelta(days=365)

        # Retrieve the data and precipitation scores from the last 12 months of the data
        prcp_results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= year_prev).\
        order_by(measurement.date).all()
        
        prcp_list = []
        for date, prcp in prcp_results:
            prcp_dict={}
            prcp_dict["Date"] = date
            prcp_dict["Precipitation"] = prcp
            prcp_list.append(prcp_dict)
            
    return jsonify(prcp_list)

if __name__ == '__main__':
    app.run(debug=True)

# Design a query that returns jsonified data of all of the stations in the database   

@app.route("/api/v1.0/stations")
def stations():
        """List of Stations"""
        stations = session.query(station.id, station.name).all()
    return jsonify(stations)
        
# Design a query that returns jsonified data for the most active station (USC00519281)
# Only returns the jsonified data for the last year of data

@app.route("/api/v1.0/tobs")
def temps():
        """Temperature Climate Analysis from the Most Active Station (USC00519281)"""
        temp = session.query(measurement.date, measurement.station, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= year_prev).\
        order_by(measurement.date.desc()).all()
    return jsonify()

# Design a query for the start route that:
# Accepts the start date as a parameter from the URL
# Returns the TMIN, TMAX, and TAVG temperatures calculated from the given start date.
    
@app.route("/api/v1.0/<start>")
def start():
    
        # Designate the date to be used in the query
        last_year = dt.date(2017,8,23) - dt.timedelta(days=365)
        
        """Min, Max, and Average Temperatures from the specified date"""
        start_route = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.station == 'USC00519281').all().\
        filter(measurement.date >= last_year).\
        group_by(measurement.date.desc()).all()
    return jsonify(start_route)
    
    
# Design a query for the start/end route that:
# Accepts the start and end dates as parameters from the URL
# Returns the TMIN, TMAX, and TAVG temperatures calculated from the given start date to the given end date.

@app.route("/api/v1.0/<start>/<end>")
def start_end():
        """S"""
        
    return jsonify()


# Close the session
session.close()