
import streamlit as st
st.set_page_config(layout="wide")
from heartui import heart_disease_prediction
import  requests
from tumor.tumorui import brain_detection
from diabetesui import diabetes_prediction
from lungcancerui import lung_cancer_prediction
from liverui import liver_disease_assessment
# from breastcancerui import breast_cancer_prediction
from streamlit_lottie import st_lottie
import joblib

# Animated title


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

body {
    font-family: 'Poppins', sans-serif;
    background-color: #f0f4f8;
    color: #1a1a2e;
        
}

.stApp {
    # background-image: url('https://www.transparenttextures.com/patterns/cubes.png');
    background-color: #000000;
}

.animated-title {
    animation: fadeInUp 1.5s ease-out, pulse 2s infinite;
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
h1 {
    color: #FFA500;
    font-weight: 700;
    font-size: 3.5em;
    text-align: center;
    margin-bottom: 30px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.disease-card {
    background: linear-gradient(145deg, #ffffff, #e6e6e6);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 5px 5px 15px #d1d9e6, -5px -5px 15px #ffffff;
    margin-bottom: 2rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.disease-card:hover {
    transform: translateY(-5px);
    box-shadow: 8px 8px 20px #d1d9e6, -8px -8px 20px #ffffff;
}

.disease-card h3 {
    color: #0f3460;
    margin-bottom: 0.5rem;
    font-size: 1.5em;
}

.stButton>button {
    width: 100%;
    background-color: #16213e;
    color: white;
    border-radius: 30px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background-color: #0f3460;
    transform: scale(1.05);
}

.back-button .stButton button {
    background-color: #e94560;
    color: white;
    border: none;
    padding: 0.7em 1.2em;
    border-radius: 30px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.back-button .stButton button:hover {
    background-color: #c73851;
    transform: scale(1.05);
}

/* Add more custom styles here */

</style>
""", unsafe_allow_html=True)
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# st.markdown("<h1 class='animated-title'>MULTI-DIAGNOSE</h1>", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "Home"

def go_home():
    st.session_state.page = "Home"
    st.rerun()
def back_button():
    if st.button("← Back", key="back_button"):
        go_home()

# Check the current page
if st.session_state.page == "Home":
    st.markdown("<h1 class='animated-title'>MULTI-DIAGNOSE</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    # lottie_health = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_5njp3vgg.json")
    # st_lottie(lottie_health, height=300, key="health_animation")

    diseases = [
        {"name": "Heart Disease", "icon": "❤️", "function": heart_disease_prediction, "lottie": "https://lottie.host/7543377c-efca-4a7e-91fc-5e3427a24cae/IO5VpNGdRB.json"},
        {"name": "Diabetes", "icon": "💉", "function": diabetes_prediction, "lottie": "https://assets3.lottiefiles.com/packages/lf20_tbjuenb2.json"},
        {"name": "Lungs Cancer", "icon": "🫁", "function": lung_cancer_prediction, "lottie": "https://lottie.host/4d5b6e17-584a-4afc-9e9e-942a440fbd6d/pcy7LQ6rlf.json"},
        # {"name": "Breast Cancer", "icon": "🎗️","function": breast_cancer_prediction, "lottie": "https://lottie.host/d4ba7ac7-1bbe-4cb9-8600-9607ed1bef7c/iklzqmxnBc.json"},
        {"name": "Brain Tumor", "icon": "🧠", "function": brain_detection, "lottie": "https://lottie.host/b0ea85a7-6b8e-48e6-91cb-0e65866ca714/ZSoycEWOwo.json"},
        {"name": "Liver Disease", "icon": "🫧", "function": liver_disease_assessment, "lottie": "https://lottie.host/1418a8de-ef1f-4a7d-825d-9a883bcadfef/klvWeF175I.json"}
    ]

    for i, disease in enumerate(diseases):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"""
            <div class="disease-card">
                <h3>{disease['icon']} {disease['name']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            lottie_data = load_lottieurl(disease['lottie'])
            if lottie_data:
                st_lottie(lottie_data, height=150, key=f"lottie_{disease['name']}")
            else:
                st.warning(f"Failed to load animation for {disease['name']}")
            
            if st.button("Check Now", key=disease['name']):
                if 'function' in disease:
                    st.session_state.page = disease['name']
                    st.rerun()
                else:
                    st.write(f"Checking for {disease['name']}...")

elif st.session_state.page == "Heart Disease":
    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    back_button()
    st.markdown('</div>', unsafe_allow_html=True)
    heart_disease_prediction()
elif st.session_state.page == "Diabetes":

    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    back_button()
    st.markdown('</div>', unsafe_allow_html=True)
    diabetes_prediction()
elif st.session_state.page == "Lungs Cancer":

    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    back_button()
    st.markdown('</div>', unsafe_allow_html=True)
    lung_cancer_prediction()

elif st.session_state.page == "Brain Tumor":

    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    back_button()
    st.markdown('</div>', unsafe_allow_html=True)
    brain_detection()
elif st.session_state.page == "Liver Disease":

    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    back_button()
    st.markdown('</div>', unsafe_allow_html=True)
    liver_disease_assessment()
# elif st.session_state.page == "Breast Cancer":

#     st.markdown('<div class="back-button">', unsafe_allow_html=True)
#     back_button()
#     st.markdown('</div>', unsafe_allow_html=True)
#     breast_cancer_prediction()