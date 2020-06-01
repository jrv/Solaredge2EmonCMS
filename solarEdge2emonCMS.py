#!/usr/bin/python3

import time
import json
import urllib.request
from urllib.parse import quote
from datetime import datetime
import sys
import configparser

config = configparser.ConfigParser()
config.read("solarEdge2emonCMS.ini")
debug = ( config['DEFAULT']['debug'] == "True")

# check EmonCMS to get the last upload timestamp
# and set a timeframe for the next SolarEdge Download
emonQuery = config['EmonCMS']['URL'] + '/input/list&apikey=' \
	+ config['EmonCMS']['ApiKey']
if (debug): print(emonQuery)
with urllib.request.urlopen(emonQuery) as url:
	data = json.loads(url.read().decode())
for x in data:
	if (x['nodeid'] == config['EmonCMS']['Node']):
		ct = int(x['time']) + 65
		ctmax = ct + 24*60*60
		if (debug): print(ct)
		tz = datetime.fromtimestamp(ct)
		if (debug): print(tz.strftime('%Y-%m-%d%%20%H:%M:%S'))
		if (ctmax > time.time()):
			ctmax = time.time() - 5*60
			if (debug): print("Use current time as tmax")
		else:
			if (debug): print("old tmax")
		tzmax = datetime.fromtimestamp(ctmax)
		if (debug): print(tzmax.strftime('%Y-%m-%d%%20%H:%M:%S'))

if (ctmax < ct + 15*60):
	if (debug): print('Already up to date')
	sys.exit(1)

solarEdgeQuery = config['SolarEdge']['URL'] \
	+ config['SolarEdge']['ObjectId'] + "/power.json" + "?startTime=" \
	+ tz.strftime('%Y-%m-%d%%20%H:%M:%S') + "&endTime=" \
	+ tzmax.strftime('%Y-%m-%d%%20%H:%M:%S') + "&api_key=" \
	+ config['SolarEdge']['ApiKey']
if (debug): print(solarEdgeQuery)

with urllib.request.urlopen(solarEdgeQuery) as url:
	data = json.loads(url.read().decode())

# {'power': {'timeUnit': 'QUARTER_OF_AN_HOUR', 'unit': 'W', 'measuredBy': 
# 'INVERTER', 'values': [{'date': '2020-05-09 20:30:00', 'value': 38.333332}]}}

for x in data["power"]["values"]:
	tz = str(int(datetime.strptime(x["date"], '%Y-%m-%d %H:%M:%S').timestamp()))
	val = str(x["value"])
	if (val == "None"):
		val = "0"
	emonQuery = config['EmonCMS']['URL'] + '/input/post?node=' \
	+ config['EmonCMS']['Node'] + '&time=' + tz \
	+ '&csv=' + val + '&apikey=' + config['EmonCMS']['ApiKey']
	if (debug): print(emonQuery)
	with urllib.request.urlopen(emonQuery) as url:
		emonData = url.read().decode()
		if (debug): print(emonData)


