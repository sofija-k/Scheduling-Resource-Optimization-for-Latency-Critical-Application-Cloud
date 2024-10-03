from time import sleep

import psutil
import subprocess
import Scheduler
import Scheduler_logger
import math
import sys

class MemcachedController:

    def __init__(self, logger, number_of_cores, low_threshold, high_threshold, qps_interval):
        self.number_of_cores = number_of_cores
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.logger = logger
        self.pid = 0
        self.low_qps = 0
        self.high_qps = 0
        self.loop_counter = math.ceil(44.6023*(0.8392**qps_interval))
        print(self.loop_counter)

        for process in psutil.process_iter():
            if "memcache" in process.name():
                self.pid = process.pid
                break

        self.logger.job_start("memcached", "0,1", "2")
        self.call_taskset("0,1")

        # First output wrong
        psutil.cpu_percent(interval=None, percpu=True)

    def run(self):
        usage = psutil.cpu_percent(interval=None, percpu=True)
        print(usage)
        summed = sum(usage[:self.number_of_cores])
        if self.number_of_cores == 1 and summed >= self.low_threshold:
            self.high_qps = 1
            #if self.low_qps >= 5:
            self.number_of_cores = 2
            cpu_number = "0,1"
            self.call_taskset(cpu_number)
            # else:
            #     self.low_qps += 1
        elif self.number_of_cores == 2 and summed <= self.high_threshold:
            #self.low_qps = 1

            if self.high_qps >= self.loop_counter:
                self.number_of_cores = 1
                cpu_number = "0"
                self.call_taskset(cpu_number)
            else:
                self.high_qps += 1
            #self.number_of_cores = 1
            #cpu_number = "0"
            #self.call_taskset(cpu_number)
        else:
            #self.low_qps = 5
            self.high_qps = 1

    def call_taskset(self, cpu_number):
        command = f"sudo taskset -a -cp {cpu_number} {self.pid}"
        self.logger.update_cores("memcached", cpu_number)
        subprocess.run(command.split(" "))


def main():
    print("Hello")
    qps_interval = int(sys.argv[1])
    logger = Scheduler_logger.SchedulerLogger()
    memcached_server = MemcachedController(logger, 2, 60, 60, qps_interval)
    controller_jobs = Scheduler.DockerController(logger)


    while True:
        #usage = psutil.cpu_percent(interval=None, percpu=True)
        #print(usage)
        memcached_server.run()
        if controller_jobs.update(memcached_server.number_of_cores):
            break
        sleep(0.25)
    controller_jobs.end_scheduler()


if __name__ == "__main__":
    main()
