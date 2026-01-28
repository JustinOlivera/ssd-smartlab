import os, time, random

def endurance_test(file_path, cycles=1000):
    for i in range(cycles):
        with open(file_path, "wb") as f:
            f.write(os.urandom(10 * 1024 * 1024))

        with open(file_path, "rb") as f:
            f.read()

        if i % 50 == 0:
            print(f"Cycle {i} complete")
