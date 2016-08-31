#!/usr/bin/python
# make sure to invoke this test from the root directory - ./tests/parse.py

execfile("forecast.py")

INFILE = 'data/ip_list_short.tsv'

ff = open( INFILE, 'r' )
ip_list = ff.read().splitlines()
ff.close()

fail_count = 0
pass_count = 0

print "Processing ip list"
for ip in ip_list:
  try:
    geo_loc = _get_location( ip )
    woeid = _get_woeid( geo_loc[0], geo_loc[1] )
    high_temp = _get_tomorrows_high_temp( woeid )
    print high_temp
    pass_count += 1
  except:
    print "Error-----"  
    fail_count += 1

print "Failures:", fail_count, " Passes:", pass_count, " Total: ", fail_count + pass_count
