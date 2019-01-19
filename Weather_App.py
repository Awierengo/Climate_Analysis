import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Initialize Flask
app = Flask(__name__)

#Initialize our database

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station



#Routes
@app.route("/")
def index():
    return(
        "All available routes:"
        "<br/>"
        "<a href = api/v1.0/precipitation>/api/v1.0/precipitation</a>"
        "<br/>"
        "<a href = api/v1.0/stations>/api/v1.0/stations</a>"
        "<br/>"
        "<a href = api/v1.0/tobs>/api/v1.0/tobs</a>"
    ) 

@app.route("/api/v1.0/precipitation")
def precipitation():
# Use our query from before initialize unique session
    session = Session(engine)

    query = session.query(Measurement.date, func.max(Measurement.prcp)).filter(Measurement.date >= '2016-08-24').group_by(Measurement.date).all()

    # add dictionarys to list
    precips = []
    for precip in query:
        precipitation_dict = {}
        precipitation_dict['date'] = precip[0]
        precipitation_dict['prcp'] = precip[1]
        precips.append(precipitation_dict)

    #Jsonify our list
    return jsonify(precips)



@app.route("/api/v1.0/stations")
def stations():
    #initialize unique session
    session = Session(engine)

    # query from before
    query2 = session.query(Station.station, Station.name).group_by(Station.station).all()

    # add dictionarys to list
    stations = []
    for station in query2:
        stations_dict = {}
        stations_dict["station_id"] = station[0]
        stations_dict["station_name"] = station[1]
        stations.append(stations_dict)

    #Jsonify our list
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    #initialize unique session
    session = Session(engine)


    # query from before
    query3 = session.query(Measurement.station, func.count(Measurement.tobs)).filter(Measurement.date >= '2016-08-24').group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).all()

    # add dictionarys to list
    tobs = []
    for tob in query3:
        tobs_dict = {}
        tobs_dict["station"] = tob[0]
        tobs_dict["temp_observations"] = tob[1]
        tobs.append(tobs_dict)
    #Jsonify our list
    return jsonify(tobs)


if __name__ == "__main__":
    app.run(debug=True)