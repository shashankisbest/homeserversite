import psutil
import socket
import time
from datetime import timedelta
import mystorageroots

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

# disks = {
#     "server": get_disk_info("/"),
#     "hdd1": get_disk_info("/mnt/old_hdd/hdd1"),
#     "hdd2": get_disk_info("/mnt/old_hdd/hdd2"),
#     "hdd3": get_disk_info("/mnt/old_hdd/hdd3"),
# }

disks = dict()

for name, path in mystorageroots.ALLOWED_STORAGE_ROOTS.items():
    if name == "server":
        continue  # Skip the server entry, as it's handled separately
    disk_info = get_disk_info(path)
    if disk_info is not None:
        disks[name] = disk_info

disks["server"] = get_disk_info("/")





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



import subprocess
import platform

SERVICES = {
    "SSH": "sshd",
    "Docker": "docker",
    "Jellyfin": "jellyfin",
    "Tailscale": "tailscaled",
}

def get_services_status():
    services = []

    for display_name, service in SERVICES.items():
        try:
            result = subprocess.run(
                ["systemctl", "is-active", service],
                capture_output=True,
                text=True,
                timeout=2
            )

            status = result.stdout.strip()

        except Exception:
            status = "unknown"

        services.append({
            "name": display_name,
            "status": status
        })

    return services




def get_docker_containers():

    containers = []

    try:

        result = subprocess.run(

            [
                "docker",
                "ps",
                "-a",
                "--format",
                "{{.Names}}|{{.Status}}"
            ],

            capture_output=True,
            text=True,
            timeout=3

        )

        for line in result.stdout.splitlines():

            name, status = line.split("|",1)

            containers.append({

                "name":name,
                "status":status

            })

    except Exception:

        pass

    return containers




def get_network_info():

    local_ip = socket.gethostbyname(socket.gethostname())

    tailscale_ip = "Not Connected"

    try:

        result = subprocess.run(

            ["tailscale","ip","-4"],

            capture_output=True,

            text=True,

            timeout=2

        )

        if result.stdout.strip():

            tailscale_ip = result.stdout.strip()

    except:

        pass

    return {

        "local_ip":local_ip,
        "tailscale_ip":tailscale_ip,

    }



def get_network_info():

    local_ip = socket.gethostbyname(socket.gethostname())

    tailscale_ip = "Not Connected"

    try:

        result = subprocess.run(

            ["tailscale","ip","-4"],

            capture_output=True,

            text=True,

            timeout=2

        )

        if result.stdout.strip():

            tailscale_ip = result.stdout.strip()

    except:

        pass

    return {

        "local_ip":local_ip,
        "tailscale_ip":tailscale_ip,

    }





def get_server_information():

    return {

        "os":platform.system(),

        "kernel":platform.release(),

        "hostname":platform.node(),

        "python":platform.python_version(),

        "cpu":platform.processor(),

        "cores":psutil.cpu_count(),

        "ram":round(psutil.virtual_memory().total/(1024**3),1)

    }





def get_dashboard_data():
    print(disks)

    return {

        "system_status":get_system_status(),

        "services":get_services_status(),

        "containers":get_docker_containers(),

        "network":get_network_info(),

        "server":get_server_information(),

    }