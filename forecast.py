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
  import math
except ImportError as err_str:
  print( "{}, make sure module exists on your server".format(err_str) ) 
  exit()

# Constants
ZERO_TOL = .001

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

  return location_json['zip']

# returns latitude and longitude
def _get_location2( ip, service = 'http://ip-api.com/json/' ):
  location = urllib.urlopen( service + ip ).read()
  location_json = json.loads( location )

  try: 
    print( location_json['city'] + ',' + location_json['region'] + ',' + location_json['countryCode'] + ',' + location_json['zip'] )
  except:
    print "Ignoring incomplte location name info"
    print location_json

  geo_loc = []
  geo_loc.append( location_json['lat'] )
  geo_loc.append( location_json['lon'] )

  return geo_loc

# Return the Where On Earth ID based on a zip code for now
# Default is Boulder CO.

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

# Return the Where On Earth ID based on a zip code for now
# Default is Boulder CO.
def _get_woeid2( lat, long ):
  # Reference: https://developer.yahoo.com/weather/
  baseurl = "https://query.yahooapis.com/v1/public/yql?"
  yql_query = "select * from geo.places where text=\"(" + str( lat ) + ", " + str( long ) + ")\"" 
  yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
  result = urllib2.urlopen(yql_url).read()
  data = json.loads(result)
  return data['query']['results']['place']['woeid']


#  return data['query']['place']['content'][0]['woeid']


def scan_for_ip( file = './data/devops_coding_input_log1.tsv', max_num_ip = -1 ):
  ip_list = []

  # Pandas.pydata.org would be better but to keep this simple just use brute force column parsing
  with open( file, 'r' ) as ff:
    for line in ff.readlines():
      cells = line.split( '\t' )
      # assume cell 
      ip = cells[23]
      ip_list.append( ip )

      # limit the number of IP's read from file for testing purposes
      if max_num_ip > 0 and len(ip_list)  >= max_num_ip :
        break

  return ip_list


def report_histogram( temperatures, num_buckets = 5 ):
  assert( num_buckets > 1 )

  # A third party modules like numpy would be better if this use case becomes more complex 
  # Use standard modules for now to simplify deployment on other servers
  
  # Make sure all temperatures are int 
  temperatures = [int(x) for x in temperatures]

  max_temp = float( max(temperatures) )   
  min_temp = float( min(temperatures) )   
  assert( max_temp > min_temp )

  step = float( (max_temp - min_temp) / num_buckets )
  step = math.ceil( step )
  bucket_count = []

  # All temperatures can not be the same
  assert( abs(max_temp - min_temp) > ZERO_TOL )

  bottom = min_temp
  top = min_temp + step

  while bottom <= max_temp: 
    count = 0
    for temp in temperatures:
      temp = float( temp )
      if bottom <= temp and temp <= top:
        count = count + 1
       
    bottom = top + ZERO_TOL # avoid counting the same number twice
    top = top + step
      
    bucket_count.append( count )

  print "Requested buckets:", num_buckets 
  print bucket_count
  print sum( bucket_count ), "out of ", len( temperatures )

  # Check that every high tempertature is accounted for 
  assert( sum( bucket_count ) == len( temperatures ) )

  return bucket_count


def main():
  ip_list = scan_for_ip( )
  report_histogram( temperatures )

  fails = 0
  for ip in ip_list:
    try:
      high_temp = get_high_temp_from_ip( ip )
        
      print( "IP:",ip," Temp:" + str( high_temp ) )
      temperatures.append( high_temp )
    except:
      fails += 1
      print( ">>>>>ip failrure: " + str( ip ) )


  report_histogram( temperatures )

  print( "Done total failures: "  + str( fails ) )

