# Serverless IoT Structure

This section explains in details the json file format used for the Serverless structure of the new gen IoT (Using edge computing).

```
[
	{
		"metadata":{
			"metricType" : "sampleSensor"
			"metricID" : "testVar"
			"geoLoc" : "PESU_1"
			"infraLoc" : "amd64-PC"
			"platLoc" : "testPlatform"
		},
		"logTS" : [
			epochs, , , 
		]
		"vals":[
			1,
			2,
			3,
			4
		]
	}
]
```

### Metadata

The metadata is the data about the data sent to the server. It contains the following segments:-

**metricType**: What type of sensor is used, such as Temperature, Humidity, etc.

**metricID**: ID of the sensor (Sensor number 1, 2, ...)

**geoLoc**: Geographical location of the the sensor (Address, or Location ID)

**infraLoc**: What infrastructure is the sensor application hosted on

**platLoc**: What platform is being used

### Logging

The ```logTS``` and ```vals``` together form the epoch times, and values collected at that time respectively. This shall be added to the db table in a serial order.

## Deployment on Docker

The Charcoal DB IoT serverless API can be deployed on using DOcker Swarms. In order to do so, follow the steps:-
*May need ```sudo``` commands if [post installation steps](https://docs.docker.com/install/linux/linux-postinstall/) not followed.*

1. **Initiate Docker swarm**
```
$ docker swarm init
```

2. **On Raspberry Pi, create the mount location and the copy the DB**
```
$ cd /
$ sudo mkdir /iot-DB
$ sudo chmod 777 /iot-DB
```
Copy the TestDB.db on the git repo to the mount location ```/iot-DB```.

3. **Deploy the stack on the swarm**
Browse back to ```USN-Scripts/IoT Server``` folder. Replace ```[OPTION]``` with ```arm``` for Raspberry Pi or ```amd``` for amd64 architecture laptops.
```
$ docker stack deploy -c docker-compose-[OPTION].yaml charcoal
```

4. **Test for service deoployment and container replication**
```
$ docker service ls
```