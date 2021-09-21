import streamlit as st
import speech_recognition as sr

def takecomand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        st.write("START SPEAKING!")
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
            st.write("You  said :",text)
        except:
            st.write("Please say again ...")
        return text
st.write("""
# SPEECH RECOGNITION USING DEEP LEARNING
This web-app detects speech and converts them into **Text**!
""")
if st.button("Click me"):
    takecomand()
