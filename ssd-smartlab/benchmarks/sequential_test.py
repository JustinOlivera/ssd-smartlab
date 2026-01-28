import os, time

def sequential_write_test(file_path, size_mb=512):
    data = os.urandom(1024 * 1024)
    start = time.time()

    with open(file_path, "wb") as f:
        for _ in range(size_mb):
            f.write(data)

    elapsed = time.time() - start
    speed = size_mb / elapsed
    return speed


def sequential_read_test(file_path):
    start = time.time()
    with open(file_path, "rb") as f:
        while f.read(1024 * 1024):
            pass

    elapsed = time.time() - start
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    speed = size_mb / elapsed
    return speed
