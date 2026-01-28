import sys
import os

# ---------------------------
# Making Python see project root
# ---------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from benchmarks.sequential_test import sequential_write_test, sequential_read_test
from benchmarks.random_test import random_read_test
from monitoring.smart_reader import read_smart_data

# ---------------------------
# Page configuration
# ---------------------------
st.set_page_config(
    page_title="SSD SmartLab",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Styling
# ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600&display=swap');

* {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Background & text */
body {
    background-color: #020617 !important;
    color: #00ff9c !important;
}

/* Main area */
.block-container {
    max-width: 1400px;
    padding-top: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617 !important;
    border-right: 1px solid #00ff9c55 !important;
}
section[data-testid="stSidebar"] * {
    color: #00ff9c !important;
}

/* Headers */
h1, h2, h3 {
    color: #00ff9c !important;
    letter-spacing: 1px;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background-color: #020617 !important;
    border: 1px solid #00ff9c88 !important;
    border-radius: 6px !important;
    padding: 14px;
    box-shadow: 0 0 8px #00ff9c33 !important;
}

/* Alerts / info boxes */
div[data-testid="stAlert"] {
    background-color: #020617 !important;
    border: 1px solid #00ff9c88 !important;
}

/* Inputs */
input, textarea, .stTextInput input, .stNumberInput input, .stSlider > div > div {
    background-color: #020617 !important;
    border: 1px solid #00ff9c88 !important;
    color: #00ff9c !important;
}

/* Buttons */
button {
    background-color: #020617 !important;
    border: 1px solid #00ff9c !important;
    color: #00ff9c !important;
    font-weight: 600;
    padding: 6px 12px;
    border-radius: 4px;
    box-shadow: 0 0 6px #00ff9c33 !important;
}
button:hover {
    background-color: #00ff9c !important;
    color: #020617 !important;
}

/* Tables */
thead tr th {
    background-color: #020617 !important;
    color: #00ff9c !important;
}
tbody tr td {
    background-color: #020617 !important;
    color: #9fffe0 !important;
}

/* Plots */
canvas, svg {
    background-color: #020617 !important;
}

/* Code blocks */
code, pre {
    background-color: #020617 !important;
    border: 1px solid #00ff9c88 !important;
    color: #00ff9c !important;
}

/* Hide default top-left sidebar toggle */
button[title="Toggle sidebar"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Header
# ---------------------------
st.title("SSD SmartLab")
st.subheader("Enterprise-Style SSD Testing & Health Analytics Platform")

st.markdown("""
SSD SmartLab is a modular validation platform designed to benchmark solid-state drives, 
analyze I/O latency behavior, and integrate firmware-level health telemetry. 
The architecture mirrors professional lab SSD validation tools.
""")

st.markdown("---")

# ---------------------------
# Sidebar controls
# ---------------------------
st.sidebar.header("SSD Test Configuration Panel")
st.sidebar.markdown("Configure your test workload parameters before execution.")

test_file = st.sidebar.text_input("Test file name", "ssd_test.bin")
file_size = st.sidebar.slider("Sequential Workload Size (MB)", 64, 1024, 256)
random_ops = st.sidebar.slider("Random Read Operations", 1000, 20000, 5000)

st.sidebar.markdown("---")

run_bench = st.sidebar.button("▶ Run Performance Benchmarks")
load_smart = st.sidebar.button("⚡ Read SMART Health Data")

# ---------------------------
# Performance Benchmarks
# ---------------------------
st.header("Performance Benchmarking")
st.markdown("""
This module generates real I/O workloads to evaluate SSD throughput and latency behavior.
Sequential workloads measure sustained bandwidth. Random workloads measure access latency distribution.
""")

if run_bench:
    st.info("Executing SSD performance benchmarks. Disk activity is in progress...")

    write_speed = sequential_write_test(test_file, file_size)
    read_speed = sequential_read_test(test_file)
    latencies = random_read_test(test_file, random_ops)

    df_lat = pd.DataFrame({"Latency (ms)": latencies})

    st.subheader("Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Sequential Write Throughput", f"{write_speed:.2f} MB/s")
    col2.metric("Sequential Read Throughput", f"{read_speed:.2f} MB/s")
    col3.metric("Average Random Read Latency", f"{df_lat['Latency (ms)'].mean():.3f} ms")

    st.markdown("---")
    st.subheader("Random Read Latency Distribution")
    fig, ax = plt.subplots()
    ax.hist(latencies, bins=60)
    ax.set_xlabel("Latency (ms)")
    ax.set_ylabel("Operations")
    ax.set_title("Random Read Latency Histogram")
    st.pyplot(fig)

    os.makedirs("data/results", exist_ok=True)
    df_lat.to_csv("data/results/latency_results.csv", index=False)

    st.success("Benchmark complete. Results archived.")

# ---------------------------
# SMART Health Monitoring
# ---------------------------
st.header("SSD SMART Health Monitoring")
st.markdown("""
Retrieve firmware-level health and reliability attributes using smartmontools.
The system automatically detects compatible devices and interfaces.
""")

if load_smart:
    st.info("Acquiring SMART telemetry...")

    smart, err = read_smart_data()

    if err:
        st.warning("SMART telemetry could not be accessed.")
        st.caption("System response:")
        st.code(err)
        st.info("On many Windows systems, NVMe SMART access is restricted. SATA devices and Linux typically provide full telemetry.")
    elif smart is None or smart.empty:
        st.warning("SMART-compatible device detected but no attributes returned.")
    else:
        df_smart = smart.reset_index()
        df_smart.columns = ["Attribute", "Reported Value"]

        st.subheader("Detected SMART Attributes")
        st.dataframe(df_smart, use_container_width=True)

        os.makedirs("data/results", exist_ok=True)
        df_smart.to_csv("data/results/smart_snapshot.csv", index=False)
        st.success("SMART snapshot captured and archived.")

# ---------------------------
# Historical Analytics
# ---------------------------
st.header("Historical Performance Analytics")
st.markdown("View previously recorded benchmarks for trend analysis and regression studies.")

if os.path.exists("data/results/latency_results.csv"):
    hist = pd.read_csv("data/results/latency_results.csv")
    st.subheader("Latency Behavior Across Samples")
    fig2, ax2 = plt.subplots()
    ax2.plot(hist.index, hist["Latency (ms)"])
    ax2.set_title("Latency Over Time")
    ax2.set_ylabel("Latency (ms)")
    ax2.set_xlabel("Operation Index")
    st.pyplot(fig2)
else:
    st.info("No historical data available. Run benchmarks to generate analytics.")

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.caption("SSD SmartLab — Modular SSD benchmarking, validation, and health analytics platform for professional lab environments.")
