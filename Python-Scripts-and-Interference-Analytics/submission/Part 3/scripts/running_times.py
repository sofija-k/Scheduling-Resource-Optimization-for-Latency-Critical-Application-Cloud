import json
from datetime import datetime
import numpy as np
import sys

time_format = '%Y-%m-%dT%H:%M:%SZ'
jobs = dict()
jobs["total"] = []

for i in range(1, 4):
    file = open("Round_" + str(i) + "_New_Order/results.json", 'r')
    json_file = json.load(file)

    start_times = []
    completion_times = []
    for item in json_file['items']:
        name = item['status']['containerStatuses'][0]['name']
        print("Job: ", str(name))
        if str(name) != "memcached":
            try:
                if str(name) not in jobs.keys():
                    jobs[str(name)] = []
                start_time = datetime.strptime(
                        item['status']['containerStatuses'][0]['state']['terminated']['startedAt'],
                        time_format)
                completion_time = datetime.strptime(
                        item['status']['containerStatuses'][0]['state']['terminated']['finishedAt'],
                        time_format)
                print("Job time: ", completion_time - start_time)
                jobs[str(name)].append((completion_time - start_time).total_seconds())
                start_times.append(start_time)
                completion_times.append(completion_time)
            except KeyError:
                print("Job {0} has not completed....".format(name))
                sys.exit(0)

    if len(start_times) != 7 and len(completion_times) != 7:
        print("You haven't run all the PARSEC jobs. Exiting...")
        sys.exit(0)

    print("Total time: {0}".format(max(completion_times) - min(start_times)))
    jobs["total"].append((max(completion_times) - min(start_times)).total_seconds())

    file.close()

for k in jobs.keys():
    print(k + ":")
    print("mean: " + str(np.mean(jobs[k])) + " s")
    print("std: " + str(np.std(jobs[k])) + " s")
    print()
