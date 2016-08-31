#!/usr/bin/python
# make sure to invoke this test from the root directory - ./tests/parse.py

INFILE = 'data/devops_coding_input_short.tsv'
OUTFILE = 'data/ip_list_test.tmp'
MAX_SIZE = 99999

execfile("forecast.py")

ip_list = _scan_for_ip( INFILE, MAX_SIZE )

ff = open( OUTFILE, 'w' )
for ip in ip_list:
  ff.write( ip + '\n' )
ff.close()

print "Status:", len( ip_list ), "IPs written to file", OUTFILE 
