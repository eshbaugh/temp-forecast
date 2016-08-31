#!/usr/bin/python
# make sure to invoke this test from the root directory - ./tests/parse.py

execfile("forecast.py")



INFILE = 'data/ip_list.tsv'

ff = open( INFILE, 'r' )
ip_list = ff.read().splitlines()
ff.close()

for ip in ip_list:
  geo_loc = _get_location2( ip )
  woeid = _get_woeid2( geo_loc[0], geo_loc[1] )
  high_temp = _get_tomorrows_high_temp( woeid )
  print high_temp
