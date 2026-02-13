import streamlit as st
import google.generativeai as genai

# पेज सेटअप
st.set_page_config(page_title="Sreesa AI Assistant", page_icon="👩‍💻")
st.title("Sreesa AI Assistant 👩‍💻")

# आपकी API Key
API_KEY = "AIzaSyAb5f2VtEo9trR2tltGIQLBdMU8wPU8SvA"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# साइडबार
with st.sidebar:
    st.title("Sreesa Settings")
    st.info("नमस्ते! मैं श्रीसा हूँ। आपकी पर्सनल AI असिस्टेंट।")
    if st.button("Reboot Sreesa"):
        st.rerun()

# चैट मेमोरी
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "नमस्ते! अब सब कुछ ठीक हो गया है। पूछिए, मैं आपकी क्या मदद करूँ?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("श्रीसा से बात करें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # बिना किसी देरी के जवाब
            response = model.generate_content(prompt)
            res_text = response.text
            st.markdown(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
        except Exception as e:
            st.error("Google Server से कनेक्शन नहीं हो पाया। कृपया अपनी API Key चेक करें या 10 सेकंड बाद फिर कोशिश करें।")

