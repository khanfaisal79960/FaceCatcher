import streamlit as st
import cv2
import numpy as np

# Set up the Streamlit page
st.set_page_config(page_title="FaceCatcher - Real-time Face Detection", layout="centered")
st.title("FaceCatcher 👁️ Real-time Face Detection")
st.write("This app uses your webcam to detect faces in real-time using OpenCV's Haar Cascades.")

# Placeholder for the video feed
frame_placeholder = st.empty()

# Load the Haar Cascade classifier for face detection
# You need to have 'haarcascade_frontalface_default.xml' in the same directory as this script,
# or provide the full path to it.
# You can download it from: https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Check if the cascade classifier loaded successfully
if face_cascade.empty():
    st.error("Error: Could not load Haar Cascade XML file. Make sure 'haarcascade_frontalface_default.xml' is in the correct path.")
    st.stop()

# Start webcam capture
cap = cv2.VideoCapture(0) # 0 for default webcam

# Check if webcam is opened successfully
if not cap.isOpened():
    st.error("Error: Could not open webcam. Please ensure it's connected and not in use by another application.")
    st.stop()

# Add a stop button
stop_button = st.button("Stop Detection")

# Loop to read frames and perform face detection
while cap.isOpened() and not stop_button:
    ret, frame = cap.read()
    if not ret:
        st.warning("Failed to grab frame from webcam. Exiting...")
        break

    # Flip the image horizontally for a selfie-view display.
    frame = cv2.flip(frame, 1)

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    # scaleFactor: Parameter specifying how much the image size is reduced at each image scale.
    # minNeighbors: Parameter specifying how many neighbors each candidate rectangle should have to retain it.
    # minSize: Minimum possible object size. Objects smaller than that are ignored.
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2) # Blue rectangle, 2 pixels thick

    # Convert the frame back to RGB for Streamlit display
    # (Streamlit expects RGB, OpenCV reads BGR)
    display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the processed frame in the placeholder
    # Changed use_column_width to use_container_width to remove deprecation warning
    frame_placeholder.image(display_frame, channels="RGB", use_container_width=True)

    # Check for stop button press (this is handled by Streamlit's rerun mechanism)
    if stop_button:
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()

st.success("Webcam stream stopped.")
