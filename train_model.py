
import pandas as pd
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# STEP 1: Read the new CSV dataset
df = pd.read_csv("dataset.csv")

# STEP 2: Clean and validate the data
df["SystemCodeNumber"] = df["SystemCodeNumber"].astype(str)
df["LastUpdated"] = pd.to_datetime(
    df["LastUpdated"], errors="coerce"
)
df["Capacity"] = pd.to_numeric(
    df["Capacity"], errors="coerce"
)
df["Occupancy"] = pd.to_numeric(
    df["Occupancy"], errors="coerce"
)

df = df.dropna(
    subset=[
        "SystemCodeNumber",
        "ParkingName",
        "Capacity",
        "Occupancy",
        "LastUpdated"
    ]
)

df = df[
    (df["Capacity"] > 0)
    & (df["Occupancy"] >= 0)
    & (df["Occupancy"] <= df["Capacity"])
].copy()

if len(df) < 20:
    raise ValueError("Not enough valid records in dataset.csv")

# STEP 3: Create numerical codes for parking locations
parking_ids = sorted(df["SystemCodeNumber"].unique())

parking_mapping = {
    parking_id: index
    for index, parking_id in enumerate(parking_ids)
}

df["ParkingCode"] = df["SystemCodeNumber"].map(
    parking_mapping
)

# STEP 4: Extract date and time features
df["Hour"] = df["LastUpdated"].dt.hour
df["DayOfWeek"] = df["LastUpdated"].dt.dayofweek
df["Month"] = df["LastUpdated"].dt.month

feature_columns = [
    "ParkingCode",
    "Capacity",
    "Hour",
    "DayOfWeek",
    "Month"
]

# STEP 5: Sort by time before splitting the data
df = df.sort_values("LastUpdated").reset_index(drop=True)

X = df[feature_columns]
y = df["Occupancy"]

split_index = int(len(df) * 0.80)

if split_index == 0 or split_index >= len(df):
    raise ValueError("Not enough data for training and testing")

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]
y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

# STEP 6: Create and train the model
model = RandomForestRegressor(
    n_estimators=60,
    max_depth=18,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# STEP 7: Evaluate the model on the later records
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)

print("Model training completed!")
print("Valid dataset records:", len(df))
print("Parking locations:", len(parking_mapping))
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Mean Absolute Error:", round(mae, 2), "spaces")

# STEP 8: Train the final model using all available records
model.fit(X, y)

# STEP 9: Save the model and parking location mapping
with open("occupancy_model.pkl", "wb") as file:
    pickle.dump(model, file)

with open("parking_mapping.pkl", "wb") as file:
    pickle.dump(parking_mapping, file)

print("occupancy_model.pkl created successfully!")
print("parking_mapping.pkl created successfully!")
