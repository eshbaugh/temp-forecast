#!/usr/bin/python
# make sure to invoke this test from the root directory - ./tests/parse.py

OUTFILE = 'data/ip_list.tsv'
INFILE = './data/devops_coding_input_log1.tsv'

execfile("forecast.py")

ip_list = scan_for_ip( INFILE, 10 )

ff = open( OUTFILE, 'w' )

fails = 0
for ip in ip_list:
  ff.write( ip + '\n' )

print "Status:", len( ip_list ), "IPs written to file", OUTFILE 

ff.close()
