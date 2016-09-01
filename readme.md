# Temperature Forcast
This Python module will read the IP addresses from the input file .tsv file and using the Yahoo weather 
service determine the weather forecast for tomorrow in that region.  The output is another .tsv file 
that contains histogram data of the frequency of occurrence for each temperature with the range defined 
by each specific histogram buckets. The number of histogram buckets along with the max number of IPs to 
be checked is configurable from the command line. 

### Usage
To except all default values
- Linux: ./forecast.py 
- Windows: 
  - cd c:\location of the script
  - c:\Python27\python.exe .\forecast.py

Additional arguments

forecast.py [input file] [output file] [histogram buckets] [max records]
- input file: Tab-separated data file with the 24th column containing IP addresses
- output file: Location of the file that will be created and contain the output of the histogram buckets
- Histogram buckets: The number of categories to sort temperature counts into
- max records: Limits the number of items read from the input file, default is unlimited.

To display command help

forecast.py -h 

### TODO 
* parse argements DONE
* create an ouptut tsv file
* Error Checking
* Log File
* create readme WIP
* cleanup code
* Class / modules?


### Further Development 
- Performance tune: Currently it can take a few hours to run 4000 records, speed will become prohibitive with 40,000 ++
  - Identify top time takers, my guess is it is the REST calls
  - Use specific sql selects instead of *
  - Research performance of paid weather services
  - ...
- Modularize to maximize code reuse once use cases are fully understood.



### Reference Links

- WOEID lookup: http://www.zazar.net/developers/jquery/zweatherfeed/example_location.html
- Yahoo API Docs: 
  - https://developer.yahoo.com/yql/console/#h=select+*+from+geo.places+where+text%3D%2280234%22
  - https://developer.yahoo.com/weather/
