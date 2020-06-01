#!/usr/bin/python3
#
# run this script only once to create the first Input entry in OpenCMS
# after that, you can define the necessary Feeds and run 
# solarEdge2emonCMS to import the data
#
import time
import json
import urllib.request
from urllib.parse import quote
from datetime import datetime
import sys
import configparser

config = configparser.ConfigParser()
config.read("solarEdge2emonCMS.ini")
debug = config['DEFAULT']['debug']

# get start and end date from SolarEdge

solarEdgeQuery = config['SolarEdge']['URL'] \
	+ config['SolarEdge']['ObjectId'] + "/dataPeriod" + "?api_key=" \
	+ config['SolarEdge']['ApiKey']
if (debug): print(solarEdgeQuery)

with urllib.request.urlopen(solarEdgeQuery) as url:
	data = json.loads(url.read().decode())

startDate = data["dataPeriod"]["startDate"]
print("Start date: " + startDate)
if (debug): print(data)

solarEdgeQuery = config['SolarEdge']['URL'] \
	+ config['SolarEdge']['ObjectId'] + "/power.json" + "?startTime=" \
	+ startDate + "%2000:00:00" + "&endTime=" \
	+ startDate + "%2000:15:00" + "&api_key=" \
	+ config['SolarEdge']['ApiKey']
if (debug): print(solarEdgeQuery)

with urllib.request.urlopen(solarEdgeQuery) as url:
	data = json.loads(url.read().decode())

if (debug): print(data)

# {'power': {'timeUnit': 'QUARTER_OF_AN_HOUR', 'unit': 'W', 'measuredBy': 
# 'INVERTER', 'values': [{'date': '2020-05-09 20:30:00', 'value': 38.333332}]}}

for x in data["power"]["values"]:
	tz = str(int(datetime.strptime(x["date"], '%Y-%m-%d %H:%M:%S').timestamp()))
	val = str(x["value"])
	if (val == "None"):
		val = "0"
	emonQuery = config['EmonCMS']['URL'] + '/input/post?node=' \
		+ config['EmonCMS']['Node']  + '&time=' + tz \
		+ '&csv=' + val + '&apikey=' + config['EmonCMS']['ApiKey']
	if (debug): print(emonQuery)
	with urllib.request.urlopen(emonQuery) as url:
		emonData = url.read().decode()
		if (debug): print(emonData)


