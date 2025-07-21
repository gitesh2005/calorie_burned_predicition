import streamlit as st
import pandas as pd
import pickle

# Load trained model and feature order
model = pickle.load(open("calorie_burned_model.pkl", "rb"))
feature_order = pickle.load(open("feature_order.pkl", "rb"))

st.set_page_config(page_title="Calories Burned Predictor", page_icon="🔥")
st.title("🔥 Calories Burned Prediction App")
st.markdown("Fill in your details to estimate your calorie burn:")

# 🧍 User Inputs
age = st.number_input("Age", min_value=10, max_value=100, step=1)
gender = st.selectbox("Gender", ["Female", "Male"])
weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)
height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, step=0.01)
duration = st.number_input("Workout Duration (hours)", min_value=0.1, max_value=5.0, step=0.1)
workout = st.selectbox("Workout Type", ["Cardio", "HIIT", "Strength", "Yoga"])

# 🎯 Manual One-Hot Encoding (Same as training)
gender_male = 1 if gender == "Male" else 0

workout_type_dict = {
    "Cardio": [0, 0, 0],  # dropped first
    "HIIT": [1, 0, 0],
    "Strength": [0, 1, 0],
    "Yoga": [0, 0, 1]
}
Workout_Type_HIIT, Workout_Type_Strength, Workout_Type_Yoga = workout_type_dict[workout]

# 🔄 Create input row in exact feature order
input_dict = {
    'Age': age,
    'Weight (kg)': weight,
    'Height (m)': height,
    'Session_Duration (hours)': duration,
    'Workout_Type_HIIT': Workout_Type_HIIT,
    'Workout_Type_Strength': Workout_Type_Strength,
    'Workout_Type_Yoga': Workout_Type_Yoga,
    'Gender_Male': gender_male
}

# ✅ Ensure exact same order as training
input_df = pd.DataFrame([input_dict])[feature_order]

# 🔮 Predict
if st.button("Predict Calories Burned"):
    prediction = model.predict(input_df)[0]
    st.success(f"🔥 Estimated Calories Burned: **{prediction:.2f} kcal**")
