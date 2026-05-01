import streamlit as st
import plotly.graph_objects as go
import diabets
import plotly.express as px
import pandas as pd
from streamlit_lottie import st_lottie
import requests


# Set page config
# st.set_page_config(layout="wide", page_title="Diabetes Risk Assessment", page_icon="🩺")
def diabetes_prediction():
# Custom CSS for a beautiful design
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

        * {font-family: 'Poppins', sans-serif;}

        h1 {
            color: #6c5ce7;
            font-weight: 700;
            font-size: 2.8em;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        h2 {
            color:  pink;
            font-weight: 600;
            font-size: 1.6em;
            margin-top: 30px;
            margin-bottom: 20px;
            border-bottom: 2px solid #6c5ce7;
            padding-bottom: 10px;
        }

        .stButton>button {
            background-color: #00b894;
            color: white;
            font-weight: 500;
            padding: 0.7em 1.2em;
            border-radius: 20px;
            border: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #00a187;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        }

        .stSelectbox>div>div {
            background-color: light black;
            border-radius: 8px;
        }

        .stNumberInput>div>div>input {
            background-color: #f0f0f0;
            border-radius: 8px;
        }

        .plot-container {
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            border-radius: 12px;
            background-color: #ffffff;
            margin-top: 30px;
        }
    </style>
    """, unsafe_allow_html=True)

    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    # Main layout
    st.markdown("<h1>🩺 Diabetes Risk Assessment</h1>", unsafe_allow_html=True)

    # Load and display Lottie animation
    lottie_diabetes = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_tbjuenb2.json")
    st_lottie(lottie_diabetes, height=200, key="diabetes_animation")

    # Create two columns for input
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h2>Personal Information</h2>", unsafe_allow_html=True)
        
        gender = st.radio('Gender', options=['Male', 'Female'], 
                        help="Select your biological sex.")
        gender = 0 if gender == "Female" else 1
        age = st.number_input("Age", min_value=25, max_value=100)
        
        bmi = st.number_input("BMI (Body Mass Index)", min_value=10.0, max_value=50.0, step=0.1, 
                            help="BMI is a measure of body fat based on height and weight. If unsure, use a BMI calculator.")
        
        st.markdown("<h2>Medical History</h2>", unsafe_allow_html=True)
        
        hypertension = st.selectbox("Hypertension", options=['No', 'Yes'], 
                                    help="Select 'Yes' if you have been diagnosed with high blood pressure.")
        hypertension = 0 if hypertension=='No' else 1
        heart_disease = st.selectbox("Heart Disease", options=['No', 'Yes'], 
                                    help="Select 'Yes' if you have any history of heart disease.")
        heart_disease= 0 if heart_disease=='No' else 1
    with col2:
        st.markdown("<h2>Lifestyle Factors</h2>", unsafe_allow_html=True)
        
        smoking_history = st.selectbox("Smoking History", options=['Never', 'Former', 'Current','Not Current','Ever', 'No info'], 
                                    help="Select your current smoking status.")
        if smoking_history=='Never':
            smoking_history=4
        elif smoking_history=='Former':
            smoking_history=3
        elif smoking_history== 'Current':
            smoking_history=1
        elif smoking_history=='Not Current':
            smoking_history=5
        elif smoking_history=='ever':
            smoking_history=2
        else:
            smoking_history=0

        st.markdown("<h2>Blood Tests</h2>", unsafe_allow_html=True)
        
        hba1c_level = st.number_input("HbA1c Level (%)", min_value=3.0, max_value=9.0, step=0.1, 
                                    help="HbA1c is a measure of your average blood sugar levels over the past 2-3 months.")
        
        blood_glucose_level = st.number_input("Blood Glucose Level (mg/dL)", min_value=70, max_value=300, 
                                            help="This is your current blood sugar level. Fasting levels are typically measured.")
    if st.button("Assess Diabetes Risk"):
        data = (gender, age, hypertension, heart_disease, smoking_history,
                bmi, hba1c_level, blood_glucose_level)

        if all(x is not None for x in data):
            risk_percentage, result = diabets.check(data)
            st.markdown("<h2>Prediction Results</h2>", unsafe_allow_html=True)

            if result == 1:
                st.error(f"❗ Diabetes Detected! Risk Level: **{risk_percentage}%**")
                
                # Suggestions based on risk percentage
                if risk_percentage <= 30:
                    st.info("### Suggested Actions (Low Risk):\n- Monitor blood sugar levels.\n- Maintain a healthy diet.\n- Stay physically active.")
                elif 30 < risk_percentage <= 60:
                    st.warning("### Suggested Actions (Moderate Risk):\n- Consult with a healthcare professional.\n- Adopt a low-glycemic index diet.\n- Avoid sugary foods and beverages.\n- Start regular exercise.")
                elif 60 < risk_percentage <= 90:
                    st.warning("### Suggested Actions (High Risk):\n- Schedule an appointment with a diabetologist.\n- Take prescribed medications if applicable.\n- Strictly avoid processed foods.\n- Engage in daily physical activities like walking or yoga.")
                else:
                    st.error("### Suggested Actions (Very High Risk):\n- Seek immediate medical attention.\n- Follow the doctor's instructions for insulin or medication.\n- Adopt a personalized diabetes management plan.")

            else:
                st.success(f"✅ No Diabetes Detected! Risk Level: **{risk_percentage}%**")
                if risk_percentage <= 30:
                    st.info("### Precautions (Low Risk):\n- Maintain your current lifestyle.\n- Regularly monitor your blood sugar levels.\n- Annual health check-ups are recommended.")
                elif 30 < risk_percentage <= 60:
                    st.info("### Precautions (Moderate Risk):\n- Start incorporating a balanced diet and exercise into your routine.\n- Avoid high-sugar foods.\n- Get periodic blood sugar tests.")

                # if res == 1:
                #     st.error("❗ Based on the provided information, there might be an ELEVATED risk of diabetes.")
                #     st.warning("Please consult with a healthcare professional for a thorough evaluation.")
                
                # else:
                #     st.success("✅ Based on the provided information, the assessed diabetes risk is LOW.")

            
           # Educational Resources
            st.subheader("Educational Resources")
            st.write("- [Understanding Diabetes](https://www.who.int/news-room/fact-sheets/detail/diabetes)")
            st.write("- [Healthy Eating and Diabetes Tips](https://www.nhs.uk/conditions/type-2-diabetes/food-and-keeping-active/)")
            st.write("- [Exercise and Fitness for Diabetes](https://diabetes.org/healthy-living/fitness)")

            st.markdown("<h2>Risk Factor Analysis</h2>", unsafe_allow_html=True)


            
            # BMI gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = bmi,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "BMI", 'font': {'size': 24}},
                gauge = {
                    'axis': {'range': [None, 50], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "darkblue"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 18.5], 'color': '#3498db'},
                        {'range': [18.5, 24.9], 'color': '#2ecc71'},
                        {'range': [24.9, 30], 'color': '#f1c40f'},
                        {'range': [30, 50], 'color': '#e74c3c'}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 30}}))
            
            fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)
        
        # Blood test results
        blood_tests = pd.DataFrame({
            'Test': ['HbA1c', 'Blood Glucose'],
            'Value': [hba1c_level, blood_glucose_level],
            'Normal Range': ['< 5.7%', '< 100 mg/dL']
        })

        
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(blood_tests.columns),
                        fill_color='light green',
                        align='left',
                        font=dict(color='white', size=12)),
            cells=dict(values=[blood_tests.Test, blood_tests.Value, blood_tests['Normal Range']],
                    fill_color='#424d21',
                    align='left'))
        ])
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        

