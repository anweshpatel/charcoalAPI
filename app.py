#	Author : @anweshpatel
#	Created : 3.14.2019
#	Project : Unified Sensor Network
#	Module : IoT Aggregator (Metrics) [R-Pi]
#	Version : v0.0.2 (Alpha 2)

import flask
from flask import request, jsonify

import time
import os
import sqlite3
import logging
import socket
import datetime

# constants
DB_LOC = "./DB"
CONFIG_LOC = "."
LOGS_LOC = "."
ERR_LOG = "Charcoal_logs_"

curTime = datetime.datetime.now().strftime("%Y-%m-%d")

# Logging Setup
logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.join(LOGS_LOC, ERR_LOG+curTime+".log"), mode='a', delay=False)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('[ %(asctime)s - %(process)d - %(levelname)s ] %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.info("API Started!")

# Methods needed **Push to a library**
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# API Setup
app = flask.Flask(__name__)
app.config['DEBUG'] = True

# HTTP Errorhandlers
@app.errorhandler(404)
def routeNotFound(self):
	return jsonify([{"code":404,"API message":"Route not found"}])

@app.errorhandler(405)
def methodNotAllowed(self):
	return jsonify([{"code":405,"API message":"Method not allowed"}])

# Sample update JSON
# [
# 	{
# 		"metadata":{
# 			"metricType" : "sampleSensor"
# 			"metricID" : "testVar"
#			"parameterType":"sample parameter"
#			"parameterID":"sampleParam"
# 			"geoLoc" : "PESU_1"
# 			"infraLoc" : "amd64-PC"
# 			"platLoc" : "testPlatform"
# 		},
# 		"intervals" : in millisecs
# 		"vals":[
# 			1,
# 			2,
# 			3,
# 			4
# 		]
# 	}
# ]

# API routes
# Update Data http://url:port/api/v1/update
@app.route('/api/v1/update', methods=['POST'])
def dataUpdate():
	if request.method == "POST":
		qParams = request.data
		queryParams = eval(qParams)
		metadata = queryParams[0]['metadata']
		query = ""
		queryArgs = []

		query = "SELECT tablename FROM metadata WHERE geoLoc=? and metricID=? and parameterID=?;"
		queryArgs.append(metadata['geoLoc'])
		queryArgs.append(metadata['metricID'])
		queryArgs.append(metadata['parameterID'])
		
		# DB Setup
		try:
			dbConn = sqlite3.connect(os.path.join(DB_LOC,"TestDB.db"))
			logger.info("EVENT:SUCCESS: Database opened successfully")
		except Exception as e:
			logger.critical("Exception: "+e)
		dbConn.row_factory = dict_factory
		cur = dbConn.cursor()

		results = cur.execute(query, queryArgs).fetchall()

		if results == []:
			return jsonify([{"code":422, "API Message":"UNPROCESSABLE ENTITY: The request was well-formed but was unable to be followed due to semantic errors. Please Check metadata before requesting."}])
		else:
			tableID = results[0]['tablename']
			query = "INSERT INTO "+tableID+" VALUES("

			#epochs = queryParams[0]['logTS']
			intervals = queryParams[0]['intervals']
			millis = int(round(time.time() * 1000)) #current time in millisecs
			vals = queryParams[0]['vals']

			epochs = []

			# Epoch list generator
			for i in range(len(vals)):
				epochs.append(millis - intervals*i)
			
			epochs.reverse()

			for i in range(len(vals)):
				execQuery = query+str(epochs[i])+","+str(vals[i])+")"
				try:
					cur.execute(execQuery)
					logger.info("EVENT:SUCCESS: Query successful")
				except Exception as e:
					logger.error("Exception: "+e)
			
			try:
				dbConn.commit()
				logger.info("EVENT:SUCCESS: Update successful")
			except Exception as e:
				logger.error("Exception: "+e)
			dbConn.close()
			return jsonify([{"code":201, "API message":"ACCEPTED: The request has been fulfilled, resulting in the creation of a new resource."}])

# sample health check JSON
# [
# 	{
# 		"metadata":{
# 			"metricType" : "sampleSensor"
# 			"metricID" : "testVar"
# 			"geoLoc" : "PESU_1"
# 			"infraLoc" : "amd64-PC"
# 			"platLoc" : "testPlatform"
# 		},
# 		"candidate":"sentinel/slave"
#	}
# ]

# Health check HTML
@app.route('/api/v1/health', methods=['GET', 'POST'])
def healthCheck():
	if request.method == 'POST':
		pParams = request.data
		postParams = eval(pParams)
		metadata = postParams[0]['metadata']
		#logger.info("Metadata" + metadata)
		selfMeta = [{"response":200,"geoLoc":"PESU_0","infraLoc":"armhf","platLoc":"testPlatform","health":{"cpus":"active","memory":"free","containers":"all-up"}}]
		
		if postParams[0]['candidate'] == "sentinel":
			return jsonify(selfMeta)
		else:
			return jsonify([{"code":200,"API message":"OK: Metrics is active.","hostName":"raspberry"}])
	elif request.method == 'GET':
		return "<h3>This is the metrics API health check</h1><p>Health = Good<p>Now running on "+socket.gethostname()

# sample health check JSON
# [
# 	{
# 		"metadata":{
# 			"metricType" : "sampleSensor"
# 			"metricID" : "testVar"
# 			"geoLoc" : "PESU_1"
# 			"infraLoc" : "amd64-PC"
# 			"platLoc" : "testPlatform"
# 		},
# 		"candidate":"sentinel/slave"
#	}
# ]

# Get actuator data
@app.route('/api/v1/actuator', methods=['POST'])
def actuator():
	if request.method == 'POST':
		pParams = request.data
		postParams = eval(pParams)
		metadata = postParams[0]['metadata']
		#print(metadata)
		queryArgs = []

		query = "SELECT tablename FROM metadata WHERE geoLoc=? and metricID=? and parameterID=?;"
		queryArgs.append(metadata['geoLoc'])
		queryArgs.append(metadata['metricID'])
		queryArgs.append(metadata['parameterID'])

		# DB Setup
		try:
			dbConn = sqlite3.connect(os.path.join(DB_LOC,"TestDB.db"))
			logger.info("EVENT:SUCCESS: Database opened successfully")
		except Exception as e:
			logger.critical("Exception: "+e)
		dbConn.row_factory = dict_factory
		cur = dbConn.cursor()

		results = cur.execute(query, queryArgs).fetchall()

		if results == []:
			return jsonify([{"code":422, "API Message":"UNPROCESSABLE ENTITY: The request was well-formed but was unable to be followed due to semantic errors. Please Check metadata before requesting."}])
		else:
			tableID = results[0]['tablename']
			query = "SELECT metric FROM "+tableID+" WHERE epoch = (SELECT MAX(epoch) from "+tableID+");"
			results = cur.execute(query).fetchall()
			return jsonify([{"value":results}])

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)