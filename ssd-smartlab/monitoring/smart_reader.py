import subprocess
import pandas as pd


def detect_smart_device():
    """
    Uses smartctl --scan to detect available devices.
    Returns (device_string, device_type) or (None, None)
    """
    try:
        result = subprocess.run(
            ["smartctl", "--scan"],
            capture_output=True,
            text=True
        )

        lines = result.stdout.strip().split("\n")
        if not lines or lines == [""]:
            return None, None

        first = lines[0]
        parts = first.split()

        device = parts[0]          # example: /dev/sda or \\.\PhysicalDrive0
        dtype = None

        if "-d" in parts:
            dtype = parts[parts.index("-d") + 1]

        return device, dtype

    except Exception:
        return None, None


def read_smart_data():
    """
    Attempts to read SMART data.
    Returns (DataFrame, error_message)
    """
    device, dtype = detect_smart_device()

    if device is None:
        return None, "No SMART devices detected."

    cmd = ["smartctl", "-a"]

    if dtype:
        cmd.extend(["-d", dtype])

    cmd.append(device)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return None, result.stderr.strip()

        data = {}
        for line in result.stdout.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip()

        df = pd.DataFrame.from_dict(data, orient="index", columns=["Value"])
        return df, None

    except FileNotFoundError:
        return None, "smartctl.exe not found."
    except Exception as e:
        return None, str(e)
