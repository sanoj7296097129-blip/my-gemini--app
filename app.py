import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. पेज और पर्सनालिटी सेटअप
st.set_page_config(page_title="Sreesa AI Assistant", page_icon="👩‍💻")
st.title("Sreesa AI Assistant 👩‍💻")

# आपकी API Key
API_KEY = "AIzaSyAb5f2VtEo9trR2tltGIQLBdMU8wPU8SvA"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. साइडबार में 'About' और 'Video' फीचर
with st.sidebar:
    st.title("Sreesa Smart Features")
    st.info("नमस्ते! मैं आपकी स्मार्ट असिस्टेंट श्रीसा हूँ। मैं फोटो देख सकती हूँ और आपके लिए वीडियो भी बना सकती हूँ।")
    
    st.subheader("Video Generator 🎬")
    video_prompt = st.text_input("किस बारे में वीडियो बनाना है?")
    if st.button("Generate Video"):
        st.warning("Video generation feature is being linked to Veo model. Coming soon!")

# 3. चैट फंक्शन
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "नमस्ते मालिक! आपकी श्रीसा हाजिर है। आज हम क्या नया करेंगे?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("श्रीसा से बात करें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # बिना देरी के जवाब देने के लिए सीधा कनेक्शन
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception:
            st.error("माफ़ कीजिये, कनेक्शन अभी भी बन रहा है। कृपया Reboot बटन दबाएं।")
