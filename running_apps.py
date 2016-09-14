import splunklib.client as client
import sys
from time import sleep
import splunklib.results as results

HOST = "splunk.cloud.***.com"
PORT = ****
SCHEME = "https"
USERNAME = "*******"
PASSWORD = "*******"

# Create a Splunk Enterprise Service instance and log in 
service = client.connect(host=HOST, port=PORT, scheme=SCHEME, username=USERNAME, password=PASSWORD)

"""
# Print installed apps to the console to verify login
for app in service.apps:
    print app.name
"""
###############################################################################################################

searchquery_normal = "search * | head 10"
kwargs_normalsearch = {"exec_mode": "normal"}
job = service.jobs.create(searchquery_normal, **kwargs_normalsearch)

# A normal search returns the job's SID right away, so we need to poll for completion
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
        sys.stdout.write("\n\nDone!\n\n")
        break
    sleep(2)


# Get the results and display them
for result in results.ResultsReader(job.results()):
	print result

f.close()

job.cancel()   
sys.stdout.write('\n')
