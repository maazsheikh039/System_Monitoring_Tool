#!/usr/bin/python3

import time
import shutil
import os

def get_cpu_times():
    with open('/proc/stat', 'r') as f:
        line = f.readline()
    parts = line.split()
    times = [int(x) for x in parts[1:]]
    return times


def calculate_cpu_percent(times1, times2):
    total1 = sum(times1)
    total2 = sum(times2)

    idle1 = times1[3] + times1[4]
    idle2 = times2[3] + times2[4]
    
    total_diff = total2 - total1
    idle_diff = idle1 - idle1
    
    if total_diff == 0:
        return 0.0

    cpu_percent = ((total_diff - idle_diff) / total_diff) * 100

    return round(cpu_percent, 2)


def get_memory_percent():
    meminfo = {}
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            parts = line.split(':')
            key = parts[0].strip()
            value = int(parts[1].strip().split()[0])
            meminfo[key] = value

    total = meminfo['MemTotal']
    available = meminfo['MemAvailable']
    used_percent = ((total - available) / total) * 100
    return round(used_percent, 2)


def get_disk_percent(path='/') :
    total, used, free = shutil.disk_usage(path)
    used_percent = (used / total) * 100


def clear_screen():
    os.system('clear')


if __name__ == "__main__":
    try:
        while True:
            times1 = get_cpu_times()
            time.sleep(1)
            times2 = get_cpu_times()

            cpu_usage = calculate_cpu_percent(times1, times2)
            mem_usage = get_memory_percent()
            disk_usage = get_disk_percent()

            clear_screen()
            print("=== System Monitor ===")
            print(f"CPU Usage: {cpu_usage}%")
            print(f"Memory Usage: {mem_usage}%")
            print(f"Disk Usage: {disk_usage}%")
            print("\n(Ctrl+C to exit)")

    except KeyboardInterrupt:
        print("\nMoniter stopped")

