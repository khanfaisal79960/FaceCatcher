import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, VideoFrame
import av # Pythonic binding for FFmpeg

# Set up the Streamlit page
st.set_page_config(page_title="FaceCatcher - Real-time Face Detection", layout="centered")
st.title("FaceCatcher 👁️ Real-time Face Detection")
st.write("This app uses your webcam to detect faces in real-time using OpenCV's Haar Cascades.")
st.write("Please allow webcam access in your browser when prompted.")

# Load the Haar Cascade classifier for face detection
# This path points to the cascade file included with OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Check if the cascade classifier loaded successfully
if face_cascade.empty():
    st.error("Error: Could not load Haar Cascade XML file. This might indicate an issue with the OpenCV installation or path.")
    st.stop()

# Define a custom VideoProcessor class for real-time frame processing
class FaceDetectionProcessor(VideoProcessorBase):
    def __init__(self):
        # Initialize the cascade classifier once per processor instance
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if self.face_cascade.empty():
            st.error("Error: Could not load Haar Cascade XML file within the video processor.")
            # In a real app, you might want to raise an exception or handle this more gracefully
            # For now, we'll let it pass, but detection won't work.

    def recv(self, frame: VideoFrame) -> VideoFrame:
        # Convert the VideoFrame (from av) to a NumPy array (OpenCV format)
        img = frame.to_ndarray(format="bgr24")

        # Flip the image horizontally for a selfie-view display.
        img = cv2.flip(img, 1)

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        # scaleFactor: Parameter specifying how much the image size is reduced at each image scale.
        # minNeighbors: Parameter specifying how many neighbors each candidate rectangle should have to retain it.
        # minSize: Minimum possible object size. Objects smaller than that are ignored.
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2) # Blue rectangle, 2 pixels thick

        # Convert the processed NumPy array back to a VideoFrame
        return VideoFrame.from_ndarray(img, format="bgr24")

# Use webrtc_streamer to start the webcam feed and apply the processor
webrtc_ctx = webrtc_streamer(
    key="face-detection",
    video_processor_factory=FaceDetectionProcessor,
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True, # Process frames asynchronously
)

if webrtc_ctx.state.playing:
    st.success("Webcam stream started. Looking for faces...")
else:
    st.info("Click 'Start' to begin face detection.")