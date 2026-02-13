import streamlit as st
import google.generativeai as genai

# ऐप का नाम और लुक
st.set_page_config(page_title="Sreesa AI", page_icon="👩‍💻")
st.title("Sreesa AI Assistant 👩‍💻")

# आपकी API Key
API_KEY = "AIzaSyAb5f2VtEo9trR2tltGIQLBdMU8wPU8SvA"

try:
    genai.configure(api_key=API_KEY)
    # यह मॉडल सबसे ज़्यादा स्थिर है
    model = genai.GenerativeModel('gemini-pro')

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "नमस्ते! मैं श्रीसा हूँ। नई शुरुआत के लिए तैयार? पूछिए, क्या मदद करूँ?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("श्रीसा से बात करें..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception:
                st.error("सर्वर लोड हो रहा है, कृपया 5 सेकंड बाद फिर से लिखें।")
except Exception:
    st.error("सेटअप में समस्या है।")
