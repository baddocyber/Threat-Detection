import joblib
import numpy as np
import pandas as pd
import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf
from pyspark.sql.types import *
from sent_to_django import send_to_django

spark = SparkSession.builder \
    .appName("TelecomThreatDetector") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0-preview3") \
    .getOrCreate()

print("Spark Session Created Successfully")

# Load your trained model once, outside the per-row logic
model = joblib.load("model.pkl")  # adjust path/name to match your actual file

# Define predict_udf — wraps your model for use inside Spark
def predict(dur, proto, service, state, spkts, dpkts):
    # build a feature row matching what your model expects, then predict
    features = np.array([[dur, spkts, dpkts]])  # adjust to your real feature set
    pred = model.predict(features)[0]
    return int(pred)

predict_udf = udf(predict, IntegerType())

# Read from Kafka
df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "telecom-threat")
    .load()
)

df = df.selectExpr("CAST(value AS STRING)")

schema = StructType([
    StructField("dur", DoubleType()),
    StructField("proto", StringType()),
    StructField("service", StringType()),
    StructField("state", StringType()),
    StructField("Spkts", IntegerType()),
    StructField("Dpkts", IntegerType())
])

df2 = df.select(from_json(col("value"), schema).alias("data")).select("data.*")

df2 = df2.withColumn(
    "prediction",
    predict_udf(col("dur"), col("proto"), col("service"), col("state"), col("Spkts"), col("Dpkts"))
)

# This is where row-by-row sending to Django happens
def process_batch(batch_df, batch_id):
    for row in batch_df.collect():
        send_to_django({
            "dur": float(row["dur"]),
            "proto": row["proto"],
            "service": row["service"],
            "state": row["state"],
            "spkts": float(row["Spkts"]),
            "dpkts": float(row["Dpkts"]),
            "prediction": int(row["prediction"]),
            "threat_level": "high" if row["prediction"] == 1 else "normal"  # adjust to your logic
        })

query = df2.writeStream \
       .foreachBatch(process_batch) \
       .option("checkpointLocation", "C:/spark_checkpoints/telecom_threat") \
       .start()

query.awaitTermination()