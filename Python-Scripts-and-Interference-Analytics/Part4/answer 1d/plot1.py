import csv
import numpy as np
import matplotlib.pyplot as plt

numbers = [1, 2]

def read_latency(test: str):
    file = open("T2_C" + str(test) + "_memcache2.csv")
    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)
    file.close()
    p95 = 0
    qps = 0
    ts_start = 0
    ts_end = 0
    for i in range(0, len(header)):
        if header[i] == "p95":
            p95 = i
        if header[i] == "QPS":
            qps = i
        if header[i] == "ts_start":
            ts_start = i
        if header[i] == "ts_end":
            ts_end = i
    p95_list = []
    qps_list = []
    ts_start_list = []
    ts_end_list = []
    for row in rows:
        p95_list.append(float(row[p95])/1000.0)
        qps_list.append(float(row[qps])/1000.0)
        ts_start_list.append(int(row[ts_start][:-3]))
        ts_end_list.append(int(row[ts_end][:-3]))
    return p95_list, qps_list, ts_start_list, ts_end_list

def read_cpu(test: str):
    file = open("T2_C" + str(test) + "_cpu2.txt")
    times = []
    percentage = []
    while True:
        line = file.readline()
        if not line:
            break
        times.append(int(line[:-1]))
        line = file.readline()
        percentage.append(float(line[:-2])*4)
    return times, percentage

plt.style.use('fast')
plt.rc('axes', labelsize=20)
plt.rcParams["figure.figsize"] = [15.50, 13.50]
plt.rcParams["figure.autolayout"] = True
plt.rc('xtick', labelsize=13)
plt.rc('ytick', labelsize=15)
#lat1 = fig.subplots(1, 1)
fig, lat1 = plt.subplots()
plt.title("1 core - 2 threads", fontsize=23)

lat1color='tab:blue'
cpu1color='tab:orange'

lat1.set_xlabel("Queries Per Second")
lat1.set_ylabel("Tail latency [ms]")
#lat1.set_ylabel("Tail latency [ms]", rotation='horizontal', horizontalalignment='left', y=1.0)
lat1.set_xlim([0, 130])
lat1.set_ylim([0, 2])
ticks = [str(i) + 'K' for i in range(5, 130, 5)]
lat1.tick_params(axis='y', labelcolor=lat1color)
ticks.insert(0, '0')
lat1.set_xticks([i for i in range(0, 130, 5)])
lat1.set_xticklabels(ticks)
lat1.hlines(1, 0, 130, colors="black", linestyles='dotted')

p95, qps, ts_start, ts_end = read_latency('1')
lat1.plot(qps, p95, '-o', label="Tail latency", color=lat1color)
times, percentage = read_cpu('1')
percentages = []
for i in range(0, len(qps)):
    percentages.append([])
for i in range(0, len(times)):
    for j in range(0, len(ts_start)):
        if times[i] >= ts_start[j] and times[i] <= ts_end[j]:
            percentages[j].append(percentage[i])
cpu1 = lat1.twinx()

cpu1.set_xlabel("Queries Per Second")
cpu1.set_ylabel("CPU Utilization %")
#cpu1.set_ylabel("CPU Utilization", rotation='horizontal', horizontalalignment='left', y=1.0, labelpad=10)
cpu1.set_xlim([0, 130])
cpu1.set_ylim([0, 100])
ticks = [str(i) + 'K' for i in range(5, 130, 5)]
cpu1.tick_params(axis='y', labelcolor=cpu1color)
ticks.insert(0, '0')
cpu1.set_xticks([i for i in range(0, 130, 5)])
cpu1.set_xticklabels(ticks)

percentage_axis = [np.mean(percentages[i]) for i in range(0, len(percentages))]
cpu1.plot(qps, percentage_axis, '-o', color=cpu1color, label="CPU Utilization")

plt.tight_layout()
#plt.legend(loc='lower right', fontsize=20)
lat1.legend(loc='upper left', fontsize=20)
cpu1.legend(loc='upper right', fontsize=20)
plt.savefig('part4_question1d.pdf')
#plt.show()
plt.close()