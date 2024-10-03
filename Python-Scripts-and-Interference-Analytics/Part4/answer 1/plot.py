import csv
import numpy as np
import matplotlib.pyplot as plt

numbers = [1, 2, 3]

def read_microbenchmark3(test: str):
    p95_lists = []
    qps_lists = []
    for i in numbers:
        # file = open(interference + '_interference' + '.csv')
        file = open(test + '_run' + str(i) + '.csv')
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
    p95_std = [np.std(k) for k in zip(*p95_lists)]
    qps_std = [np.std(k) for k in zip(*qps_lists)]

    return p95_mean, qps_mean, p95_std, qps_std

tests = ['T1_C1', 'T1_C2', 'T2_C1', 'T2_C2']
label_test = dict()
label_test['T1_C1'] = "T=1 thread, C=1 core"
label_test['T1_C2'] = "T=1 thread, C=2 cores"
label_test['T2_C1'] = "T=2 threads, C=1 core"
label_test['T2_C2'] = "T=2 threads, C=2 cores"

plt.style.use('ggplot')
plt.rc('axes', labelsize=23)
plt.rcParams["figure.figsize"] = [18.50, 7.50]
plt.rcParams["figure.autolayout"] = True
plt.xlabel("Queries Per Second")
plt.ylabel("Tail latency [ms]", loc='top', rotation='horizontal')
plt.xlim([0, 130000])
plt.ylim([0, 4])
plt.yticks(range(0, 5), fontsize=16)
ticks = [str(i) + 'K' for i in range(5, 130, 5)]
ticks.insert(0, '0')
plt.xticks(ticks=range(0, 130000, 5000), labels=ticks, fontsize=16)
for test in tests:
    y, x, y_err, x_err = read_microbenchmark3(test)
    plt.errorbar(x, y, xerr=x_err, yerr=y_err, label=label_test[test], capsize=4, capthick=1.3, elinewidth=1.5, fmt='-o', mec='white', mew=.75)
    #plt.errorbar(x, y, xerr=x_err, yerr=y_err)
plt.legend(fontsize=17)
plt.savefig('part4_question1.pdf')
#plt.show()
plt.close()
