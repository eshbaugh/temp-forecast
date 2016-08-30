#!/usr/bin/python
# make sure to invoke this test from the root directory - ./tests/temperature.py

INFILE = 'data/temperature_list.tsv'
OUTFILE = 'data/histogram_report.tsv'

execfile("forecast.py")

ff = open( INFILE, 'r' )
temperatures = ff.read().splitlines()
ff.close() 

report_histogram( temperatures, 5 )

