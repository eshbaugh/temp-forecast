#!/usr/bin/python

"""a Python module that parses a file for IP addresses and creates a histogram data for tomorrow's high temps

Methods
  _scan_for_ip: Scan the passed file and return a list of IPs listed in column 24 
  _validate_ip_list: Removes any invalid or incorrectly formated IP addresses from the list
  _get_location: Obtain the latitude and longitude from an IP address
  _get_woeid: Obtain the woeid using the latitude and longitude
  _get_tomorrows_high_temperature: Get tomorrow's high temperature for the Where On Earth ID (woeid) location
  _report_histogram: Output the number of temperatures in each histogram bucket to a .tsv file format 
  main: The orchestrator for this method

About / troubleshooting:
  This module was built and tested with Python 2.7.11 on Ubuntu Linux. 
""" 

try: 
  import urllib, urllib2
  import json
  import csv
  import sys
  import math
  import argparse
  import time
  import socket
except ImportError as err_str:
  print( "{}, make sure this module exists on your server".format(err_str) ) 
  exit()


def _scan_for_ip( in_file, max_num_ip = -1 ):
  ip_list = []

  # Pandas.pydata.org would be better but to keep this simple just use brute force column parsing
  with open( in_file, 'r' ) as ff:
    for line in ff.readlines():
      cells = line.split( '\t' )
      # assume cell 
      ip = cells[23]
      ip_list.append( ip )

      # limit the number of IP's read from file for testing purposes
      if max_num_ip > 0 and len(ip_list)  >= max_num_ip :
        break

  return ip_list


def _validate_ip_list( ip_list ):
  error_count = 0

  out_list = []

  for ip in ip_list:
    try:
      socket.inet_aton( ip )
    except:
      print "Error:invalid IP address:", ip
      error_count += 1
    else:
      out_list.append( ip )

  return (out_list, error_count)


def _get_location( ip, service = 'http://ip-api.com/json/' ):
  location = urllib.urlopen( service + ip ).read()
  location_json = json.loads( location )

  if location_json['status'] == 'fail':
    raise Exception("Error:Unable to determine a location for IP:" + ip)

  geo_loc = []
  geo_loc.append( location_json['lat'] )
  geo_loc.append( location_json['lon'] )
  return geo_loc


def _get_woeid( lat, long ):
  # Reference: https://developer.yahoo.com/weather/
  baseurl = "https://query.yahooapis.com/v1/public/yql?"
  yql_query = "select * from geo.places where text=\"(" + str( lat ) + ", " + str( long ) + ")\"" 
  yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
  result = urllib2.urlopen(yql_url).read()
  data = json.loads(result)
  return data['query']['results']['place']['woeid']


def _get_tomorrows_high_temp( woeid = 2367231 ):
  # Reference: https://developer.yahoo.com/weather/
  baseurl = "https://query.yahooapis.com/v1/public/yql?"
  yql_query = "select * from weather.forecast where woeid=" + str( woeid )
  yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
  result = urllib2.urlopen(yql_url).read()
  data = json.loads(result)

  return data['query']['results']['channel']['item']['forecast'][1]['high']
  

def _report_histogram( temperatures, outfile, num_buckets = 5 ):
  ZERO_TOL = .1

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
  buckets = []

  # All temperatures can not be the same
  assert( abs(max_temp - min_temp) > ZERO_TOL )

  bottom = min_temp
  top = min_temp + step

  total = 0
  while bottom <= max_temp: 
    count = 0
    for temp in temperatures:
      temp = float( temp )
      if bottom <= temp and temp <= top:
        count += 1
        total += 1
       
    item = [bottom, top, count]
    buckets.append( item )

    bottom = top + ZERO_TOL # avoid counting the same number twice
    top = top + step
      
  ff = open( outfile, 'w' )
  ff.write( "BucketMin\tBucketMax\tcount\n" )

  for item in buckets:
    out_str = str(item[0]) + "\t" + str(item[1]) + "\t" + str(item[2]) + "\n"
    ff.write( out_str )

  ff.close()

  # All tempertatures are accounted for 
  assert( total == len( temperatures ) )

  return total


def main( in_file, out_file, buckets, max_records ):
  print "Starting processing at time: " + time.strftime( "%H:%M:%S" )

  try:
    ip_list = _scan_for_ip( in_file, max_records )
  except Exception as error:
    print error 
    exit()

  total_records = len( ip_list )

  ip_list, bad_ips = _validate_ip_list( ip_list )

  print "Obtaining next day forcast for", len(ip_list), " IP addresses"

  if bad_ips > 0:
    percent_bad = (float(bad_ips) / float(total_records)) * 100.0
    print "Invalid IP addresses encountered:", bad_ips, "({:3.1f}%)".format(percent_bad)

  temperatures=[]

  bad_locations = 0
  bad_woeids = 0
  bad_weather = 0 # :-)

  for ip in ip_list:
    # makeshift progress meter
    sys.stdout.write('.')
    sys.stdout.flush()
    
    try:
      geo_loc = _get_location( ip )
    except Exception as error:
      bad_locations += 1
      print error 
      continue

    try:
      woeid = _get_woeid( geo_loc[0], geo_loc[1] )
    except Exception as error:
      bad_woeids += 1
      print error 
      continue
    
    try: 
      high_temp = _get_tomorrows_high_temp( woeid )
    except Exception as error:
      bad_weather += 1
      print error 
      continue

    temperatures.append( high_temp )

  print "\nDone processing at time: " + time.strftime( "%H:%M:%S" )

  if bad_locations > 0:
    percent_bad = (float(bad_locations) / float(total_records)) * 100.0
    print "Unable to determin locations for", bad_locations, "({:3.1f}%) of records".format(percent_bad)

  if bad_woeids > 0:
    percent_bad = (float(bad_woeids) / float(total_records)) * 100.0
    print "Unable to determine WOEID locations for", bad_woeids, "({:3.1f}%) of records".format(percent_bad)

  if bad_weather > 0:
    percent_bad = (float(bad_weather) / float(total_records)) * 100.0
    print "Unable to determine weather for", bad_weather, "({:3.1f}%) of records".format(percent_bad)

  total_processed = _report_histogram( temperatures, out_file, buckets )

  succeed_count = len( temperatures )

  print "Successfully processed", succeed_count, "records out of", total_records, "ip addresses scanned"
  print "View", out_file, "for histogram results"
  print "Total failures: " + str( bad_ips + bad_locations + bad_woeids + bad_weather ) 


# Process command line arguments and call the main method
parser = argparse.ArgumentParser( description='Find tomorrows high temperature for regions specified by IPs')
parser.add_argument( 'input_filename', metavar = 'infile', type = str, nargs='?', default = './data/devops_coding_input_log1.tsv', help='Input filename' ) 
parser.add_argument( 'output_filename', metavar = 'outfile', type = str, nargs='?', default = './data/output.tsv', help='Output filename' ) 
parser.add_argument( 'buckets', metavar = 'histogram', type = int, nargs='?', default = 5, help='Number of histogram buckets: default 5' ) 
parser.add_argument( 'max_records', metavar = 'maxrecords', type = int, nargs='?', default = -1, help='Maximum number of records processed: default unlimited' ) 
args = parser.parse_args( )


main( args.input_filename, args.output_filename, args.buckets, args.max_records )
