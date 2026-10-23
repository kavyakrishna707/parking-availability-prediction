🚗 Parking Availability Prediction System

📌 About the Project

The Parking Availability Prediction System is a machine learning-based web application designed to predict parking occupancy and estimate the number of available parking spaces at a selected location and time.

The system uses a Random Forest Regressor trained on parking data to predict the number of occupied spaces. Based on the predicted occupancy and total parking capacity, it calculates the available spaces and displays the availability level as High, Medium, or Low.

✨ Features

- 📍 Select a parking location.
- 📅 Choose a date and time for prediction.
- 🤖 Predict parking occupancy using machine learning.
- 🅿️ Calculate estimated available parking spaces.
- 📊 Display parking availability levels.
- 💻 User-friendly web interface.

🛠️ Technologies Used

- Python — Main programming language
- Flask — Web application backend
- Pandas — Dataset processing
- Scikit-learn — Machine learning model
- HTML, CSS, JavaScript — Frontend development
- Pickle — Saving and loading the trained model
- CSV — Dataset storage

🧠 Machine Learning Model

The project uses the Random Forest Regressor, an ensemble learning algorithm that combines multiple decision trees to predict numerical values.

The model uses parking location, parking capacity, hour, day of the week, and month as input features to predict occupancy.

⚙️ How It Works

1. The user selects a parking location and date and time.
2. The Flask backend processes the input.
3. The trained model predicts the number of occupied spaces.
4. The system calculates the estimated available spaces.
5. The results are displayed on the website.

Formula:

Available Spaces = Total Capacity − Predicted Occupancy

📂 Dataset

The project uses a CSV dataset containing parking locations, capacities, occupancy values, and timestamps. The current dataset is simulated and is intended for learning and demonstration purposes.

🚀 Future Improvements

- Integrate real-time parking occupancy data.
- Compare multiple machine learning algorithms.
- Improve prediction accuracy using real-world datasets.
- Add interactive parking maps.
- Develop a mobile-friendly application.

🎯 Project Goal

The goal is to demonstrate how machine learning can be integrated with web development to build a parking prediction application that may help users plan their parking more efficiently.

Note: Predictions depend on the quality and representativeness of the training data. The current version does not use live parking sensor data.
