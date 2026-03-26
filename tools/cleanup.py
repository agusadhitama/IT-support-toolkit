import os
import platform
import shutil
import subprocess


# =========================
# BASIC UTIL
# =========================
def is_windows():
    return platform.system().lower() == "windows"


# =========================
# CLEAN TEMP FILES (RETURN DATA)
# =========================
def clean_temp():
    temp_path = os.getenv('TEMP') if is_windows() else "/tmp"

    if not os.path.exists(temp_path):
        return {"error": "Temp directory not found"}

    deleted = 0
    failed = 0

    for file in os.listdir(temp_path):
        path = os.path.join(temp_path, file)

        try:
            if os.path.isfile(path):
                os.remove(path)
                deleted += 1
            elif os.path.isdir(path):
                shutil.rmtree(path)
                deleted += 1
        except:
            failed += 1

    return {
        "deleted": deleted,
        "failed": failed,
        "path": temp_path
    }


# =========================
# CLEAN RECYCLE BIN
# =========================
def clean_recycle_bin():
    try:
        if is_windows():
            subprocess.call("rd /s /q C:\\$Recycle.Bin", shell=True)
        else:
            subprocess.call("rm -rf ~/.local/share/Trash/*", shell=True)

        return True
    except:
        return False


# =========================
# DISPLAY FUNCTIONS (CLI)
# =========================
def display_clean_temp(write_log=None, header=None, success=None, error=None):
    if header:
        header("TEMP CLEANUP")

    result = clean_temp()

    if "error" in result:
        if error:
            error(result["error"])
        else:
            print("Error:", result["error"])
        return

    msg = f"Deleted: {result['deleted']} | Failed: {result['failed']}"

    if success:
        success(msg)
    else:
        print(msg)

    if write_log:
        write_log(f"Temp cleaned ({msg})")


def display_clean_recycle_bin(write_log=None, header=None, success=None, error=None):
    if header:
        header("RECYCLE BIN CLEANUP")

    result = clean_recycle_bin()

    if result:
        if success:
            success("Recycle bin cleared")
        else:
            print("Recycle bin cleared")
    else:
        if error:
            error("Failed to clear recycle bin")
        else:
            print("Failed to clear recycle bin")

    if write_log:
        write_log("Recycle bin cleaned")