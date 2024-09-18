import speech_recognition as sr
import noisereduce as nr
import numpy as np
from pydub import AudioSegment
from scipy.io import wavfile
import os

# Function to convert audio file to text
def speech_to_text(audio_path):
    recognizer = sr.Recognizer()

    # Load the audio file and reduce noise
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_channels(1)
    audio.export("output_audio_file1.wav", format="wav")

    rate, data = wavfile.read("output_audio_file1.wav")
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write("temp_reduced_noise.wav", rate, reduced_noise.astype(np.int16))

    # Split audio into chunks and process each chunk
    audio = AudioSegment.from_wav("temp_reduced_noise.wav")
    chunk_length_ms = 30000  # 30 seconds per chunk
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    full_text = ""
    for i, chunk in enumerate(chunks):
        chunk.export(f"chunk{i}.wav", format="wav")
        with sr.AudioFile(f"chunk{i}.wav") as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                full_text += text + " "
            except sr.UnknownValueError:
                print(f"Chunk {i+1} could not be understood.")
            except sr.RequestError as e:
                print(f"API request failed for chunk {i+1}; {e}")

    return full_text
