# Temperature Forcast
This Python module will read the IP addresses from the 24th column in the input file .tsv file and using the the Yahoo weather service determine the weather forcast for tomorrow in that region.  The output is another .tsv file that contains histogram data of the frequence of occurence of each tempature with the range defined by each specific histogram buckets. The number of histogram buckets along with the max number of IPs to be checked is configurable from the command line. 

### Usage
To except all default values
* Linux: ./forecast.py 
* Windows: c:\Python27\python.exe c:\<location of script>\forecast.py

Additional arguments
forecast.py [input file] [output file] [histogram buckets] [max records]

### TODO 
* parse argements
* create an ouptut tsv file
* create readme
* cleanup code
* Class / modules?

### Useful Links

- WOEID lookup: http://www.zazar.net/developers/jquery/zweatherfeed/example_location.html
- Yahoo API Docs: 
  - https://developer.yahoo.com/yql/console/#h=select+*+from+geo.places+where+text%3D%2280234%22
  - https://developer.yahoo.com/weather/


