#!/usr/bin/python
# make sure to invoke this test from the root directory - ./tests/temperature.py

INFILE = 'data/ip_list.tsv'
OUTFILE = 'data/temperature_list.tsv'

execfile("forecast.py")

ff = open( INFILE, 'r' )
ip_list = ff.read().splitlines()
ff.close()

ff = open( OUTFILE, 'w' )
fails = 0
passes = 0
for ip in ip_list:
  try: 
    high_temp = get_high_temp_from_ip( ip )

    #print( "IP:",ip," Temp:" + str( high_temp ) )
    ff.write( high_temp + '\n' )
    passes += 1
  except:
    fails = fails + 1
    print( ">>>>>ip failrure: " + str( ip ) )
ff.close()

print "Status:", passes, "Temperatures written to file", OUTFILE 
print "Failed to get temperature for", fails, "IP addresses"

