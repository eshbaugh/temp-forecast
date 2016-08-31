# Temperature Forcast
This Python module will read the IP addresses from the 24th column in the input file .tsv file and using the Yahoo weather service determine the weather forecast for tomorrow in that region.  The output is another .tsv file that contains histogram data of the frequency of occurrence for each temperature with the range defined by each specific histogram buckets. The number of histogram buckets along with the max number of IPs to be checked is configurable from the command line. 

### Usage
To except all default values
- Linux: ./forecast.py 
- Windows: c:\Python27\python.exe c:\<location of script>\forecast.py

Additional arguments
forecast.py [input file] [output file] [histogram buckets] [max records]
- input file: Tab-separated data file with the 24th column containing IP addresses
- output file: Location of the file that will be created and contain the output of the histogram buckets
- Histogram buckets: The number of categories between the minimum and maximum temperature to place counts of the temperatures in that range.
- max records: Limits the number of items read from the input file, default is unlimited.

### TODO 
* parse argements DONE
* create an ouptut tsv file
* create readme
* cleanup code
* Class / modules?


### Further Development 


### Reference Links

- WOEID lookup: http://www.zazar.net/developers/jquery/zweatherfeed/example_location.html
- Yahoo API Docs: 
  - https://developer.yahoo.com/yql/console/#h=select+*+from+geo.places+where+text%3D%2280234%22
  - https://developer.yahoo.com/weather/
