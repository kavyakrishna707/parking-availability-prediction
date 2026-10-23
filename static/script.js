
const form = document.getElementById("predictionForm");
const parkingInput = document.getElementById("parking_id");
const dateTimeInput = document.getElementById("date_time");
const predictButton = document.getElementById("predictButton");
const statusMessage = document.getElementById("statusMessage");

const resultCard = document.getElementById("resultCard");
const emptyState = document.getElementById("emptyState");

const vehicleIcons = {
    Car: "🚗",
    Bike: "🏍️",
    Bus: "🚌",
    Truck: "🚚",
    Other: "🚙"
};

// Set the default date/time to the current local time.
function setDefaultDateTime() {
    const now = new Date();

    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());

    dateTimeInput.value = now.toISOString().slice(0, 16);
}

setDefaultDateTime();

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const parkingId = parkingInput.value;
    const vehicleType = document.querySelector(
        'input[name="vehicle_type"]:checked'
    )?.value;
    const dateTime = dateTimeInput.value;

    if (!parkingId || !vehicleType || !dateTime) {
        statusMessage.textContent =
            "Please select a location, vehicle type, and arrival time.";
        statusMessage.className = "status";
        return;
    }

    predictButton.disabled = true;
    predictButton.querySelector(".button-text").textContent =
        "Predicting availability...";

    statusMessage.textContent = "";
    statusMessage.className = "status";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                parking_id: parkingId,
                vehicle_type: vehicleType,
                date_time: dateTime
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.error || "Unable to predict parking availability."
            );
        }

        // Display the location and trip details.
        document.getElementById("parkingResult").textContent =
            result.location_name;

        document.getElementById("timeResult").textContent =
            "Arrival: " + result.date_time;

        document.getElementById("vehicleResult").textContent =
            result.vehicle_type;

        document.getElementById("resultVehicleIcon").textContent =
            vehicleIcons[result.vehicle_type] || "🚘";

        // Display availability category.
        document.getElementById("availabilityResult").textContent =
            result.availability;

        const availabilityBanner = document.querySelector(
            ".availability-banner"
        );

        availabilityBanner.className =
            "availability-banner " + result.availability.toLowerCase();

        const availabilityIcon = document.getElementById("availabilityIcon");

        if (result.availability === "High") {
            availabilityIcon.textContent = "✓";
        } else if (result.availability === "Medium") {
            availabilityIcon.textContent = "!";
        } else {
            availabilityIcon.textContent = "×";
        }

        // Display occupancy numbers.
        document.getElementById("capacityResult").textContent =
            result.capacity;

        document.getElementById("occupiedResult").textContent =
            result.occupied;

        document.getElementById("availableResult").textContent =
            result.available;

        document.getElementById("percentageResult").textContent =
            result.free_percentage + "% free";

        // Occupancy bar shows the percentage of spaces already occupied.
        const occupiedPercentage = result.capacity > 0
            ? (result.occupied / result.capacity) * 100
            : 0;

        document.getElementById("occupancyBar").style.width =
            occupiedPercentage + "%";

        // Update the results panel.
        emptyState.classList.add("hidden");
        resultCard.classList.remove("hidden");

        statusMessage.textContent = "Prediction completed successfully.";
        statusMessage.className = "status success";

    } catch (error) {
        statusMessage.textContent = error.message;
        statusMessage.className = "status";
    } finally {
        predictButton.disabled = false;

        predictButton.querySelector(".button-text").textContent =
            "Predict Availability";
    }
});
