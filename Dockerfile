FROM python:3.11-slim

WORKDIR /app/src
COPY locustfiles/ /mnt/locust/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "store_manager.py"]