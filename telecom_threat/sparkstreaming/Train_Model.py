import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib


# Load Dataset
columns = [
    "srcip","sport","dstip","dsport","proto","state","dur",
    "sbytes","dbytes","sttl","dttl","sloss","dloss",
    "service","Sload","Dload","Spkts","Dpkts",
    "swin","dwin","stcpb","dtcpb","smeansz","dmeansz",
    "trans_depth","res_bdy_len","Sjit","Djit","Stime",
    "Ltime","Sintpkt","Dintpkt","tcprtt","synack",
    "ackdat","is_sm_ips_ports","ct_state_ttl",
    "ct_flw_http_mthd","is_ftp_login","ct_ftp_cmd",
    "ct_srv_src","ct_srv_dst","ct_dst_ltm","ct_src_ltm",
    "ct_src_dport_ltm","ct_dst_sport_ltm",
    "ct_dst_src_ltm","attack_cat","label"
]

df = pd.read_csv(
    r"C:\Users\ADMIN\Desktop\NETWORK_ANORMALY_DETECTOR\telecom_threat\sparkstreaming\UNSW-NB15.csv",
    header=None,
    names=columns
)

print(df.columns.tolist())


# Select Features

features = ["dur", "proto", "service", "state", "Spkts", "Dpkts"]

df = df[features + ["label"]]


# Encode categorical data

le_proto = LabelEncoder()
le_service = LabelEncoder()
le_state = LabelEncoder()

df["proto"] = le_proto.fit_transform(df["proto"])
df["service"] = le_service.fit_transform(df["service"])
df["state"] = le_state.fit_transform(df["state"])

# Remove rows with missing labels
df = df.dropna(subset=["label"])

# Convert label to integer
df["label"] = df["label"].astype(int)


# Split data

X = df[features]
y = df["label"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# Scale features

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# Train Decision Tree

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# 4. Evaluate model
y_pred = model.predict(X_test)
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)


accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    pos_label=1,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    pos_label=1,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    pos_label=1,
    zero_division=0
)


print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)


print("\nClassification Report")
print(classification_report(y_test, y_pred))


# Save model and scaler

joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

joblib.dump(le_proto, "proto_encoder.pkl")
joblib.dump(le_service, "service_encoder.pkl")
joblib.dump(le_state, "state_encoder.pkl")

print("Model Training Completed")


print(df["label"].isnull().sum())
print(df["label"].value_counts(dropna=False))