
from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
from datetime import datetime

app = Flask(__name__)

# STEP 1: Load the trained model and location mapping
with open("occupancy_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("parking_mapping.pkl", "rb") as file:
    parking_mapping = pickle.load(file)

# STEP 2: Read the new dataset
df = pd.read_csv("dataset.csv")
df["SystemCodeNumber"] = df["SystemCodeNumber"].astype(str)

# STEP 3: Get each parking area's name and capacity
parking_info = (
    df.groupby("SystemCodeNumber")
    .agg(
        ParkingName=("ParkingName", "first"),
        Capacity=("Capacity", "first")
    )
    .to_dict("index")
)

# STEP 4: Prepare the dropdown options
parking_areas = [
    {
        "id": parking_id,
        "name": parking_info[parking_id]["ParkingName"]
    }
    for parking_id in sorted(parking_mapping.keys())
    if parking_id in parking_info
]


@app.route("/")
def home():
    return render_template(
        "index.html",
        parking_areas=parking_areas
    )


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True) or {}

        parking_id = str(data.get("parking_id", ""))
        date_time = data.get("date_time", "")
        vehicle_type = data.get("vehicle_type", "")

        valid_vehicle_types = [
            "Car", "Bike", "Bus", "Truck", "Other"
        ]

        # Validate the user's selections
        if parking_id not in parking_mapping:
            return jsonify({
                "error": "Please select a valid parking location."
            }), 400

        if parking_id not in parking_info:
            return jsonify({
                "error": "Parking location information is missing."
            }), 400

        if vehicle_type not in valid_vehicle_types:
            return jsonify({
                "error": "Please select a valid vehicle type."
            }), 400

        timestamp = datetime.strptime(
            date_time, "%Y-%m-%dT%H:%M"
        )

        capacity = int(
            parking_info[parking_id]["Capacity"]
        )

        # Prepare input features in the same order used in training
        features = pd.DataFrame([{
            "ParkingCode": parking_mapping[parking_id],
            "Capacity": capacity,
            "Hour": timestamp.hour,
            "DayOfWeek": timestamp.weekday(),
            "Month": timestamp.month
        }])

        # STEP 5: Predict occupancy
        predicted_occupancy = float(
            model.predict(features)[0]
        )

        occupied = max(
            0,
            min(capacity, round(predicted_occupancy))
        )

        # STEP 6: Calculate available spaces
        available = capacity - occupied
        free_percentage = (available / capacity) * 100

        # STEP 7: Classify parking availability
        if free_percentage >= 60:
            availability = "High"
        elif free_percentage >= 30:
            availability = "Medium"
        else:
            availability = "Low"

        # STEP 8: Return results to the website
        return jsonify({
            "location_name": parking_info[parking_id]["ParkingName"],
            "parking_id": parking_id,
            "vehicle_type": vehicle_type,
            "date_time": timestamp.strftime("%d-%m-%Y %H:%M"),
            "capacity": capacity,
            "occupied": occupied,
            "available": available,
            "availability": availability,
            "free_percentage": round(free_percentage, 1)
        })

    except ValueError:
        return jsonify({
            "error": "Please enter a valid date and time."
        }), 400

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "Prediction failed. Please check the terminal."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
