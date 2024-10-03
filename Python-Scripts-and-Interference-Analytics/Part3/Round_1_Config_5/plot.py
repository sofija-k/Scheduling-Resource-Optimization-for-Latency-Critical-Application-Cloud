import csv, json
import datetime
import sys
import matplotlib.pyplot as plt

file = open('memcache.csv')
csvreader = csv.reader(file)
header = []
header = next(csvreader)
rows = []
for row in csvreader:
    rows.append(row)
file.close()
p95 = 0
ts_start = 0
ts_end = 0
for i in range(0, len(header)):
    if header[i] == "p95":
        p95 = i
    if header[i] == "ts_start":
        ts_start = i
    if header[i] == "ts_end":
        ts_end = i
p95_list = []
ts_start_list = []
ts_end_list = []
for row in rows:
    p95_list.append(float(row[p95])/1000.0)
    ts_start_list.append(int(row[ts_start]))
    ts_end_list.append(int(row[ts_end]))

time_format = '%Y-%m-%dT%H:%M:%SZ'

file = open("results.json", 'r')
json_file = json.load(file)

jobs = []
start = []
completion = []

for item in json_file['items']:
    name = item['status']['containerStatuses'][0]['name']
    if str(name) != "memcached":
        try:
            jobs.append(str(name))
            start_time = datetime.datetime.strptime(
                    item['status']['containerStatuses'][0]['state']['terminated']['startedAt'],
                    time_format)
            completion_time = datetime.datetime.strptime(
                    item['status']['containerStatuses'][0]['state']['terminated']['finishedAt'],
                    time_format)
            start.append(datetime.datetime.timestamp(start_time)*1000 + 3600000*2)
            completion.append(datetime.datetime.timestamp(completion_time)*1000 + 3600000*2)
        except KeyError:
            print("Job {0} has not completed....".format(name))
            sys.exit(0)

file.close()

# normalize so that x = 0 for one value in start
minimum = min(start)
ts_start_list = [(x - minimum)/1000 for x in ts_start_list]
ts_end_list = [(x - minimum)/1000 for x in ts_end_list]
start = [(x - minimum)/1000 for x in start]
completion = [(x - minimum)/1000 for x in completion]

# remove unnecessary memcached values
for i in range(0, len(ts_start_list)):
    if ts_start_list[i] > 0:
        if i > 0:
            ts_start_list[i-1] = 0
            for j in range(0, i-1):
                del ts_start_list[0]
                del ts_end_list[0]
                del p95_list[0]
        else:
            ts_start_list[i] = 0
        break

maximum = max(completion)
for i in range(0, len(ts_end_list)):
    if ts_end_list[i] > maximum:
        num = len(ts_end_list)
        for j in range(0, num-i-1):
            del ts_start_list[-1]
            del ts_end_list[-1]
            del p95_list[0]
        break

colors = dict()
colors["parsec-blackscholes"] = '#CCA000'
colors["parsec-canneal"] = '#CCCCAA'
colors["parsec-dedup"] = '#CCACCA'
colors["parsec-ferret"] = '#AACCCA'
colors["parsec-freqmine"] = '#0CCA00'
colors["parsec-radix"] = '#00CCA0'
colors["parsec-vips"] = '#CC0A00'

labels = dict()
labels["parsec-blackscholes"] = ' (node-b-4core)'
labels["parsec-canneal"] = ' (node-c-8core)'
labels["parsec-dedup"] = ' (node-a-2core)'
labels["parsec-ferret"] = ' (node-b-4core)'
labels["parsec-freqmine"] = ' (node-c-8core)'
labels["parsec-radix"] = ' (node-a-2core)'
labels["parsec-vips"] = ' (node-a-2core)'

#plt.style.use('ggplot')
plt.style.use('seaborn-whitegrid')
plt.rcParams["figure.autolayout"] = True
plt.rcParams["figure.figsize"] = [10.50, 8.50]
fig = plt.figure()
bar, jobs_plt = fig.subplots(2, 1)

bar.set_xlabel("Time [s]")
bar.set_ylabel("Memcached p95 latency [ms]", loc='top', rotation='horizontal')
bar.set_xlim([0, 160])
bar.set_ylim([0, 1])
width = [ts_end_list[i] - ts_start_list[i] for i in range(0, len(ts_end_list))]
bar.bar(ts_start_list, p95_list, width, 0, align='edge', color='g')

jobs_plt.set_xlim([0, 160])
jobs_plt.set_xlabel("Time [s]")
for i in range(0, len(jobs)):
    jobs_plt.plot([start[i], completion[i]], [jobs[i] + labels[jobs[i]], jobs[i] + labels[jobs[i]]], '-o', color=colors[jobs[i]], linewidth=3)
    #jobs_plt.hlines(y=jobs[i], xmin=start[i], xmax=completion[i], colors=colors[jobs[i]], lw=4)
    #plot(x, y, color='green', marker='o', linestyle='dashed',

     #linewidth=2, markersize=12)

#fig.show()
plt.savefig('plot.pdf')
plt.close()