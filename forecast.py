#!/usr/bin/python

import urllib, urllib2
import json

def get_location( ip, service = 'http://ip-api.com/json/' ):
  location = urllib.urlopen( service + ip ).read()
  location_json = json.loads( location )
  print( ip )
  print( location_json['city'] )
  print( location_json['region'] )
  print( location_json['countryCode'] )

# Reference: https://developer.yahoo.com/weather/
def get_weather( ):
# http://api.wunderground.com/auto/wui/geo/GeoLookupXML/index.xml?query=37.76834106,-122.39418793
# http://forecast.weather.gov/MapClick.php?lat=40.781581302919285&lon=-73.96648406982422&site=okx&unit=0&lg=en&FcstType=text#.V8H0t2QrJ7g 
# https://pypi.python.org/pypi/noaaweather/0.1.0

  baseurl = "https://query.yahooapis.com/v1/public/yql?"
  yql_query = "select * from weather.forecast where woeid=2460286"
  yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
  result = urllib2.urlopen(yql_url).read()
  data = json.loads(result)
  print data['query']['results']['channel']['item']['forecast'][1]['high']


print('------------')
get_location( '8.8.8.8' )
get_weather( )
#get_location( '73.14.44.118' )
