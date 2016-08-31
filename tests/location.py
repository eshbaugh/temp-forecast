#!/usr/bin/python
# make sure to invoke this test from the root directory - ./tests/parse.py

execfile("forecast.py")

woeid = _get_woeid2( 39.9135737, -105.01548269999999 )

print woeid
