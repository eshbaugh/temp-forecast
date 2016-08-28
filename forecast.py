#!/usr/bin/python

import urllib, urllib2
import json
# from pyql.weather.models import Weather, GeoData

# Returns tomorrows high temperature in deg F. for the location specified
# by the passed Where On Earth ID, default is Boulder CO, US
def get_tomorrows_high_temp( woeid = 2367231 ):
  # Reference: https://developer.yahoo.com/weather/
  baseurl = "https://query.yahooapis.com/v1/public/yql?"
  yql_query = "select * from weather.forecast where woeid=" + str( woeid )
  yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
  result = urllib2.urlopen(yql_url).read()
  data = json.loads(result)
  print data['query']['results']['channel']['item']['forecast'][1]['high'] + ' deg F'

# Returs the location in zip code for now 
# TODO Zip probably is not localizable, need to look at city/state/country or longatude/latatude
def get_location( ip, service = 'http://ip-api.com/json/' ):
  location = urllib.urlopen( service + ip ).read()
  location_json = json.loads( location )
  print( ip )
  print( location_json )
  print( location_json['city'] )
  print( location_json['region'] )
  print( location_json['countryCode'] )
  print( location_json['lon'] )
  print( location_json['lat'] )
  print( location_json['zip'] )

  return location_json['zip']

# Return the Where On Earth ID based on a zip code for now
# Default is Boulder CO.
def get_woeid( zip = 80301 ):
  # Reference: https://developer.yahoo.com/weather/
  baseurl = "https://query.yahooapis.com/v1/public/yql?"
  yql_query = "select * from geo.places where text=" + str( zip )
  yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
  result = urllib2.urlopen(yql_url).read()
  data = json.loads(result)

  return data['query']['results']['place'][0]['woeid']


# Main 
print('------------')
zip = get_location( '8.8.8.8' )
print( "Zip:" + zip )

woeid = get_woeid( zip )
print( "WOEID:" + str( woeid ) )

get_tomorrows_high_temp( woeid )

