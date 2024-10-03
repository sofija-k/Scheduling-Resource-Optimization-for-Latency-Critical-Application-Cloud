import matplotlib.pyplot as plt
import datetime

number_run = 6
qps_interval = 5

def read_jobs():
    jobs = dict()
    with open("jobs_" + str(number_run) + ".txt", 'r') as file:
        for line in file:
            elements = line.split()
            timestamp = elements[0]
            event = elements[1]
            job = elements[2]
            if event == "start":
                jobs[job] = []
                jobs[job].append(int(datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f").timestamp()) + 3600*2)
            if event == "end":
                jobs[job].append(int(datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f").timestamp()) + 3600*2)
    return jobs

def read_mcperf():
    timestamp_start = 0
    timestamp_end = 0
    table = []
    with open("mcperf_" + str(number_run) + ".txt", 'r') as file:
        for line in file:
            elements = line.split()
            if len(elements) > 2:
                if elements[0] == 'Timestamp' and elements[1] == 'start:':
                    timestamp_start = int(elements[2]) // 1000
                elif elements[0] == 'Timestamp' and elements[1] == 'end:':
                    timestamp_end = int(elements[2]) // 1000
            if len(elements) == 18:
                table.append(elements)
    return timestamp_start, timestamp_end, table

def read_table(table):
    header = table[0]
    p95 = 0
    qps = 0
    for i in range(0, len(header)):
        if header[i] == "p95":
            p95 = i
        if header[i] == "QPS":
            qps = i
    p95_list = []
    qps_list = []
    ts_start_list = []
    ts_end_list = []
    for i in range(1, len(table)):
        p95_list.append(float(table[i][p95])/1000.0)
        qps_list.append(float(table[i][qps])/1000.0)
        ts_start_list.append((i-1)*qps_interval)
        ts_end_list.append(i*qps_interval)
    return p95_list, qps_list, ts_start_list, ts_end_list
                
jobs = read_jobs()
timestamp_start, timestamp_end, table = read_mcperf()
end = jobs['scheduler'][1] - timestamp_start
del jobs['scheduler']
del jobs['memcached']

for el in jobs.values():
    el[0] -= timestamp_start
    el[1] -= timestamp_start
timestamp_start -= timestamp_start
p95_list, qps_list, ts_start_list, ts_end_list = read_table(table)

print(jobs)
print(timestamp_start)
print(timestamp_end)
for i in range(len(p95_list)-1, -1, -1):
    if ts_start_list[i] > end + 60:
        del p95_list[i]
        del qps_list[i]
        del ts_start_list[i]
        del ts_end_list[i]
for i in range(0, len(p95_list)):
    print("QPS: " + str(qps_list[i]) + ", p95: " + str(p95_list[i]) + ", start: ", str(ts_start_list[i]) + ", end: ", str(ts_end_list[i]))

plt.rcParams["figure.autolayout"] = True
plt.rcParams["figure.figsize"] = [12.50, 7.50]
fig = plt.figure()
main, jobs_plt = fig.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]})

main.set_xlabel("Time [s]")
main.set_ylabel("Tail latency [ms]")
main.set_xlim([0, end+60])
main.set_ylim([0, 2])
main.tick_params(axis='y', labelcolor="#1f77b4")
main.hlines(1, 0, end+60, colors="black", linestyles='dotted')
avg_time = [(ts_start_list[i] + ts_end_list[i]) / 2 for i in range(0, len(ts_end_list))]

main.plot(avg_time, p95_list, '-o', label="Tail latency", color="#1f77b4")

#main.bar(ts_start_list, p95_list, 10, 0, align='edge', color='g', alpha=0.2)

qps = main.twinx()
qps.set_ylabel("Queries Per Second")
qps.set_xlim([0, end+60])
qps.set_ylim([0, 110])
ticks = [str(i) + 'K' for i in range(5, 110, 5)]
ticks.insert(0, '0')
qps.set_yticks([i for i in range(0, 110, 5)])
qps.set_yticklabels(ticks)
qps.bar(ts_start_list, qps_list, qps_interval, 0, align='edge', alpha=0.2, color='#2ca02c', edgecolor='black', label="Queries Per Second")
qps.tick_params(axis='y', labelcolor="#2ca02c")

main.set_zorder(10)
main.patch.set_visible(False)

colors = dict()
colors["blackscholes"] = '#CCA000'
colors["canneal"] = '#CCCCAA'
colors["dedup"] = '#CCACCA'
colors["ferret"] = '#AACCCA'
colors["freqmine"] = '#0CCA00'
colors["radix"] = '#00CCA0'
colors["vips"] = '#CC0A00'

jobs_plt.set_xlim([0, end + 60])
jobs_plt.set_xlabel("Time [s]")
for job in jobs.keys():
    jobs_plt.plot([jobs[job][0], jobs[job][1]], [job, job], '-o', linewidth=3, color=colors[job])

plt.tight_layout()
main.legend(loc='upper left', fontsize=10)
qps.legend(loc='upper right', fontsize=10)

plt.show()
plt.close()