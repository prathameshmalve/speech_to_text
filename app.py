import streamlit as st
import os
from speech_to_text import speech_to_text  # Importing the function from the other file

# Streamlit Web App
st.title("Speech-to-Text Transcription")

# Upload audio file
uploaded_file = st.file_uploader("Upload a .wav file", type="wav")

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("uploaded_audio.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write("File uploaded successfully!")

    # Run speech-to-text on the uploaded file
    transcribed_text = speech_to_text("uploaded_audio.wav")

    # Display the transcription
    if transcribed_text:
        st.write("Transcription complete:")
        st.text_area("Transcribed Text", value=transcribed_text, height=300)

    # Clean up the temporary files
    os.remove("uploaded_audio.wav")
    
    # Remove specific temporary files if they exist
    temp_files = ["output_audio_file1.wav", "temp_reduced_noise.wav"]
    for file_name in temp_files:
        if os.path.exists(file_name):
            os.remove(file_name)

    # Remove chunk files dynamically
    i = 0
    while os.path.exists(f"chunk{i}.wav"):
        os.remove(f"chunk{i}.wav")
        i += 1
