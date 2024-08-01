import os
import time
import requests
import psutil

MONITORING_INTERVAL = 60  # in seconds
API_ENDPOINT = "https://your-api-endpoint.com/memory-usage"

def get_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss

def send_memory_usage():
    print("Starting...")
    memory_usage = get_memory_usage()
    payload = {
        "memory_usage": memory_usage
    }
    try:
        print("Starting.1111..")
        response = requests.post(API_ENDPOINT, json=payload, timeout=5)
        print("Starting..22222.")
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to send memory usage data: {e}")

# if __name__ == "__main__":
while True:
    send_memory_usage()
    time.sleep(MONITORING_INTERVAL)
