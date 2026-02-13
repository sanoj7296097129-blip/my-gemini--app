
import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os

st.set_page_config(page_title="Sreesa AI Assistant")
st.title("Sreesa Smart AI (Voice & Vision)")

# API Key सेटअप
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 1. इमेज अपलोड करने का फीचर
    uploaded_file = st.sidebar.file_uploader("फोटो अपलोड करें", type=["jpg", "jpeg", "png"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("मुझसे बात करें या फोटो के बारे में पूछें:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # अगर फोटो अपलोड है, तो उसे AI को भेजें
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content(prompt)
            
            res_text = response.text
            st.markdown(res_text)

            # 2. आवाज़ (Voice) का फीचर
            tts = gTTS(text=res_text, lang='hi')
            tts.save("response.mp3")
            st.audio("response.mp3", format="audio/mp3")
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})

except Exception as e:
    st.error("सेटअप में कुछ कमी है। कृपया अपनी 'Secrets' चेक करें।")

  
