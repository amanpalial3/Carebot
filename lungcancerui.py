import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from streamlit_lottie import st_lottie
import requests
import lung_cancer

# Set page config
# st.set_page_config(layout="wide", page_title="Lung Cancer Risk Assessment", page_icon="🫁")
def lung_cancer_prediction():
# Custom CSS for a beautiful design
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

        * {font-family: 'Roboto', sans-serif;}

        h1 {
            color: #3498db;
            font-weight: 700;
            font-size: 3em;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        h2 {
            color: #3498db;
            font-weight: 600;
            font-size: 1.8em;
            margin-top: 30px;
            margin-bottom: 20px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }

        .stButton>button {
            background-color: #2ecc71;
            color: white;
            font-weight: 500;
            padding: 0.7em 1.2em;
            border-radius: 20px;
            border: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #27ae60;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        }

        .stSelectbox>div>div {
            background-color: light black;
            border-radius: 8px;
        }

        .stNumberInput>div>div>input {
            background-color: #ecf0f1;
            border-radius: 8px;
        }

        .plot-container {
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            border-radius: 12px;
            background-color: #f9f9f9;
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
    st.markdown("<h1>Lung Cancer Risk Assessment🫁</h1>", unsafe_allow_html=True)

    # Load and display Lottie animation
    lottie_lungs = load_lottieurl("https://lottie.host/4d5b6e17-584a-4afc-9e9e-942a440fbd6d/pcy7LQ6rlf.json")
    st_lottie(lottie_lungs, height=250, key="lungs_animation")

    # Create two columns for input
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h2>Personal Information</h2>", unsafe_allow_html=True)
        GENDER = st.radio('GENDER', options=['Male', 'Female'],horizontal=True)
        GENDER = 0 if GENDER == "Female" else 1
        AGE = st.number_input("AGE", min_value=1, max_value=120)
        
        st.markdown("<h2>Lifestyle Factors</h2>", unsafe_allow_html=True)
        SMOKING = st.selectbox("SMOKING", options=['Yes', 'No'])
        SMOKING = 1 if SMOKING=='No' else 2
        ALCOHOL = st.selectbox("ALCOHOL CONSUMING", options=['Yes', 'No'])
        ALCOHOL = 1 if ALCOHOL=='No' else 2
        st.markdown("<h2>Physical Symptoms</h2>", unsafe_allow_html=True)
        YELLOW_FINGERS= st.selectbox("YELLOW FINGERS", options=['Yes', 'No'])
        YELLOW_FINGERS = 1 if YELLOW_FINGERS=='No' else 2
        WHEEZING = st.selectbox("WHEEZING", options=['Yes', 'No'])
        WHEEZING = 1 if WHEEZING=='No' else 2
        COUGHING = st.selectbox("COUGHING", options=['Yes', 'No'])
        COUGHING = 1 if COUGHING=='No' else 2
        SHORTNESS_OF_BREATH = st.selectbox("SHORTNESS OF BREATH", options=['Yes', 'No'])
        SHORTNESS_OF_BREATH = 1 if SHORTNESS_OF_BREATH=='No' else 2

    with col2:
        st.markdown("<h2>Mental Health</h2>", unsafe_allow_html=True)
        ANXIETY = st.selectbox("ANXIETY", options=['Yes', 'No'])
        ANXIETY= 1 if ANXIETY=='No' else 2
        PEER_PRESSURE = st.selectbox("PEER PRESSURE", options=['Yes', 'No'])
        PEER_PRESSURE = 0 if PEER_PRESSURE=='No' else 1
        
        st.markdown("<h2>General Health</h2>", unsafe_allow_html=True)
        CHRONIC_DISEASE = st.selectbox("CHRONIC DISEASE", options=['Yes', 'No'])
        CHRONIC_DISEASE = 1 if CHRONIC_DISEASE=='No' else 2
        FATIGUE = st.selectbox("FATIGUE", options=['Yes', 'No'])
        FATIGUE = 1 if FATIGUE=='No' else 2
        ALLERGY = st.selectbox("ALLERGY", options=['Yes', 'No'])
        ALLERGY = 1 if ALLERGY=='No' else 2
        
        st.markdown("<h2>Additional Symptoms</h2>", unsafe_allow_html=True)
        SWALLOWING_DIFFICULTY = st.selectbox("SWALLOWING DIFFICULTY", options=['Yes', 'No'])
        SWALLOWING_DIFFICULTY = 1 if SWALLOWING_DIFFICULTY=='No' else 2
        CHEST_PAIN = st.selectbox("CHEST PAIN", options=['Yes', 'No'])
        CHEST_PAIN = 1 if CHEST_PAIN=='No' else 2

    if st.button("Assess Lung Cancer Risk"):
        # Collect data for prediction
        data = (GENDER, AGE, SMOKING, YELLOW_FINGERS, ANXIETY, PEER_PRESSURE, CHRONIC_DISEASE, FATIGUE, ALLERGY, WHEEZING, ALCOHOL, COUGHING, SHORTNESS_OF_BREATH, SWALLOWING_DIFFICULTY, CHEST_PAIN)
        
        if all(x is not None for x in data):
            result, risk_percentage = lung_cancer.check(data)
            
            
            st.markdown("<h2>Prediction Results</h2>", unsafe_allow_html=True)
            # st.write(f"Risk Percentage: {risk_percentage:.2f}%")
            
            if result == 1:
                st.error(f"❗ Lung Cancer Detected! Risk Level: **{risk_percentage}%**")
                if risk_percentage <= 30:
                    st.info("### Suggested Actions (Low Risk):\n- Monitor any changes in symptoms.\n- Avoid smoking and exposure to pollutants.\n- Regular check-ups with a doctor.")
                elif 30 < risk_percentage <= 60:
                    st.warning("### Suggested Actions (Moderate Risk):\n- Schedule a consultation with an oncologist.\n- Get chest X-rays or CT scans.\n- Maintain a healthy lifestyle.")
                elif 60 < risk_percentage <= 90:
                    st.warning("### Suggested Actions (High Risk):\n- Immediate medical evaluation is recommended.\n- Get a thorough diagnostic test (e.g., biopsy).\n- Follow oncologist's treatment plan.")
                else:
                    st.error("### Suggested Actions (Very High Risk):\n- Seek immediate medical intervention.\n- Start treatment as recommended by a specialist.\n- Follow a personalized cancer treatment plan.")
                
                # st.error(f"❗ Based on the provided information, there might be an ELEVATED risk of lung cancer ({risk_percentage:.2f}%). Please consult with a healthcare professional.")
            else:
                st.success(f"✅ Based on the provided information, the assessed risk is LOW ({risk_percentage:.2f}%).")
                if risk_percentage <= 30:
                    st.info("### Precautions (Low Risk):\n- Avoid exposure to carcinogens.\n- Stay active and maintain a healthy diet.\n- Get regular health check-ups.")
                elif 30 < risk_percentage <= 60:
                    st.info("### Precautions (Moderate Risk):\n- Start regular screenings (e.g., chest X-rays).\n- Avoid smoking and environmental pollutants.")
            st.subheader("Educational Resources")
            st.write("- [Understanding Lung Cancer](https://www.who.int/news-room/fact-sheets/detail/lung-cancer)")
            st.write("- [Prevention Tips for Lung Cancer](https://www.cancer.gov/types/lung/patient/lung-prevention-pdq)")
            st.write("- [Lung Cancer Test Suggestions](https://www.metropolisindia.com/blog/health-wellness/different-tests-for-lung-cancer-detection)")
            st.subheader("Doctors List:")
            st.write("- [Lung Cancer Specialist](https://www.askapollo.com/diseases/lung-cancer)")
        # Visualizations
        st.markdown("<h2>Risk Factor Analysis</h2>", unsafe_allow_html=True)
        
        # Convert 'Yes'/'No' to 1/0 for visualization
        risk_factors = {
            'Smoking': SMOKING,
            'Alcohol': ALCOHOL,
            'Yellow Fingers': YELLOW_FINGERS,
            'Anxiety': ANXIETY,
            'Chronic Disease': CHRONIC_DISEASE,
            'Fatigue': FATIGUE,
            'Allergy': ALLERGY,
            'Wheezing': WHEEZING,
            'Coughing': COUGHING,
            'Shortness of Breath': SHORTNESS_OF_BREATH,
            'Swallowing Difficulty': SWALLOWING_DIFFICULTY,
            'Chest Pain': CHEST_PAIN
        }
        
        df = pd.DataFrame(risk_factors, index=[0])

        fig = go.Figure(data=[go.Bar(
            x=df.columns,
            y=df.iloc[0],
            marker=dict(color='rgb(34, 163, 171)')
        )])

        fig.update_layout(title="Risk Factor Analysis",
                          xaxis_title="Factors",
                          yaxis_title="Presence (1 = Yes, 0 = No)")
        st.plotly_chart(fig)