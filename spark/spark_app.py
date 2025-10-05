from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, count
import os

# Read broker address from environment variables set in docker-compose.yml
KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "kafka:29092")
INPUT_TOPIC = "processed-data-topic" # Hypothetical topic for this example

spark = SparkSession.builder \
    .appName("PySparkKafkaStreamProcessor") \
    .master("local[*]") \
    .getOrCreate()
    
spark.sparkContext.setLogLevel("WARN")

kafka_df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", KAFKA_BROKERS) \
  .option("subscribe", INPUT_TOPIC) \
  .load()

# This is where your custom PySpark analytics/ML logic would go
value_df = kafka_df.selectExpr("CAST(value AS STRING) as text_data")

# Print results to the console for verification
query = value_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

# query.awaitTermination() # Keep commented out to allow the service to run in the background