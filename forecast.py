#!/usr/bin/python

"""a Python module that parces a file for IP addresses and creates a histogram data for tomorrows high temps

Classes:
  GeoWeather: Contains geographic and weather methods and utilities
  Log: Creates and manages log files
  Parse: Reads the source file and creates a list of IP addresses

Troubleshooting:
  This module was built and tested with Python 2.7.11 on Ubuntu Linux. 

""" 

try: 
  import urllib, urllib2
  import json
  import csv
except ImportError as err_str:
  print( "{}, make sure module exists on your server".format(err_str) ) 
  exit()

def get_high_temp_from_ip( ip = '8.8.8.8' ):
  zip = _get_location( ip )
  woeid = _get_woeid( zip )
  high_temp = _get_tomorrows_high_temp( woeid )

  return high_temp


# Returns tomorrows high temperature in deg F. for the location specified
# by the passed Where On Earth ID, default is Boulder CO, US
def _get_tomorrows_high_temp( woeid = 2367231 ):
  # Reference: https://developer.yahoo.com/weather/
  baseurl = "https://query.yahooapis.com/v1/public/yql?"
  yql_query = "select * from weather.forecast where woeid=" + str( woeid )
  yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
  result = urllib2.urlopen(yql_url).read()
  data = json.loads(result)

  return data['query']['results']['channel']['item']['forecast'][1]['high']

# Returs the location in zip code for now 
# TODO Zip probably is not localizable, need to look at city/state/country or longatude/latatude
def _get_location( ip, service = 'http://ip-api.com/json/' ):
  location = urllib.urlopen( service + ip ).read()
  location_json = json.loads( location )
#  print( location_json )
  print( location_json['city'] + ',' + location_json['region'] + ',' + location_json['countryCode'] + ',' + location_json['zip'] )
#  print( location_json['lon'] )
#  print( location_json['lat'] )

  return location_json['zip']


# Return the Where On Earth ID based on a zip code for now
# Default is Boulder CO.
def _get_woeid( zip = 80301 ):
  # Reference: https://developer.yahoo.com/weather/
  baseurl = "https://query.yahooapis.com/v1/public/yql?"
  yql_query = "select * from geo.places where text=" + str( zip )
  yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
  result = urllib2.urlopen(yql_url).read()
  data = json.loads(result)

  return data['query']['results']['place'][0]['woeid']


def test( ip ):
  print( '------------' )
  print( 'IP:' + ip )
  high_temp = get_high_temp_from_ip( ip )
  print( 'Temp:' + high_temp )


def scan_for_ip( file = './data/devops_coding_input_log1.log' ):
  ip_list = []

  # Pandas.pydata.org would be better but to keep this simple just use brute force column parsing
  with open( file, 'r' ) as ff:
    for line in ff.readlines():
      cells = line.split( '\t' )
      # assume cell 
      ip = cells[23]
      ip_list.append( ip )
#      if len(ip_list)  > 5 :
#        break

  print( ip_list )
  return ip_list


ip_list = scan_for_ip( )

fails = 0
for ip in ip_list:
  try:
    high_temp = get_high_temp_from_ip( ip )
    print( "Temp:" + str( high_temp ) )
  except:
    fails = fails + 1
    print( ">>>>>ip failrure: " + str( ip ) )

print( "Done total failures: "  + str( fails ) )

#test( '62.102.227.177' )
#test( '184.168.47.225' )
#test( '94.199.116.23' )
#test( '101.0.89.226' )

