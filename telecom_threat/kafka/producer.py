import pandas as pd
import json
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

csv_file = r"C:\Users\ADMIN\Desktop\NETWORK_ANORMALY_DETECTOR\telecom_threat\kafka\UNSW-NB15.csv" 

chunksize = 100

for chunk in pd.read_csv(csv_file, chunksize=chunksize):

    for column in chunk.columns:
       if chunk[column].dtype == "object" or str(chunk[column].dtype) == "string":
        chunk[column] = chunk[column].fillna("unknown")
       else:
        chunk[column] = chunk[column].fillna(0)

    for _, row in chunk.iterrows():

        producer.send(
            "telecom-threat",
            row.to_dict()
        )

        print("Sent:", row.name)

        time.sleep(0.05)

producer.flush()
producer.close()

print("Dataset transmission completed.")