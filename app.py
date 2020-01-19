import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta

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

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipetation():
    session = Session(engine)
    results=session.query(Measurement.date).order_by(Measurement.date.desc()).limit(1)
    for date in results:
         last_date=date
    my_date = datetime.strptime(last_date[0], "%Y-%m-%d")
    N=365
    d = timedelta(days = N)
    an_year_ago = my_date - d

    results=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>an_year_ago)

    session.close()

    all_prec=[]

    for date, prec in results:
        prec_dict={}
        prec_dict['date']=date
        prec_dict['prec']=prec
        all_prec.append(prec_dict)

    return (jsonify(all_prec))    

   
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    results=session.query(Measurement.station).distinct()

    session.close()

    all_stations=[]

    for station in results:
        all_station={}
        all_station['station']=station
        all_stations.append(all_station)

    return (jsonify(all_stations))   




@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results=session.query(Measurement.date).order_by(Measurement.date.desc()).limit(1)
    for date in results:
         last_date=date
    my_date = datetime.strptime(last_date[0], "%Y-%m-%d")
    N=365
    d = timedelta(days = N)
    an_year_ago = my_date - d

    results=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>an_year_ago)

    session.close()

    all_tobs=[]

    for date, tob in results:
        all_tob={}
        all_tob['date']=date
        all_tob['prec']=tob
        all_tobs.append(all_tob)

    return (jsonify(all_tobs))  



@app.route("/api/v1.0/<start>")
def calc_temps(start):
    session = Session(engine)
    results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    session.close()

    all_starts=[]

    for tmin,tavg,tmax in results:
         all_start={}
         all_start['Min Temp']=tmin
         all_start['Avg temp']=tavg
         all_start['Max temp']=tmax
         all_starts.append(all_start)

    return (jsonify(all_starts))

@app.route("/api/v1.0/<start>/<end>")
def calc_temp_between(start,end):
    session = Session(engine)
    results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end)

    session.close()

    all_ends=[]

    for tmin,tavg,tmax in results:
         all_end={}
         all_end['Min Temp']=tmin
         all_end['Avg temp']=tavg
         all_end['Max temp']=tmax
         all_ends.append(all_end)

    return (jsonify(all_ends))



if __name__ == '__main__':
    app.run(debug=True)