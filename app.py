import streamlit as st
import pandas as pd
import plotly.express as px
import pdfplumber
import re
import requests
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

from heartui import heart_disease_prediction
from diabetesui import diabetes_prediction
from lungcancerui import lung_cancer_prediction
from liverui import liver_disease_assessment
from tumor.tumorui import brain_detection

st.set_page_config(page_title="CareBot + Multi-Diagnose", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .main-container { background: rgba(255,255,255,0.95); border-radius: 30px; padding: 2rem; margin: 1rem; }
    .animated-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem; }
    .floating-card { transition: all 0.3s ease; background: white; padding: 1rem; border-radius: 15px; text-align: center; }
    .floating-card:hover { transform: translateY(-5px); }
    .glow-text { text-shadow: 0 0 20px rgba(102,126,234,0.5); background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; padding: 1rem; color: white; text-align: center; }
    .bot-avatar { font-size: 4rem; }
    .disease-card { background: linear-gradient(145deg, #ffffff, #e6e6e6); border-radius: 20px; padding: 1.5rem; box-shadow: 5px 5px 15px #d1d9e6, -5px -5px 15px #ffffff; margin-bottom: 2rem; transition: transform 0.3s ease, box-shadow 0.3s ease; text-align: center; }
    .disease-card:hover { transform: translateY(-5px); }
    .disease-card h3 { color: #0f3460; margin-bottom: 0.5rem; font-size: 1.5em; }
    .stButton>button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 25px; width: 100%; }
    .stButton>button:hover { transform: scale(1.05); }
    .back-button .stButton button { background-color: #e94560; margin-bottom: 1rem; }
    hr { display: none; }
</style>
""", unsafe_allow_html=True)

if 'report_text' not in st.session_state:
    st.session_state.report_text = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'main_menu' not in st.session_state:
    st.session_state.main_menu = "Dashboard"

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def go_home():
    st.session_state.page = "Home"
    st.rerun()

def back_button():
    if st.button("← Back to Diseases", key="back_disease"):
        go_home()

def extract_pdf_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join([p.extract_text() or "" for p in pdf.pages])

def extract_medical_params(text):
    text_lower = text.lower()
    params = {
        "Patient Name": None, "Age": None, "Gender": None,
        "Blood Pressure": None, "Cholesterol": None,
        "Hemoglobin": None, "Blood Sugar": None
    }
    name_match = re.search(r'Name\s*:\s*([A-Z][A-Za-z\s]+?)(?=\s+Lab\s+No\.|\s+Age|\n|$)', text, re.IGNORECASE)
    if name_match:
        params["Patient Name"] = name_match.group(1).strip()
    age_match = re.search(r'Age\s*:\s*(\d{1,3})', text, re.IGNORECASE)
    if age_match:
        params["Age"] = int(age_match.group(1))
    if 'female' in text_lower:
        params["Gender"] = "Female"
    elif 'male' in text_lower:
        params["Gender"] = "Male"
    bp_match = re.search(r'(\d{2,3})\s*[/]\s*(\d{2,3})', text)
    if bp_match:
        params["Blood Pressure"] = f"{bp_match.group(1)}/{bp_match.group(2)}"
    chol_match = re.search(r'(?:cholesterol|chol)[:\s]*(\d{2,3})', text_lower)
    if chol_match:
        params["Cholesterol"] = f"{chol_match.group(1)} mg/dL"
    hb_match = re.search(r'(?:hemoglobin|hb)[:\s]*(\d{1,2}\.?\d*)', text_lower)
    if hb_match:
        params["Hemoglobin"] = f"{hb_match.group(1)} g/dL"
    glucose_match = re.search(r'(?:glucose|blood sugar)[:\s]*(\d{2,4})', text_lower)
    if glucose_match:
        params["Blood Sugar"] = f"{glucose_match.group(1)} mg/dL"
    return params

def chat_answer(question, report_text):
    q = question.lower()
    if "name" in q:
        return "Patient name is shown in extracted data."
    elif "age" in q:
        return "Age is listed under extracted parameters."
    elif "blood pressure" in q or "bp" in q:
        return "Blood pressure reading is shown."
    elif "cholesterol" in q:
        return "Cholesterol level is extracted."
    elif "sugar" in q or "glucose" in q:
        return "Blood glucose value is available."
    else:
        return "Ask about any extracted parameter like name, age, BP, cholesterol, etc."

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/robot-2.png", width=80)
    main_menu = option_menu(
        menu_title=None,
        options=["🏠 Dashboard", "📄 Report Analysis", "📊 Analytics", "💬 CareBot Chat", "📝 Manual Prediction", "ℹ️ About"],
        icons=["house", "file-text", "graph-up", "chat-dots", "activity", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important"},
            "icon": {"color": "#667eea", "font-size": "1.2rem"},
            "nav-link": {"text-align": "center", "margin": "0.2rem", "border-radius": "10px"},
            "nav-link-selected": {"background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"},
        }
    )
    st.markdown("---")
    st.metric("Reports Analyzed", "156", "+12")
    st.metric("Active Users", "2.4k", "+18%")

if main_menu == "🏠 Dashboard":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; background: linear-gradient(135deg, #facc15, #ff8c00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">✨ Welcome to CareBot + Multi-Diagnose</h2>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    for col, val, txt in [(col1, "5+", "Diseases"), (col2, "2.5K+", "Reports"), (col3, "24/7", "Support"), (col4, "📊", "Analytics")]:
        with col:
            st.markdown(f'<div class="metric-card">{val}<br>{txt}</div>', unsafe_allow_html=True)
    st.markdown("### 🚀 Features")
    st.info("📄 **PDF Report Analysis** – Upload lab report to extract medical values")
    st.info("📝 **Manual Prediction** – Choose a disease and get AI/ML prediction")
    st.info("💬 **Chat** – Ask questions about your report")
    st.info("📊 **Analytics** – Visualize health trends")
    st.markdown('</div>', unsafe_allow_html=True)

elif main_menu == "📄 Report Analysis":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        uploaded = st.file_uploader("Upload Medical Report (PDF)", type=['pdf'])
        if uploaded:
            with st.spinner("Reading PDF..."):
                text = extract_pdf_text(uploaded)
                st.session_state.report_text = text
                st.success("✅ Report processed!")
                with st.expander("View raw text"):
                    st.text(text[:1000])
    with col2:
        if st.session_state.report_text:
            params = extract_medical_params(st.session_state.report_text)
            st.markdown("### 📋 Extracted Patient Data")
            items = [(k, v) for k, v in params.items() if v is not None]
            if items:
                for key, value in items:
                    st.markdown(f"- **{key}:** {value}")
            else:
                st.info("No values extracted. Try a more detailed report.")
    st.markdown('</div>', unsafe_allow_html=True)

elif main_menu == "📊 Analytics":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Sample Health Indicators")
    sample_df = pd.DataFrame({
        'Parameter': ['Blood Pressure', 'Cholesterol', 'Hemoglobin', 'Blood Sugar'],
        'Value': [120, 180, 13.5, 100]
    })
    fig = px.bar(sample_df, x='Parameter', y='Value', color='Parameter', title="Example Health Metrics")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Demo chart – upload report to see real data.")
    st.markdown('</div>', unsafe_allow_html=True)

elif main_menu == "💬 CareBot Chat":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("### 💬 Chat with CareBot")
    for q, a in st.session_state.chat_history[-10:]:
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant", avatar="🤖"):
            st.write(a)
    if prompt := st.chat_input("Ask about your health report..."):
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant", avatar="🤖"):
            resp = chat_answer(prompt, st.session_state.report_text)
            st.write(resp)
        st.session_state.chat_history.append((prompt, resp))
    if not st.session_state.report_text:
        st.info("Upload a report for better answers.")
    st.markdown('</div>', unsafe_allow_html=True)

elif main_menu == "📝 Manual Prediction":
    if st.session_state.page == "Home":
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; color:#FFA500;'>MANUAL PREDICTION</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        diseases = [
            {"name": "Heart Disease", "icon": "❤️", "func": heart_disease_prediction},
            {"name": "Diabetes", "icon": "💉", "func": diabetes_prediction},
            {"name": "Lungs Cancer", "icon": "🫁", "func": lung_cancer_prediction},
            {"name": "Brain Tumor", "icon": "🧠", "func": brain_detection},
            {"name": "Liver Disease", "icon": "🫧", "func": liver_disease_assessment}
        ]
        for i, d in enumerate(diseases):
            with [col1, col2, col3][i % 3]:
                st.markdown(f"""
                <div class="disease-card">
                    <h3>{d['icon']} {d['name']}</h3>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Check Now", key=f"btn_{d['name']}"):
                    st.session_state.page = d['name']
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="back-button">', unsafe_allow_html=True)
        back_button()
        st.markdown('</div>', unsafe_allow_html=True)
        if st.session_state.page == "Heart Disease":
            heart_disease_prediction()
        elif st.session_state.page == "Diabetes":
            diabetes_prediction()
        elif st.session_state.page == "Lungs Cancer":
            lung_cancer_prediction()
        elif st.session_state.page == "Brain Tumor":
            brain_detection()
        elif st.session_state.page == "Liver Disease":
            liver_disease_assessment()

elif main_menu == "ℹ️ About":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;">
        <div style="font-size:4rem;">🤖🩺</div>
        <h2>CareBot + Multi-Diagnose</h2>
        <p>Integrated AI Health Assistant</p>
    </div>
    ### 🎯 Features
    - **PDF Report Analysis** – Extracts patient name, age, BP, cholesterol, etc.
    - **Manual Prediction** – Heart, Diabetes, Lung, Brain, Liver (ML-based predictions)
    - **Chat** – Ask questions about your extracted report
    - **Analytics** – Visual health trends
    ### ⚠️ Disclaimer
    For informational purposes only. Not a substitute for medical advice.
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 CareBot | AI-Powered Health Assistant")