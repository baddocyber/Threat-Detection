import findspark
findspark.init()

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TestSpark") \
    .getOrCreate()

print("Spark Version:", spark.version)


import joblib
import numpy as np
import pandas as pd
import findspark
findspark.init()

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TelecomThreatDetection") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("Spark Session Created Successfully")

model = joblib.load(r"C:\Users\ADMIN\Desktop\NETWORK_ANORMALY_DETECTOR\telecom_threat\sparkstreaming\model.pkl")
scaler = joblib.load(r"C:\Users\ADMIN\Desktop\NETWORK_ANORMALY_DETECTOR\telecom_threat\sparkstreaming\scaler.pkl")

from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType

def predict_attack(dur, proto, service, state, Spkts, Dpkts):

    try:
        features = np.array([[dur, proto, service, state, Spkts, Dpkts]])
        features = scaler.transform(features)

        prediction = model.predict(features)[0]

        return int(prediction)

    except:
        return 0
    
predict_udf = udf(predict_attack, IntegerType())

df2 = df2.select("data.*")

df2 = df2.withColumn(
    "prediction",
    predict_udf(
        col("dur"),
        col("proto"),
        col("service"),
        col("state"),
        col("Spkts"),
        col("Dpkts")
    )
)

from pyspark.sql.functions import when

df2 = df2.withColumn(
    "threat_level",
    when(col("prediction") == 1, "ATTACK").otherwise("NORMAL")
)