from benchmarks.sequential_test import sequential_write_test, sequential_read_test
from monitoring.smart_reader import read_smart_data

file = "test.bin"

w = sequential_write_test(file, 256)
r = sequential_read_test(file)
smart = read_smart_data()

print("Write MB/s:", w)
print("Read MB/s:", r)
print("SMART snapshot:\n", smart.head())
