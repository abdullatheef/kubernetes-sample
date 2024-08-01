FROM python:3.9-slim

WORKDIR /app

COPY memory_monitor.py .

RUN pip install psutil requests

CMD ["python", "memory_monitor.py"]
