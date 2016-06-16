import splunklib.client as client
import os, sys
import time
import splunklib.results as results
import urllib
import urllib2
import collections
import itertools
import threading

# ============================ Functions ============================

def change_key(dict, old, new):
   for i in range(len(dict)):
    k, v = dict.popitem(False)
    dict[new if old == k else k] = v

# ============================ Create Splunk Enterprise Service instance, log in & run query ============================

print "Hello! Welcome to the Splunk cmdb search and data extraction program."

# Try, except, finally didn't seem to work for error checking - fix up!
SCHEME = str(raw_input("Please enter in the scheme of the URL (http or https): "))
HOST = str(raw_input("Thanks, now enter in the host name (e.g. splunk.cloud.***.com): "))
USERNAME = str(raw_input("What is your username? "))
PASSWORD = str(raw_input("Lastly, I need your password: "))
PORT = ****

service = client.connect(host=HOST, port=PORT, scheme=SCHEME, username=USERNAME, password=PASSWORD)
print "Perfect, you're in!"

searchquery_normal = str(raw_input("Now you can paste your search query. Make sure macros have been broken down, and just right click to paste: "))
#search index = ...
kwargs_normalsearch = {"exec_mode": "normal"}
job = service.jobs.create(searchquery_normal, **kwargs_normalsearch)

print "Thanks! Please wait a moment."


# ============================ Running ============================

#Open file to dump results to
f = open("searchresults.txt", "w")

# Normal search returns the job's SID right away, need to poll for completion
while True:
    while not job.is_ready():
        pass
    stats = {"isDone": job["isDone"],
             "doneProgress": float(job["doneProgress"])*100,
              "scanCount": int(job["scanCount"]),
              "eventCount": int(job["eventCount"]),
              "resultCount": int(job["resultCount"])}

    status = ("\r%(doneProgress)03.1f%%   %(scanCount)d scanned   "
              "%(eventCount)d matched   %(resultCount)d results") % stats

    sys.stdout.write(status)
    sys.stdout.flush()
    if stats["isDone"] == "1":
        sys.stdout.write("\n\nDone! Please take a look at the searchresults text file. \n\n")
        break
    time.sleep(2)

# ============================ Get the results ============================

reader = results.ResultsReader(job.results())
for result in reader:

  #print ("%s \n") % result   
  f.write("%s\n" % result)

  # ============================ Configure dictionary with results ============================

  length = len(result)

  for i in range (0, length):

    """ 
    FORMATTING FOR COMMAND LINE DISPLAY OF URL'S

    url = key + "=" + value

    if key != result.keys()[length - 1]:
      print url + "&",
      sys.stdout.softspace = 0
    else:
      print url + "\n\n"

    """

    # Rename keys using function for db compatibility 
    change_key(result, 'cloud', 'cl')

  # ============================ Pass in values to encode URL for webservice ============================
  params = urllib.urlencode(result)
  params = str(params)

  # ============================ Attach string and send HTTP Request ============================
  URL = "*******"
  full_URL = URL + "*******" + params
  
  data = urllib2.urlopen(full_URL)
  
f.close()

# ============================ Displaying search date and time, renaming file with timestamp ============================
timestr = time.strftime("%Y-%m-%d--%H-%M-%S")
print "%s" % (timestr + "\n")
timestamp = "searchresults_" + timestr + ".txt"

os.rename("searchresults.txt", timestamp)

print "\nSQL inserts completed. Check web service for information."

#Close job
job.cancel()   
sys.stdout.write('\n')


#Written by Vishaal Shah-Chittur
