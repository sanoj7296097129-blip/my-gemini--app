import streamlit as st
import google.generativeai as genai

# ऐप का टाइटल
st.title("My Gemini AI Assistant")

# Streamlit Secrets से API Key लेना (सुरक्षा के लिए)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')

    # यूजर इनपुट
    user_input = st.text_input("मुझसे कुछ भी पूछें:")

    if user_input:
        with st.spinner('सोच रहा हूँ...'):
            response = model.generate_content(user_input)
            st.write(response.text)
else:
    st.error("कृपया Streamlit की सेटिंग्स में अपनी 'GEMINI_API_KEY' जोड़ें।")
  
