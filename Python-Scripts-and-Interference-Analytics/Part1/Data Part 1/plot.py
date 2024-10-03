import csv
import numpy as np
import matplotlib.pyplot as plt

def near(qps_list, p95_list, i):
    near = True
    if abs(qps_list[i+1] - qps_list[i]) > 500:
        near = False
    if abs(p95_list[i+1] - p95_list[i]) > 0.2:
        near = False
    return near

numbers = [1, 3, 4]

def read_microbenchmark1(interference: str):
    p95_lists = []
    qps_lists = []
    for i in numbers:
        # file = open(interference + '_interference' + '.csv')
        file = open(interference + '_interference' + str(i) + '.csv')
        csvreader = csv.reader(file)
        header = []
        header = next(csvreader)
        rows = []
        for row in csvreader:
            rows.append(row)
        file.close()
        p95 = 0
        qps = 0
        for i in range(0, len(header)):
            if header[i] == "p95":
                p95 = i
            if header[i] == "QPS":
                qps = i
        p95_list = []
        qps_list = []
        for row in rows:
            p95_list.append(float(row[p95])/1000.0)
            qps_list.append(float(row[qps]))
        p95_lists.append(p95_list)
        qps_lists.append(qps_list)
    p95_lists = [np.array(x) for x in p95_lists]
    qps_lists = [np.array(x) for x in qps_lists]
    p95_mean = [np.mean(k) for k in zip(*p95_lists)]
    qps_mean = [np.mean(k) for k in zip(*qps_lists)]
    p95_mean = [x for _, x in sorted(zip(qps_mean, p95_mean))]
    p95_std = [np.std(k) for k in zip(*p95_lists)]
    p95_std = [x for _, x in sorted(zip(qps_mean, p95_std))]
    qps_std = [np.std(k) for k in zip(*qps_lists)]
    qps_std = [x for _, x in sorted(zip(qps_mean, qps_std))]

    return p95_mean, qps_mean, p95_std, qps_std

def read_microbenchmark2(interference: str):
    p95_lists = []
    qps_lists = []
    for i in numbers:
        # file = open(interference + '_interference' + '.csv')
        file = open(interference + '_interference' + str(i) + '.csv')
        csvreader = csv.reader(file)
        header = []
        header = next(csvreader)
        rows = []
        for row in csvreader:
            rows.append(row)
        file.close()
        p95 = 0
        qps = 0
        for i in range(0, len(header)):
            if header[i] == "p95":
                p95 = i
            if header[i] == "QPS":
                qps = i
        p95_list = []
        qps_list = []
        for row in rows:
            p95_list.append(float(row[p95])/1000.0)
            qps_list.append(float(row[qps]))
        p95_list = [x for _, x in sorted(zip(qps_list, p95_list))]
        qps_list = sorted(qps_list)
        p95_lists.append(p95_list)
        qps_lists.append(qps_list)
    p95_lists = [np.array(x) for x in p95_lists]
    qps_lists = [np.array(x) for x in qps_lists]
    p95_mean = [np.mean(k) for k in zip(*p95_lists)]
    qps_mean = [np.mean(k) for k in zip(*qps_lists)]
    p95_std = [np.std(k) for k in zip(*p95_lists)]
    qps_std = [np.std(k) for k in zip(*qps_lists)]
    i = 0
    while i < len(p95_mean) - 1:
        if near(qps_mean, p95_mean, i):
            del p95_mean[i]
            del qps_mean[i]
            del p95_std[i]
            del qps_std[i]
            i -= 1
        i += 1

    return p95_mean, qps_mean, p95_std, qps_std

def read_microbenchmark3(interference: str):
    p95_lists = []
    qps_lists = []
    for i in numbers:
        # file = open(interference + '_interference' + '.csv')
        file = open(interference + '_interference' + str(i) + '.csv')
        csvreader = csv.reader(file)
        header = []
        header = next(csvreader)
        rows = []
        for row in csvreader:
            rows.append(row)
        file.close()
        p95 = 0
        qps = 0
        for i in range(0, len(header)):
            if header[i] == "p95":
                p95 = i
            if header[i] == "QPS":
                qps = i
        p95_list = []
        qps_list = []
        for row in rows:
            new_qps = float(row[qps])
            if len(qps_list) > 0:
                if new_qps < qps_list[-1]:
                    continue
            p95_list.append(float(row[p95])/1000.0)
            qps_list.append(float(row[qps]))
        p95_lists.append(p95_list)
        qps_lists.append(qps_list)
    p95_lists = [np.array(x) for x in p95_lists]
    qps_lists = [np.array(x) for x in qps_lists]
    p95_mean = [np.mean(k) for k in zip(*p95_lists)]
    qps_mean = [np.mean(k) for k in zip(*qps_lists)]
    p95_std = [np.std(k) for k in zip(*p95_lists)]
    qps_std = [np.std(k) for k in zip(*qps_lists)]

    return p95_mean, qps_mean, p95_std, qps_std

tests = ['no', 'cpu', 'l1d', 'l1i', 'l2', 'llc', 'membw']

plt.style.use('ggplot')
plt.rc('axes', labelsize=23)
plt.rcParams["figure.figsize"] = [17.50, 8.50]
plt.rcParams["figure.autolayout"] = True
plt.xlabel("Queries Per Second")
plt.ylabel("Tail latency [ms]", loc='top', rotation='horizontal')
plt.xlim([0, 110000])
plt.ylim([0, 8])
plt.yticks(range(0, 9), fontsize=16)
ticks = [str(i) + 'K' for i in range(5, 110, 5)]
ticks.insert(0, '0')
plt.xticks(ticks=range(0, 110000, 5000), labels=ticks, fontsize=16)
for test in tests:
    y, x, y_err, x_err = read_microbenchmark3(test)
    #plt.plot(x, y, label=test+" interference", marker='o')
    plt.errorbar(x, y, xerr=x_err, yerr=y_err, label=test+" interference", capsize=4, capthick=1.3, elinewidth=1.5, fmt='-o', mec='white', mew=.75)
    #plt.errorbar(x, y, xerr=x_err, yerr=y_err)
plt.legend(fontsize=17)
plt.savefig('part1.png')
#plt.show()
plt.close()
