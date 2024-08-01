from flask import Flask, request
from prometheus_client import Counter, generate_latest, CollectorRegistry, multiprocess
import logging
import time
import os

app = Flask(__name__)

# Create a counter for the number of requests
REQUEST_COUNT = Counter('flask_requests_total', 'Total Request Count', ['method', 'endpoint', 'http_status'])

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

@app.route('/')
def hello_world():
    print("hello_world")
    logging.info("sample log")
    return 'Hello, World!'

# Endpoint to expose metrics
@app.route('/metrics')
def metrics():
    registry = CollectorRegistry()
    if 'PROMETHEUS_MULTIPROC_DIR' in os.environ:
        multiprocess.MultiProcessCollector(registry)
    return generate_latest(registry)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
