import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from streamlit_lottie import st_lottie
import requests
import liver
import base64

def liver_disease_assessment():

    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        * {font-family: 'Poppins', sans-serif;}
        h1 {color: #2c3e50; font-weight: 700; font-size: 2.8em; text-align: center; margin-bottom: 30px;}
        h2 {color: #34495e; font-weight: 600; font-size: 1.6em; margin-top: 30px; margin-bottom: 20px;
            border-bottom: 2px solid #3498db; padding-bottom: 10px;}
        .stButton>button {
            background-color: #3498db; color: white; font-weight: 500;
            padding: 0.7em 1.2em; border-radius: 20px; border: none;
        }
        .stButton>button:hover {background-color: #2980b9;}
    </style>
    """, unsafe_allow_html=True)

    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    st.markdown("<h1>🩺 Liver Disease Risk Assessment</h1>", unsafe_allow_html=True)
    lottie_liver = load_lottieurl("https://lottie.host/1418a8de-ef1f-4a7d-825d-9a883bcadfef/klvWeF175I.json")
    st_lottie(lottie_liver, height=300, key="liver_animation")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h2>Personal Information</h2>", unsafe_allow_html=True)
        age_of_the_patient = st.number_input("Age of the Patient", 0, 120)
        gender = st.radio("Gender", ["Male", "Female"])
        gender_of_the_patient = 1 if gender == "Male" else 0

        st.markdown("<h2>Liver Function Tests</h2>", unsafe_allow_html=True)
        total_bilirubin = st.number_input("Total Bilirubin", 0.0, 30.0)
        direct_bilirubin = st.number_input("Direct Bilirubin", 0.0, 15.0)
        alkphos_alkaline_phosphotase = st.number_input("Alkaline Phosphatase", 0, 1000)

    with col2:
        st.markdown("<h2>Liver Enzymes</h2>", unsafe_allow_html=True)
        sgpt = st.number_input("SGPT (Alamine Aminotransferase)", 0, 1000)
        sgot = st.number_input("SGOT (Aspartate Aminotransferase)", 0, 1000)

        st.markdown("<h2>Protein Levels</h2>", unsafe_allow_html=True)
        total_proteins = st.number_input("Total Proteins", 0.0, 10.0)
        alb_albumin = st.number_input("Albumin", 0.0, 6.0)
        ag_ratio = st.number_input("A/G Ratio", 0.0, 3.0)

    # --------------------------
    # Predict Button
    # --------------------------
    if st.button("Assess Liver Disease Risk"):

        data = (
            age_of_the_patient,
            gender_of_the_patient,
            total_bilirubin,
            direct_bilirubin,
            alkphos_alkaline_phosphotase,
            sgpt,
            sgot,
            total_proteins,
            alb_albumin,
            ag_ratio
        )

        if all(x is not None for x in data):

            res1 = liver.check(data)

            if res1 == 1:
                st.error("❗ High Risk Detected")
                st.write("The model suggests a **higher chance of liver disease** based on your entered values.")
                st.warning("Please consult a certified medical professional for confirmation and further advice.")
            else:
                st.success("✅ Low Risk")
                st.write("Your inputs indicate a **low likelihood of liver disease**.")
                st.info("Maintaining a healthy lifestyle and regular checkups is recommended.")

        else:
            st.error("⚠ Please fill all values before prediction.")
