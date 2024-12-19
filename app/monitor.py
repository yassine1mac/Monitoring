import psutil
import sqlite3
import time

def get_system_metrics():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    net = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    return cpu, memory, disk, net

def log_metrics():
    conn = sqlite3.connect('app/metrics.db')
    cursor = conn.cursor()
    while True:
        cpu, memory, disk, net = get_system_metrics()
        cursor.execute('''
            INSERT INTO metrics (cpu_usage, memory_usage, disk_usage, network_usage)
            VALUES (?, ?, ?, ?)
        ''', (cpu, memory, disk, net))
        conn.commit()
        time.sleep(10)

if __name__ == "__main__":
    log_metrics()

