# Telecom Network Anomaly & Cyber-Threat Detection

A real-time network threat detection pipeline built on a Lambda-style architecture: network flow records are streamed through **Kafka**, classified by an ML model in **Spark Structured Streaming**, and surfaced in a **Django** dashboard with email alerting.

## Architecture

```
UNSW-NB15 flows → Kafka producer → Spark consumer (ML model) → Django API → Dashboard + email alerts
```

## Structure

| Path | Purpose |
|---|---|
| `telecom_threat/kafka/producer.py` | Streams flow records into Kafka |
| `telecom_threat/sparkstreaming/Train_Model.py` | Trains the Decision Tree classifier on UNSW-NB15 and saves the model and encoders |
| `telecom_threat/sparkstreaming/spark_consumer.py` | Consumes the Kafka stream, applies the model, flags threats |
| `telecom_threat/sparkstreaming/sent_to_django.py` | Pushes detections to the Django dashboard |
| `telecom_threat/sparkstreaming/*.pkl` | Trained model, scaler, and label encoders |
| `threat_detection_dashboard/` | Django dashboard (views, models, templates, email alerts) |

## Dataset

Uses the **UNSW-NB15** dataset. The CSV is ~160 MB, which exceeds GitHub's file limit, so it is not included. Download it from the official UNSW source and place `UNSW-NB15.csv` in `telecom_threat/kafka/` and `telecom_threat/sparkstreaming/`.

## Setup

```bash
cd threat_detection_dashboard
pip install django pandas scikit-learn joblib pyspark kafka-python findspark
export DJANGO_SECRET_KEY=... EMAIL_HOST_USER=... EMAIL_HOST_PASSWORD=...   # see .env.example
python manage.py migrate
python manage.py runserver
```

Then start Kafka, run `producer.py`, and run `spark_consumer.py`.

## Notes
- Secrets (Django secret key, email credentials) are read from environment variables — never commit them.
- `Train_Model.py` contains a local Windows path to the dataset; update it for your machine.

**Author:** Adam Armiya'u — Department of Cybersecurity, Nigerian Army University Biu
