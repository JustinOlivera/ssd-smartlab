import os, random, time

def random_read_test(file_path, ops=5000, block_size=4096):
    latencies = []

    with open(file_path, "rb") as f:
        file_size = os.path.getsize(file_path)

        for _ in range(ops):
            pos = random.randint(0, file_size - block_size)
            f.seek(pos)

            start = time.time()
            f.read(block_size)
            latencies.append((time.time() - start) * 1000)

    return latencies
