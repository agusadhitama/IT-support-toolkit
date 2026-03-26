import os
import platform
import socket
import subprocess
from datetime import datetime


LOG_FILE = "logs/toolkit.log"


def write_log(message):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")


# =========================
# SYSTEM INFO
# =========================
def system_info():
    print("\n=== SYSTEM INFORMATION ===")
    info = {
        "OS": platform.system() + " " + platform.release(),
        "Hostname": socket.gethostname(),
        "Processor": platform.processor()
    }

    for key, value in info.items():
        print(f"{key}: {value}")
        write_log(f"{key}: {value}")


# =========================
# NETWORK CHECK
# =========================
def network_check():
    print("\n=== NETWORK CHECK ===")
    try:
        subprocess.check_output(["ping", "8.8.8.8", "-n", "2"], stderr=subprocess.STDOUT)
        print("Internet Status: CONNECTED")
        write_log("Internet CONNECTED")
    except subprocess.CalledProcessError:
        print("Internet Status: DISCONNECTED")
        write_log("Internet DISCONNECTED")


# =========================
# DISK CLEANUP
# =========================
def disk_cleanup():
    print("\n=== DISK CLEANUP ===")
    temp = os.getenv('TEMP')

    if temp and os.path.exists(temp):
        try:
            for file in os.listdir(temp):
                file_path = os.path.join(temp, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except:
                    pass
            print("Temp files cleaned.")
            write_log("Temp files cleaned")
        except Exception as e:
            print("Error cleaning temp:", e)
            write_log(f"Cleanup error: {e}")
    else:
        print("Temp folder not found.")


# =========================
# SERVICE CHECK (WINDOWS)
# =========================
def check_service():
    print("\n=== SERVICE CHECK ===")
    service_name = "Spooler"

    try:
        output = subprocess.check_output(
            ["sc", "query", service_name], stderr=subprocess.STDOUT, text=True
        )

        if "RUNNING" in output:
            print(f"{service_name} is RUNNING")
            write_log(f"{service_name} RUNNING")
        else:
            print(f"{service_name} is NOT running")
            write_log(f"{service_name} NOT running")

    except Exception as e:
        print("Error checking service:", e)
        write_log(f"Service check error: {e}")


# =========================
# MENU
# =========================
def main():
    while True:
        print("\n=== IT SUPPORT TOOLKIT ===")
        print("1. System Information")
        print("2. Network Check")
        print("3. Disk Cleanup")
        print("4. Service Check (Print Spooler)")
        print("5. Exit")

        choice = input("Select option: ")

        if choice == "1":
            system_info()
        elif choice == "2":
            network_check()
        elif choice == "3":
            disk_cleanup()
        elif choice == "4":
            check_service()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
