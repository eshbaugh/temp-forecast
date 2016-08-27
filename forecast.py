#!/usr/bin/python

import urllib

def get_location(ip):

  location = urllib.urlopen('http://ip-api.com/php/' + ip).read()
  print(location)


get_location('8.8.8.8')


