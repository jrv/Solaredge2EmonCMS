# Solaredge2EmonCMS
Python script to upload data from SolarEdge API to EmonCMS

This script can be used to harvest data from the SolarEdge website and upload it to EmonCMS. It can run from cron to get the current energy production (every 15 minutes).

How to use:

* Copy solarEdge2emonCMS.ini.template to solarEdge2emonCMS.ini and set all values for your installation
* Run solarEdge2emonCMS-setup.py once, this will create an Input in EmonCMS
* Create the necessary Feeds in EmonCMS
* Run solarEdge2emonCMS.py to upload data. It will upload approximately 1 day of data at a time, starting with the oldest data, so to get it up to date, you have to run it a number of times. Dont run multiple instances at the same time, but you can loop it until all your data has been uploaded.
* When all data is uploaded, you can install solarEdge2emonCMS.py to run from cron every 15 minutes
