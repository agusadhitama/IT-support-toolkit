import platform
import socket
import subprocess


# =========================
# BASIC UTIL
# =========================
def is_windows():
    return platform.system().lower() == "windows"


# =========================
# PING TEST (RETURN BOOL)
# =========================
def ping_test():
    try:
        command = "ping 8.8.8.8 -n 2" if is_windows() else "ping -c 2 8.8.8.8"
        subprocess.check_output(command, shell=True)
        return True
    except:
        return False


# =========================
# GET IP INFO (RETURN DATA)
# =========================
def get_ip_info():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        return {
            "hostname": hostname,
            "ip": ip
        }

    except Exception as e:
        return {"error": str(e)}


# =========================
# FLUSH DNS
# =========================
def flush_dns():
    try:
        if is_windows():
            subprocess.call("ipconfig /flushdns", shell=True)
        else:
            subprocess.call("systemd-resolve --flush-caches", shell=True)

        return True
    except:
        return False


# =========================
# RESET NETWORK
# =========================
def reset_network():
    try:
        if is_windows():
            subprocess.call("netsh winsock reset", shell=True)
            subprocess.call("netsh int ip reset", shell=True)
        else:
            subprocess.call("sudo systemctl restart NetworkManager", shell=True)

        return True
    except:
        return False


# =========================
# DISPLAY FUNCTIONS (FOR CLI)
# =========================
def display_ping(write_log=None, header=None, success=None, error=None):
    if header:
        header("PING TEST")

    result = ping_test()

    if result:
        if success:
            success("Internet CONNECTED")
        else:
            print("Internet CONNECTED")
    else:
        if error:
            error("Internet DISCONNECTED")
        else:
            print("Internet DISCONNECTED")

    if write_log:
        write_log(f"Ping result: {'CONNECTED' if result else 'DISCONNECTED'}")


def display_ip(write_log=None, header=None, success=None, error=None):
    if header:
        header("IP INFORMATION")

    data = get_ip_info()

    if "error" in data:
        if error:
            error(data["error"])
        else:
            print("Error:", data["error"])
        return

    print(f"Hostname : {data['hostname']}")
    print(f"IP Addr  : {data['ip']}")

    if success:
        success("IP retrieved")

    if write_log:
        write_log("IP info checked")


def display_flush_dns(write_log=None, header=None, success=None, error=None):
    if header:
        header("FLUSH DNS")

    result = flush_dns()

    if result:
        if success:
            success("DNS flushed")
        else:
            print("DNS flushed")
    else:
        if error:
            error("Failed to flush DNS")
        else:
            print("Failed to flush DNS")

    if write_log:
        write_log("Flush DNS executed")


def display_reset_network(write_log=None, header=None, success=None, error=None):
    if header:
        header("RESET NETWORK")

    result = reset_network()

    if result:
        if success:
            success("Network reset done")
        else:
            print("Network reset done")
    else:
        if error:
            error("Failed to reset network")
        else:
            print("Failed to reset network")

    if write_log:
        write_log("Network reset executed")


# =========================
# AUTO FIX (SMART FEATURE)
# =========================
def auto_fix(write_log=None, header=None, success=None, error=None, info=None):
    if header:
        header("AUTO FIX NETWORK")

    if not ping_test():
        if info:
            info("Attempting auto fix...")

        flush_dns()
        reset_network()

        if ping_test():
            if success:
                success("Connection restored!")
            else:
                print("Connection restored!")
        else:
            if error:
                error("Still no connection")
            else:
                print("Still no connection")
    else:
        if success:
            success("No issues detected")
        else:
            print("No issues detected")

    if write_log:
        write_log("Auto fix executed")