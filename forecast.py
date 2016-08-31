#!/usr/bin/python

"""a Python module that parces a file for IP addresses and creates a histogram data for tomorrows high temps

Classes:
  GeoWeather: Contains geographic and weather methods and utilities
  Log: Creates and manages log files
  Parse: Reads the source file and creates a list of IP addresses
  Histogram

Troubleshooting:
  This module was built and tested with Python 2.7.11 on Ubuntu Linux. 

""" 

try: 
  import urllib, urllib2
  import json
  import csv
  import math
  import argparse
except ImportError as err_str:
  print( "{}, make sure this module exists on your server".format(err_str) ) 
  exit()

# Constants
ZERO_TOL = .001



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


# Returns latitude and longitude for the passed IP
def _get_location( ip, service = 'http://ip-api.com/json/' ):
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
def _get_woeid( lat, long ):
  # Reference: https://developer.yahoo.com/weather/
  baseurl = "https://query.yahooapis.com/v1/public/yql?"
  yql_query = "select * from geo.places where text=\"(" + str( lat ) + ", " + str( long ) + ")\"" 
  yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
  result = urllib2.urlopen(yql_url).read()
  data = json.loads(result)
  return data['query']['results']['place']['woeid']


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


def main( in_file, out_file, buckets, max_records ):
  print in_file, out_file, buckets, max_records

  ip_list = scan_for_ip( in_file, max_records )

  temperatures=[]

  fails = 0
  for ip in ip_list:
    try:
      geo_loc = _get_location( ip )
      woeid = _get_woeid( geo_loc[0], geo_loc[1] )
      high_temp = _get_tomorrows_high_temp( woeid )
        
      print( "IP:",ip," Temp:" + str( high_temp ) )
      temperatures.append( high_temp )
    except:
      fails += 1
      print( ">>>>>ip failrure: " + str( ip ) )

  print temperatures
  report_histogram( temperatures )

  print( "Done total failures: "  + str( fails ) )


# Process command line arguments and call the main method
parser = argparse.ArgumentParser( description='Find tomorrows high temperature for regions specified by IPs')
parser.add_argument( 'input_filename', metavar = 'infile', type = str, nargs='?', default = './data/devops_coding_input_log1.tsv', help='Input filename' ) 
parser.add_argument( 'output_filename', metavar = 'outfile', type = str, nargs='?', default = './data/output.tsv', help='Output filename' ) 
parser.add_argument( 'buckets', metavar = 'histogram', type = int, nargs='?', default = 5, help='Number of histogram buckets: default 5' ) 
parser.add_argument( 'max_records', metavar = 'maxrecords', type = int, nargs='?', default = 5, help='Maximum number of records processed: default unlimited' ) 
args = parser.parse_args( )

main( args.input_filename, args.output_filename, args.buckets, args.max_records )
