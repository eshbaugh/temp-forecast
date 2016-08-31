#!/usr/bin/python
# make sure to invoke this test from the root directory - ./tests/temperature.py

INFILE = 'data/temperature_list_short.tsv'
OUTFILE = 'data/histogram_report_test.tmp'

execfile("forecast.py")

ff = open( INFILE, 'r' )
temperatures = ff.read().splitlines()
ff.close() 

_report_histogram( temperatures, OUTFILE, 5 )
