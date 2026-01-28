import subprocess
import pandas as pd

def read_smart_data(drive="/dev/sda"):
    result = subprocess.run(
        ["smartctl", "-A", drive],
        capture_output=True,
        text=True
    )

    metrics = {}
    for line in result.stdout.split("\n"):
        parts = line.split()
        if len(parts) > 9 and parts[0].isdigit():
            metrics[parts[1]] = int(parts[9])

    return pd.Series(metrics)
