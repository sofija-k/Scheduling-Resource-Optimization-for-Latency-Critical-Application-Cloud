import psutil
import time

cores = 2

while True:
    usage = psutil.cpu_percent(interval=5, percpu=True)
    summed = sum(usage[:cores])
    print(int(time.time()))
    print(summed)