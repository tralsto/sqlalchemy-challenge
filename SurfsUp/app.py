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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
        """Precipitation Data from the last 12 months""""
        year_prev = dt.date(2017,8,23) - dt.timedelta(days=365)

        # Perform a query to retrieve the data and precipitation scores
        prcp_results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= year_prev).\
        order_by(measurement.date).all()
        
        return jsonify(prcp_results)

@app.route("/api/v1.0/stations")
def stations():
        """S""""
        return jsonify()

@app.route("/api/v1.0/tobs")
def temps():
        """T""""
        return jsonify()

@app.route("/api/v1.0/<start>")
def start():
        """S""""
        return jsonify()
    
@app.route("/api/v1.0/<start>/<end>")
def start_end():
        """S""""
         return jsonify()