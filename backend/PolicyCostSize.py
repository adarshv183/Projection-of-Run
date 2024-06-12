import pickle
from datetime import datetime, timedelta
import pandas as pd
import json


# Function to create a feature set for a given future datetime
def create_feature_set(future_datetime):
    features = {}
    features["minutes"] = future_datetime.minute
    features["hour"] = future_datetime.hour
    features["day_of_week"] = future_datetime.dayofweek
    features["day_of_month"] = future_datetime.day
    features["month"] = future_datetime.month
    features["year"] = future_datetime.year

    return pd.DataFrame(features, index=[0])


filename = "D:/Adhi/BMS/HPE-CTY/Projection-of-Run/models/xgb_model_delta.sav"
loaded_model = pickle.load(open(filename, "rb"))

req = [
    {
        "name": "Array_Snapshot_1",
        "type": "SNAPSHOT",
        "timestamp": "2024-06-25 20:00:00",
        "interval": 240,
        "timestamps": [
            "2024-06-25 20:00:00",
            "2024-06-25 16:00:00",
            "2024-06-25 12:00:00",
        ],
    },
    {
        "name": "Array_Snapshot_2",
        "type": "SNAPSHOT",
        "timestamp": "2024-06-25 00:00:00",
        "interval": 1440,
        "timestamps": [
            "2024-06-25 00:00:00",
            "2024-06-24 00:00:00",
            "2024-06-23 00:00:00",
        ],
    },
    {
        "name": "On-Premises_Protection_Store_4",
        "type": "BACKUP",
        "timestamp": "2024-06-25 00:00:00",
        "interval": 1440,
        "timestamps": [
            "2024-06-25 00:00:00",
            "2024-06-24 00:00:00",
            "2024-06-23 00:00:00",
            "2024-06-22 00:00:00",
            "2024-06-21 00:00:00",
            "2024-06-20 00:00:00",
            "2024-06-19 00:00:00",
            "2024-06-18 00:00:00",
            "2024-06-17 00:00:00",
            "2024-06-16 00:00:00",
            "2024-06-15 00:00:00",
            "2024-06-14 00:00:00",
            "2024-06-13 00:00:00",
            "2024-06-12 00:00:00",
            "2024-06-11 00:00:00",
            "2024-06-10 00:00:00",
            "2024-06-09 00:00:00",
            "2024-06-08 00:00:00",
            "2024-06-07 00:00:00",
            "2024-06-06 00:00:00",
            "2024-06-05 00:00:00",
            "2024-06-04 00:00:00",
            "2024-06-03 00:00:00",
            "2024-06-02 00:00:00",
        ],
    },
    {
        "name": "On-Premises_Protection_Store_7",
        "type": "BACKUP",
        "timestamp": "2024-06-19 00:00:00",
        "interval": 10080,
        "timestamps": [
            "2024-06-19 00:00:00",
            "2024-06-12 00:00:00",
            "2024-06-05 00:00:00",
            "2024-05-29 00:00:00",
        ],
    },
    {
        "name": "HPE_Cloud_Protection_Store_5",
        "type": "CLOUD_BACKUP",
        "timestamp": "2024-06-19 00:00:00",
        "interval": 10080,
        "timestamps": [
            "2024-06-19 00:00:00",
            "2024-06-12 00:00:00",
            "2024-06-05 00:00:00",
            "2024-05-29 00:00:00",
        ],
    },
    {
        "name": "HPE_Cloud_Protection_Store_6",
        "type": "CLOUD_BACKUP",
        "timestamp": "2024-06-20 00:00:00",
        "interval": 43200,
        "timestamps": ["2024-06-20 00:00:00"],
    },
]

information = {
    "SNAPSHOT": {"full_backup": 50, "cost": 20, "c_ratio": 0.04},
    "BACKUP": {"full_backup": 55, "cost": 40, "c_ratio": 0.1},
    "CLOUD_BACKUP": {"full_backup": 80, "cost": 60, "c_ratio": 0.1},
}


def projectCost(schedules, information):
    print(schedules, information)
    res = {}
    for item in schedules:
        type = item.get("type")
        name = item.get("name")
        cumilative_delta = information[type].get("full_backup")
        for timestamp in item["timestamps"]:
            feature_set = create_feature_set(pd.Timestamp(timestamp))
            delta_prediction = loaded_model.predict(feature_set)[0]
            print(f"Prediction for {timestamp} ({name}): {delta_prediction}")
            cumilative_delta += delta_prediction

        cumilative_delta = cumilative_delta * information[type].get("c_ratio")
        res[name] = {
            "type": type,
            "size_on_disk": cumilative_delta,
            "cost_projected": cumilative_delta * information[type].get("cost"),
        }
        print(f"Result for {name}: {res[name]}")
    print(res)
    return res


if __name__ == "__main__":
    print(projectCost(req, information))
