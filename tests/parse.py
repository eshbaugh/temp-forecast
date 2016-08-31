#!/usr/bin/python
# make sure to invoke this test from the root directory - ./tests/parse.py

OUTFILE = 'data/ip_list.tsv'
INFILE = 'data/devops_coding_input_log1.tsv'
MAX_SIZE = 99999
MAX_SIZE = 300

execfile("forecast.py")

ip_list = scan_for_ip( INFILE, MAX_SIZE )

ff = open( OUTFILE, 'w' )
for ip in ip_list:
  ff.write( ip + '\n' )
ff.close()

print "Status:", len( ip_list ), "IPs written to file", OUTFILE 
