import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os

# पेज सेटअप
st.set_page_config(page_title="Sreesa AI Assistant", page_icon="👩‍💻")
st.title("Sreesa AI Assistant 👩‍💻")

# आपकी नई API Key
API_KEY = "AIzaSyAb5f2VtEo9trR2tltGIQLBdMU8wPU8SvA"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # साइडबार विज़न फीचर
    with st.sidebar:
        st.header("Sreesa Vision")
        uploaded_file = st.file_uploader("फोटो अपलोड करें", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="आपकी फोटो", use_container_width=True)

    # चैट मेमोरी
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "नमस्ते! मैं श्रीसा हूँ। अब मैं पूरी तरह तैयार हूँ। पूछिए, मैं आपकी क्या मदद करूँ?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("श्रीसा से बात करें..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([prompt, img])
                else:
                    response = model.generate_content(prompt)
                
                res_text = response.text
                st.markdown(res_text)
                
                # आवाज़ जनरेट करना
                tts = gTTS(text=res_text[:300], lang='hi')
                tts.save("s_voice.mp3")
                st.audio("s_voice.mp3")
                
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error("माफ़ कीजिये, कनेक्शन में अभी भी दिक्कत है। कृपया इंटरनेट चेक करें।")

except Exception as e:
    st.error("सेटअप अधूरा है।")








  
