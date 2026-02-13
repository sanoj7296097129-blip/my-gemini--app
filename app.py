import streamlit as st
import google.generativeai as genai

# ऐप का नाम
st.title("Sreesa AI Assistant")

# API Key को सुरक्षित तरीके से उठाना
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # सही मॉडल का नाम (gemini-1.5-flash)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # चैट की याददाश्त (Memory) के लिए
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # पुरानी बातचीत दिखाना
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # यूजर का सवाल लेना
    if prompt := st.chat_input("नमस्ते! मैं श्रीसा हूँ। मैं आपकी क्या मदद कर सकती हूँ?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI का जवाब जनरेट करना
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error("कृपया ऐप की 'Secrets' सेटिंग्स में अपनी नई 'GEMINI_API_KEY' अपडेट करें।")

  
