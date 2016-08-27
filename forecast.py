#!/usr/bin/python

import urllib
import json

def get_location(ip, service = 'http://ip-api.com/json/' ):

  print('------------')
  location = urllib.urlopen(service + ip).read()
  location_json = json.loads(location)
  print(location_json['city'])
  print(location_json['region'])
  print(location_json['countryCode'])

get_location('8.8.8.8')


