import platform
import socket
import psutil


# =========================
# GET SYSTEM INFO (RETURN DATA)
# =========================
def get_system_info():
    try:
        info = {
            "os": f"{platform.system()} {platform.release()}",
            "hostname": socket.gethostname(),
            "processor": platform.processor(),
            "cpu_usage": psutil.cpu_percent(),
            "ram_usage": psutil.virtual_memory().percent,
            "total_ram": round(psutil.virtual_memory().total / (1024**3), 2),
            "available_ram": round(psutil.virtual_memory().available / (1024**3), 2),
            "disk_usage": psutil.disk_usage('/').percent
        }
        return info

    except Exception as e:
        return {"error": str(e)}


# =========================
# DISPLAY SYSTEM INFO
# =========================
def display_system_info(write_log=None, header=None, success=None, error=None):
    if header:
        header("SYSTEM INFORMATION")

    data = get_system_info()

    if "error" in data:
        if error:
            error(data["error"])
        else:
            print("Error:", data["error"])
        return

    print(f"OS            : {data['os']}")
    print(f"Hostname      : {data['hostname']}")
    print(f"Processor     : {data['processor']}")
    print(f"CPU Usage     : {data['cpu_usage']}%")
    print(f"RAM Usage     : {data['ram_usage']}%")
    print(f"Total RAM     : {data['total_ram']} GB")
    print(f"Available RAM : {data['available_ram']} GB")
    print(f"Disk Usage    : {data['disk_usage']}%")

    if success:
        success("System info retrieved")

    if write_log:
        write_log("System info checked")