import psutil
import socket
import time
from datetime import timedelta


import os
import psutil

def get_disk_info(path):
    if not os.path.ismount(path):
        return None

    usage = psutil.disk_usage(path)

    return {
        "path": path,
        "used": round(usage.used / (1024**3), 2),
        "total": round(usage.total / (1024**3), 2),
        "free": round(usage.free / (1024**3), 2),
        "percent": usage.percent,
    }

disks = {
    "server": get_disk_info("/"),
    "hdd1": get_disk_info("/mnt/old_hdd/hdd1"),
    "hdd2": get_disk_info("/mnt/old_hdd/hdd2"),
    "hdd3": get_disk_info("/mnt/old_hdd/hdd3"),
}


def get_system_status():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return {
        "hostname": socket.gethostname(),

        "cpu_percent": psutil.cpu_percent(interval=0.5),

        "memory_percent": memory.percent,
        "memory_used": round(memory.used / (1024**3),2),
        "memory_total": round(memory.total / (1024**3),2),

        "disks" : disks,

        "disk_percent": disk.percent,
        "disk_used": round(disk.used/(1024**3),2),
        "disk_total": round(disk.total/(1024**3),2),

        "uptime": str(timedelta(seconds=int(time.time()-psutil.boot_time())))
    }