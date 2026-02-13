import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import io

# 1. पेज सेटअप
st.set_page_config(page_title="Sreesa AI Assistant", page_icon="👩‍💻")
st.title("Sreesa AI Assistant 👩‍💻")

# 2. आपकी API Key (वही नई वाली)
API_KEY = "AIzaSyAb5f2VtEo9trR2tltGIQLBdMU8wPU8SvA"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # साइडबार विज़न
    with st.sidebar:
        st.header("Sreesa Vision")
        uploaded_file = st.file_uploader("फोटो अपलोड करें", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="आपकी फोटो", use_container_width=True)

    # 3. चैट मेमोरी
    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome = "नमस्ते! मैं श्रीसा हूँ। अब सारी कमियाँ दूर हो गई हैं। बताइए, मैं आपकी क्या मदद करूँ?"
        st.session_state.messages.append({"role": "assistant", "content": welcome})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. मुख्य चैट फंक्शन
    if prompt := st.chat_input("श्रीसा से बात करें..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # लोडिंग स्पिनर
                with st.spinner("श्रीसा सोच रही है..."):
                    if uploaded_file:
                        img = Image.open(uploaded_file)
                        response = model.generate_content([prompt, img])
                    else:
                        response = model.generate_content(prompt)
                
                res_text = response.text
                st.markdown(res_text)
                
                # आवाज़ फीचर
                tts = gTTS(text=res_text[:250], lang='hi')
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                st.audio(audio_buffer, format="audio/mp3")
                
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception:
                st.warning("जवाब लोड हो रहा है, कृपया एक बार फिर बटन दबाएं या पेज रिफ्रेश करें।")

except Exception:
    st.error("सेटअप लोड करने में दिक्कत हुई।")









  
