import os
import time
from datetime import datetime
from colorama import Fore, Style, init

# Init colorama
init(autoreset=True)

# Import modules
from tools.system_info import display_system_info
from tools.network import (
    display_ping,
    display_ip,
    display_flush_dns,
    auto_fix
)
from tools.cleanup import (
    display_clean_temp,
    display_clean_recycle_bin
)

# =========================
# LOG SYSTEM
# =========================
LOG_FILE = "logs/activity.log"

def write_log(message):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")

# =========================
# UI FUNCTIONS
# =========================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header(title):
    clear()
    print(Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + f"{title.center(50)}")
    print(Fore.CYAN + "=" * 50)

def success(msg):
    print(Fore.GREEN + f"[✓] {msg}")

def error(msg):
    print(Fore.RED + f"[✗] {msg}")

def info(msg):
    print(Fore.BLUE + f"[i] {msg}")

def pause():
    input(Fore.MAGENTA + "\nPress Enter to continue...")

# =========================
# EXTRA FEATURES
# =========================
def check_service():
    header("SERVICE CHECK")
    service = input("Enter service name (e.g. spooler): ")

    try:
        result = os.popen(f"sc query {service}").read()
        print(result)
        write_log(f"Checked service: {service}")
    except Exception as e:
        error(f"Failed: {e}")

    pause()

def health_check():
    header("SYSTEM HEALTH CHECK")

    try:
        print("Running system file checker...\n")
        os.system("sfc /scannow")
        write_log("Ran system health check")
    except Exception as e:
        error(f"Failed: {e}")

    pause()

def export_report():
    header("EXPORT REPORT")

    try:
        filename = f"report_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write("IT SUPPORT TOOLKIT REPORT\n")
            f.write("=" * 40 + "\n\n")
            f.write("Generated at: " + str(datetime.now()) + "\n")

        success(f"Report saved as {filename}")
        write_log(f"Exported report: {filename}")
    except Exception as e:
        error(f"Failed: {e}")

    pause()

# =========================
# MAIN MENU
# =========================
def main():
    while True:
        header("IT SUPPORT TOOLKIT PRO")

        print("1. System Information")
        print("2. Ping Test")
        print("3. IP Information")
        print("4. Flush DNS")
        print("5. Disk Cleanup (Temp)")
        print("6. Service Check")
        print("7. Auto Fix Network")
        print("8. Health Check")
        print("9. Export Report")
        print("10. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            display_system_info(write_log, header, success, error)

        elif choice == "2":
            display_ping(write_log, header, success, error)

        elif choice == "3":
            display_ip(write_log, header, success, error)

        elif choice == "4":
            display_flush_dns(write_log, header, success, error)

        elif choice == "5":
            display_clean_temp(write_log, header, success, error)

        elif choice == "6":
            check_service()

        elif choice == "7":
            auto_fix(write_log, header, success, error, info)

        elif choice == "8":
            health_check()

        elif choice == "9":
            export_report()

        elif choice == "10":
            print(Fore.YELLOW + "Goodbye 👋")
            break

        else:
            error("Invalid choice")
            pause()

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()