import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image

import numpy as np
import os
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
def brain_detection():
# Load your trained model
    model = tf.keras.models.load_model('tumor\CNN_Model_1.keras')

    # Define class names
    class_names = ['glioma_tumor', 'meningioma_tumor', 'no_tumor', 'pituitary_tumor']

    def predict_image(img_path):
        img = Image.open(img_path)
        img = img.resize((299, 299))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        predicted_probability = predictions[0][predicted_class]
        
        return class_names[predicted_class], predictions[0], predicted_probability

    st.title('Brain Tumor Classification')

    uploaded_file = st.file_uploader("Choose a brain MRI image...", type="jpg")

    if uploaded_file is not None:
        try:
            # Create tempDir if it doesn't exist
            if not os.path.exists("tempDir"):
                os.makedirs("tempDir")
            
            temp_file_path = os.path.join("tempDir", uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Display the uploaded image
            st.image(uploaded_file, caption='Uploaded MRI Image.',width=350)
            
            # Make prediction
            class_name, probabilities,prob = predict_image(temp_file_path)
            
            # Display prediction results
            st.write(f"Prediction: {class_name}")
            st.write(f"prob: {prob}")
            st.write(f"Confidence: {probabilities[class_names.index(class_name)]:.2f}")
            
            # Create and display bar chart
            fig = px.bar(x=probabilities, y=class_names, orientation='h')
            fig.update_layout(title='Prediction Probabilities',
                            xaxis_title='Probability',
                            yaxis_title='Class')
            st.plotly_chart(fig)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        
        finally:
            # Clean up temporary file
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                os.remove(temp_file_path)