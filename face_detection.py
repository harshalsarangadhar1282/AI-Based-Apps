import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def detect_faces(self, image: np.ndarray):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        result_image = image.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(result_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return result_image, len(faces)

def initialize_session_state():
    if 'detector' not in st.session_state:
        st.session_state.detector = FaceDetector()
    if 'theme' not in st.session_state:
        st.session_state.theme = 'Light'
    if 'processed_image' not in st.session_state:
        st.session_state.processed_image = None
    if 'faces_detected' not in st.session_state:
        st.session_state.faces_detected = 0

def apply_theme(theme: str):
    if theme == 'Dark':
        st.markdown("""
            <style>.main { background-color: #0E1117; color: #FAFAFA; }</style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>.main { background-color: #FFFFFF; color: #31333F; }</style>
        """, unsafe_allow_html=True)

def main():
    initialize_session_state()
    apply_theme(st.session_state.theme)
    
    st.title("Face Recognition AI 👤")
    st.markdown("Upload an image or use webcam to detect faces")
    
    with st.sidebar:
        st.header("⚙️ Settings")
        st.session_state.theme = st.radio("Theme:", ['Light', 'Dark'])
    
    option = st.radio("Choose input method:", ["Upload Image", "Webcam"])
    
    if option == "Upload Image":
        uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])
        if uploaded_file:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            processed_image, num_faces = st.session_state.detector.detect_faces(image)
            
            col1, col2 = st.columns(2)
            with col1:
                st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Original Image")
            with col2:
                st.image(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB), caption=f"Detected {num_faces} faces")
            
            if st.button("Save Processed Image"):
                cv2.imwrite("processed_image.jpg", processed_image)
                st.success("Image saved as processed_image.jpg")
    
    else:
        st.warning("Webcam feature requires additional setup")
        st.info("For webcam functionality, please check the full version with OpenCV video capture")

if __name__ == "__main__":
    main()