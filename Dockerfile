FROM python:3.9-slim

WORKDIR /app

# Install MySQL development files and client
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential pkg-config default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Make wait-for-it.sh executable
RUN chmod +x wait-for-it.sh

CMD ["./wait-for-it.sh", "db", "python", "app.py"]
