import streamlit as st
import heart
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
# import v

def heart_disease_prediction():
    st.markdown("<h1>Heart Disease Prediction</h1>", unsafe_allow_html=True)
    
    option = option_menu("", options=['Prediction'], orientation='horizontal')
    if option=='Prediction':
        st.markdown("<h1>Heart Disease Prediction</h1>", unsafe_allow_html=True)
        def load_lottieurl(url: str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()

        # Your custom CSS here (unchanged)
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
            
            * {font-family: 'Roboto', sans-serif;}
            
            h1 {
                color: orange;
                font-weight: 700;
                font-size: 3em; 
                text-align: center;
                margin-bottom: 30px;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0% {
                    transform: scale(1);
                }
                50% {
                    transform: scale(1.05);
                }
                100% {
                    transform: scale(1);
                }
            }
            
            h3 {
                color: #34495e;
                font-weight: 400;
                font-size: 1.5em;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            
            .stButton>button {
                background-color: #3498db;
                color: white;
                font-weight: 500;
                padding: 0.5em 1em;
                border-radius: 5px;
            }
            
            .stButton>button:hover {
                background-color: #2980b9;
            }
            
            .stSelectbox>div>div {
                background-color: #000000;
            }
            
            .stNumberInput>div>div>input {
                background-color: #ecf0f1;
            }
            
            .plot-container {
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                padding: 20px;
                border-radius: 10px;
                background-color: #ecf0f1;
            }
                    
            </style>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])

        with col1:
            st.header("Personal Information")
            age = st.number_input("Age", min_value=25, max_value=100)
            gender = st.radio('Gender', options=['Male', 'Female'])
            gender = 0 if gender == "Female" else 1

            st.header("Health Metrics")
            cholesterol = st.number_input("Cholesterol in mg/dL",help="Cholesterol level in mg/dL")
            blood_pressure = st.number_input("Blood Pressure(mmHg)",help="Systolic blood pressure in mmHg")
            heart_rate = st.number_input("Heart Rate")

            st.header("Lifestyle Factors")
            smoke = st.selectbox("Smoking", options=['Select', 'Current', 'Former', 'Never'])
            smoke = 2 if smoke == "Never" else 0 if smoke == "Current" else 1 if smoke == "Former" else None

            alcohol_intake = st.selectbox("Alcohol Intake", options=['Select', 'Heavy', 'No alcohol intake', 'Moderate'])
            alcohol_intake = 0 if alcohol_intake == "Heavy" else 2 if alcohol_intake == "No alcohol intake" else 1 if alcohol_intake == "Moderate" else None

            exercise_hours = st.number_input("Exercise Hours")

            st.header("Medical History")
            family_history = st.selectbox("Family History", options=['Select', 'Yes', 'No'], help="Do you have a family history of heart disease?")
            family_history = 0 if family_history == "No" else 1 if family_history == "Yes" else None
            
            Diabetes = st.selectbox("Diabetes", options=['Select', 'Yes', 'No'], help="Do you have diabetes?")
            Diabetes = 0 if Diabetes == "No" else 1 if Diabetes == "Yes" else None
            
            Obesity = st.selectbox("Obesity", options=['Select', 'Yes', 'No'], help="Are you obese?")
            Obesity = 0 if Obesity == "No" else 1 if Obesity == "Yes" else None

            stress_level = st.slider("Stress Level", 1, 10)
            blood_sugar = st.number_input("Blood Sugar(mg/dL)", help="Fasting blood sugar level in mg/dL")

            exercise_induced_angina = st.selectbox("Exercise Induced Angina", options=['Select', 'Yes', 'No'], help="Do you experience angina induced by exercise?")
            exercise_induced_angina = 0 if exercise_induced_angina == "No" else 1 if exercise_induced_angina == "Yes" else None

            chest_pain_type = st.selectbox("Chest Pain Type", options=['Select', 'Atypical Angina', 'Typical Angina', 'Non-anginal Pain', 'Asymptomatic'], help="Select your chest pain type")
            chest_pain_type = 1 if chest_pain_type == "Atypical Angina" else 3 if chest_pain_type == "Typical Angina" else 2 if chest_pain_type == "Non-anginal Pain" else 0 if chest_pain_type == "Asymptomatic" else None
            # if st.button("Check"):
            #     data = (age, gender, cholesterol, blood_pressure, heart_rate, smoke, alcohol_intake, exercise_hours, family_history, Diabetes, Obesity, stress_level, blood_sugar, exercise_induced_angina, chest_pain_type)
            #     if None not in data:
            #         result = heart.check(data)
            #         st.write(result)
                    # if res == 1:
                    #     st.error("❗ Heart disease detected")
                    # else:
                    #     st.success("✅ No heart disease detected")
                    #     st.balloons()
            if st.button("Check"):
                data = (age, gender, cholesterol, blood_pressure, heart_rate, smoke, alcohol_intake, exercise_hours, 
                        family_history, Diabetes, Obesity, stress_level, blood_sugar, exercise_induced_angina, chest_pain_type)
                
                if None not in data:
                    result, risk_percentage = heart.check(data)
                    st.markdown("<h2>Prediction Results</h2>", unsafe_allow_html=True)
                    if result == 1:
                        st.error(f"❗ Heart Disease Detected! Risk Level: **{risk_percentage}%**")
                        # st.write(f"Risk Percentage: {risk_percentage:.2f}%")
                    
                        if risk_percentage < 20:
                            st.success("✅ Low risk of heart disease detected.")
                            st.markdown("### Recommendations:")
                            st.write("- Maintain a healthy lifestyle.")
                            st.write("- Regular exercise (at least 30 minutes daily).")
                            st.write("- Balanced diet with fruits and vegetables.")
                        
                        elif 20 <= risk_percentage < 50:
                            st.warning("⚠️ Moderate risk of heart disease detected.")
                            st.markdown("### Recommendations:")
                            st.write("- Schedule a consultation with a cardiologist.")
                            st.write("- Monitor cholesterol and blood pressure regularly.")
                            st.write("- Consider lifestyle changes: quitting smoking, reducing alcohol, etc.")
                            st.write("- Tests to consider: ECG, blood tests.")
                        
                        else:
                            st.error("❗ High risk of heart disease detected.")
                            st.markdown("### Recommendations:")
                            st.write("- Immediate consultation with a cardiologist.")
                            st.write("- Diagnostic tests: Echocardiogram, stress test, angiography.")
                            st.write("- Potential medications: statins, aspirin, or other prescribed drugs.")
                            st.write("- Avoid strenuous physical activities.")
                else:
                    st.error("Please fill out all fields.")

                    
                    

        with col2:
            lottie_heart = load_lottieurl("https://lottie.host/7543377c-efca-4a7e-91fc-5e3427a24cae/IO5VpNGdRB.json")
            st_lottie(lottie_heart, height=300, key="heart_animation")

            
    # elif option=='Visuals':
    #     v.show_visualizations()