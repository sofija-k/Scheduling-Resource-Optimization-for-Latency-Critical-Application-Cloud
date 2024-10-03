import datetime
import numpy as np


def read_jobs(number_run):
    jobs = dict()
    with open("jobs_" + number_run + ".txt", 'r') as file:
        for line in file:
            elements = line.split()
            timestamp = elements[0]
            event = elements[1]
            job = elements[2]
            if event == "start":
                jobs[job] = []
                jobs[job].append(
                    float(datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f").timestamp()) + 3600 * 2)
            if event == "end":
                jobs[job].append(
                    float(datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f").timestamp()) + 3600 * 2)
    print(jobs)
    return jobs


def read_mcperf(number_run):
    timestamp_start = 0
    timestamp_end = 0
    table = []
    with open("mcperf_" + number_run + ".txt", 'r') as file:
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
        p95_list.append(float(table[i][p95]) / 1000.0)
        qps_list.append(float(table[i][qps]) / 1000.0)
        ts_start_list.append((i - 1) * 10)
        ts_end_list.append(i * 10)
    return p95_list, qps_list, ts_start_list, ts_end_list

def clean_up_jobs(number_run):
    # jobs = read_jobs(number_run)
    # timestamp_start, timestamp_end, table = read_mcperf(number_run)
    # end = jobs['scheduler'][1] - timestamp_start
    # # del jobs['scheduler']
    # del jobs['memcached']
    #
    # for el in jobs.values():
    #     el[0] -= timestamp_start
    #     el[1] -= timestamp_start
    # timestamp_start -= timestamp_start
    # p95_list, qps_list, ts_start_list, ts_end_list = read_table(table)
    #
    # print(jobs)
    # print(timestamp_start)
    # print(timestamp_end)
    # for i in range(len(p95_list) - 1, -1, -1):
    #     if ts_start_list[i] > end + 60:
    #         del p95_list[i]
    #         del qps_list[i]
    #         del ts_start_list[i]
    #         del ts_end_list[i]
    # for i in range(0, len(p95_list)):
    #     print("QPS: " + str(qps_list[i]) + ", p95: " + str(p95_list[i]) + ", start: ", str(ts_start_list[i]) + ", end: ",
    #           str(ts_end_list[i]))
    # return jobs, p95_list, qps_list, ts_start_list, ts_end_list
    jobs = read_jobs(number_run)
    del jobs['memcached']
    for job in jobs.keys():
        print(job)
        jobs[job] = (jobs[job][1] -  jobs[job][0])
        print(jobs[job])

    return jobs

def main():
    number_of_files = 3
    interval_timing_of_run = ""

    jobs = dict()
    time_for_job = {"blackscholes": [],
                    "radix": [],
                    "canneal": [],
                    "freqmine": [],
                    "vips": [],
                    "dedup": [],
                    "ferret": [],
                    "scheduler": []}
    for index in range(4,7):
        jobs = clean_up_jobs(interval_timing_of_run + str(index))
        for name in time_for_job.keys():
            time_for_job[name].append(jobs[name])

    for name in time_for_job.keys():
        print(name + " mean is " + str(np.mean(time_for_job[name])) )
        print(name + " standard deviation " + str(np.std(time_for_job[name])))

    for index in range(4,7):
        timestamp_start, timestamp_end, table = read_mcperf(interval_timing_of_run + str(index))
        p95_list, qps_list, ts_start_list, ts_end_list = read_table(table)
        jobs = read_jobs(str(index))
        end = jobs['scheduler'][1] - timestamp_start
        print(jobs['scheduler'])
        print(ts_end_list)
        while ts_end_list[0] < jobs['scheduler'][0] - timestamp_start:
            del p95_list[0]
            del qps_list[0]
            del ts_start_list[0]
            del ts_end_list[0]
        for i in range(len(p95_list) - 1, -1, -1):
            if ts_start_list[i] > end:
                del p95_list[i]
                del qps_list[i]
                del ts_start_list[i]
                del ts_end_list[i]
        violate = 0
        for el in p95_list:
            if el >= 1:
                violate += 1
        print(str(index) + " run: " + str(violate / len(p95_list)))
        print(violate / len(p95_list))


if __name__ == "__main__":
    main()
