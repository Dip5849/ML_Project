import streamlit as st
import requests
import time
from streamlit_lottie import st_lottie
import json
import requests as req

# Load Lottie animation
def load_lottieurl(url: str):
    r = req.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Example free Lottie animation (education theme)
lottie_book = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_sSF6EG.json")

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Student Score Prediction", page_icon="📊", layout="centered")

st.title(f"📊 Student Math Score Prediction")

# Show animation above form
st_lottie(lottie_book, height=150, key="book")

st.write("✨ Fill in the student details below !!!")

# Animated form
with st.form("prediction_form"):
    st.markdown("### 📝 Student Information")

    # Animated CSS effect
    st.markdown("""
    <style>
    .stSelectbox, .stNumberInput {
        animation: fadeIn 1.5s ease-in-out;
    }
    @keyframes fadeIn {
        0% {opacity: 0; transform: translateY(10px);}
        100% {opacity: 1; transform: translateY(0);}
    }
    </style>
    """, unsafe_allow_html=True)

    gender = st.selectbox("👩 Gender", ["female", "male"])
    race_ethnicity = st.selectbox("🌍 Race/Ethnicity", ["group B", "group C", "group A", "group D", "group E"])
    parental_level_of_education = st.selectbox(
        "🎓 Parental Level of Education",
        ["bachelor's degree", "some college", "master's degree",
         "associate's degree", "high school", "some high school"]
    )
    lunch = st.selectbox("🍱 Lunch", ["standard", "free/reduced"])
    test_preparation_course = st.selectbox("📚 Test Preparation Course", ["none", "completed"])

    # Numerical inputs
    reading_score = st.number_input("📖 Reading Score", min_value=0, max_value=100, value=70)
    writing_score = st.number_input("✍ Writing Score", min_value=0, max_value=100, value=70)

    submitted = st.form_submit_button("Predict 🚀")

if submitted:
    payload = {
        "gender": gender,
        "race_ethnicity": race_ethnicity,
        "parental_level_of_education": parental_level_of_education,
        "lunch": lunch,
        "test_preparation_course": test_preparation_course,
        "reading_score": reading_score,
        "writing_score": writing_score
    }

    with st.spinner("⏳ Sending data to model..."):
        time.sleep(1)
        response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        prediction = response.json()["prediction"]

        st.success("✅ Prediction received!")

        # Animated progress bar
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        st.metric(label="📌 Predicted Score", value=f"{prediction:.2f}")

    else:
        st.error("❌ Failed to get prediction. Please check backend.")
