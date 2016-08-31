#!/usr/bin/python
# make sure to invoke this test from the root directory - ./tests/temperature.py

INFILE = 'data/ip_list_short.tsv'
OUTFILE = 'data/temperature_test.tmp'

execfile("forecast.py")

ff = open( INFILE, 'r' )
ip_list = ff.read().splitlines()
ff.close()

ff = open( OUTFILE, 'w' )
fails = 0
passes = 0
for ip in ip_list:
  try: 
    geo_loc = _get_location( ip )
    woeid = _get_woeid( geo_loc[0], geo_loc[1] )
    high_temp = _get_tomorrows_high_temp( woeid )

    print( "IP:",ip," Temp:" + str( high_temp ) )
    ff.write( high_temp + '\n' )
    passes += 1
  except:
    fails = fails + 1
    print( ">>>>>ip failrure: " + str( ip ) )
ff.close()

print "Status:", passes, "Temperatures written to file", OUTFILE 
print "Failed to get temperature for", fails, "IP addresses"

