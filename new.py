import streamlit as st
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
import requests
import json
import streamlit_shadcn_ui as ui
from streamlit_lottie import st_lottie
import tensorflow as tf
from PIL import Image
import numpy as np
from streamlit_option_menu import option_menu
from streamlit_card import card
import os
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
model1= tf.keras.models.load_model('CNN_Model_1.keras')
# model2= tf.keras.models.load_model('pneumonia_model.keras')
def func2():
    def resize_image(image, target_size=(299, 299)):
        resized_image = image.resize(target_size)
        return resized_image

    def preprocess_image(image):
        # Check if the image has a channel dimension
        if len(image.shape) == 3:
            # Color image, ensure channel dimension is 3
            if image.shape[-1] == 3:
                return image
            else:
                # Convert to RGB
                return np.stack((image,) * 3, axis=-1)
        elif len(image.shape) == 2:
            # Grayscale image, add channel dimension of size 3
            return np.stack((image,) * 3, axis=-1)
        else:
            raise ValueError("Invalid image shape")
    with st.sidebar:
        selected= option_menu(f"welcome in..",["MRI-Diagnosis", "Pneumonia-Diagnosis"], 
                                        icons=["upc scan", "lungs-fill"], default_index=0,
                                        menu_icon="person-square")
    if selected=="MRI-Diagnosis":
        def load_lottieurl(url: str):
            r= requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        lottie_hello=load_lottieurl("https://lottie.host/bad0bdac-fa82-477a-8b75-1a41bdb74917/seP3AisUH3.json")
        def mrii(*texts):
            css = """
            @import url('https://fonts.googleapis.com/css2?family=Jersey+20&family=Pixelify+Sans:wght@400..700&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Jersey+20&family=Jost:ital,wght@0,100..900;1,100..900&family=Pixelify+Sans:wght@400..700&display=swap');
            .mri_typewriter {
              overflow: hidden;
              border-right: .15em solid transparent; 
              white-space: nowrap; 
              margin: 0 auto; 
              letter-spacing: .15em; 
              margin-left: 15%; /* Adjust as needed */
              font-size: 40px; 
              font-family: "Jersey 20", sans-serif;
              font-weight: 400;
              font-style: normal;
            }
            .diagnosis_fonnt{
             font-family: "Jost", sans-serif;
             font-optical-sizing: auto;
             font-size: 20px;
             font-weight: 700;
             font-style: italic;
             font-variation-settings:
             "slnt" 0,
             "CASL" 0,
             "CRSV" 0.5,
             "MONO" 0;
             align-text:center; 
            }
            """
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
            for text in texts:
                st.markdown(f"<div class='mri_typewriter'>{text}</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            mrii("MRI Scan Diagnosis")
            mrii("<div><p class='diagnosis_fonnt'>You have to provide the picture of</p><p class='diagnosis_fonnt'>MRI report and the Machine learning </p><p class='diagnosis_fonnt'>model would help ypu to diagnose.</p><p class='diagnosis_fonnt'>Once Model is done with diagnosis,</p><p class='diagnosis_fonnt'>it would provide you with the issues</p><p class='diagnosis_fonnt'>and its respective treatments.</p></div>")
        with col2:
            st_lottie(
                lottie_hello,
                speed=1,
                reverse= False,
                loop=True,
                quality= "medium",
                height=430,
                width=700,
            )
        st.markdown(f"<div class='mri_typewriter', style='margin-left:0px;font-size: 35px; '>Enter the image here!!</div>", unsafe_allow_html=True)
        st.markdown('<div style="color:red; font-size: 13px">**Note: Our machine learning predictions are not a substitute for professional medical advice; consult a doctor for accurate diagnosis. Use our platform for educational purposes and as a secondary opinion only.</div>', unsafe_allow_html=True)
        dict_final = {0: 'Glioma Brain Tumour', 1: 'Meningioma Brain Tumour', 2: 'No Brain Tumour', 3: 'Pitutary Brain Tumour'}
        uploaded_file = st.file_uploader("abc", type=["jpg", "jpeg"], label_visibility="hidden")
        if uploaded_file is not None:
            # Display the uploaded image
            original_image = Image.open(uploaded_file)
            colA,colB= st.columns(2)
            with  colA:
                st.image(original_image, caption='The original image', use_column_width=False)
            # Resize the image to (299, 299)
            with colB:
                resized_img = resize_image(original_image, target_size=(299, 299))
                img = np.asarray(resized_img)
                #Preprocess the image to ensure consistent shape
                img = preprocess_image(img)
                img = np.expand_dims(img, axis=0)
                #st.write(img)
                #st.write(np.array(img.shape))
                img = img / 255
                st.write("Resizing the image")
                st.image(resized_img, caption='The image after resizing', use_column_width=False)
            predictions = model1.predict(img)
            #print(predictions)
            anss=predictions[0].argmax()
            mri_answer=dict_final[anss]
            colx,coly,colz= st.columns([2.4,2,1.3])
            colD,colE,colF= st.columns(3)
            col1,col2=st.columns(2)
            with coly:
                button2=ui.button("Analyse the MRI report!!",key="abc",className="bg-orange-500 text-white",)
                if button2:
                    if anss==2:
                        with colE:
                            card(
                                title="The Report says:",
                                text="You have No Brain Tumour!!",
                                image="https://htmlcolorcodes.com/assets/images/colors/bright-green-color-solid-background-1920x1080.png",
                                key="card1"
                                )
                    else:
                        with col1:
                            card(
                                title="The Report says:",
                                text=(f"You have {mri_answer}"),
                                image="https://media.sciencephoto.com/f0/20/53/73/f0205373-800px-wm.jpg",
                                key="card1"
                                )       
                        with col2:  
                            card(
                                title=(f"Treatment steps are:"),
                                text=(f"Consult the Oncologist asap or try the Diagno bot assitance for an opinion"),
                                image="https://recovertogether.withgoogle.com/static/images/treatment/hero.jpg",
                                key="card2"
                            )
                            

def main():
    func2()

if __name__ == "__main__":
    main()