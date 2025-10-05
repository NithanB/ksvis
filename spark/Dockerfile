FROM apache/spark:3.5.0

# Switch to root to install pandas
USER root

WORKDIR /app
COPY spark_app.py .

RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*

RUN pip3 install pandas

# Switch back to spark user
USER spark
