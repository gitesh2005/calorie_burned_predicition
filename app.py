import streamlit as st
import pandas as pd
import pickle

# Load model and feature order
model = pickle.load(open("calorie_burned_model.pkl", "rb"))
feature_order = pickle.load(open("feature_order.pkl", "rb"))

st.title("🔥 Calories Burned Prediction App")

st.markdown("Enter your personal and workout details:")

# Inputs
age = st.number_input("Age", min_value=10, max_value=100)
weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)
height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, step=0.01)
duration = st.number_input("Session Duration (hours)", min_value=0.1, max_value=5.0, step=0.1)

gender = st.selectbox("Gender", ["Female", "Male"])
workout = st.selectbox("Workout Type", ["Cardio", "HIIT", "Strength", "Yoga"])

# One-hot encoding manually (drop_first=True)
gender_male = 1 if gender == "Male" else 0

# Workout_Type dummies — drop_first=True => Cardio is dropped
workout_type_dict = {
    "Cardio": [0, 0, 0],   # dropped
    "HIIT":   [1, 0, 0],
    "Strength": [0, 1, 0],
    "Yoga": [0, 0, 1]
}
workout_type_hiit, workout_type_strength, workout_type_yoga = workout_type_dict[workout]

# Construct input
input_data = {
    'Age': age,
    'Weight (kg)': weight,
    'Height (m)': height,
    'Session_Duration (hours)': duration,
    'Workout_Type_HIIT': workout_type_hiit,
    'Workout_Type_Strength': workout_type_strength,
    'Workout_Type_Yoga': workout_type_yoga,
    'Gender_Male': gender_male
}

input_df = pd.DataFrame([input_data])[feature_order]

# Prediction
if st.button("Predict Calories Burned"):
    prediction = model.predict(input_df)[0]
    st.success(f"🔥 Estimated Calories Burned: {prediction:.2f} kcal")
