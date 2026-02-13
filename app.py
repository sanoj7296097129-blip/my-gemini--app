import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os

# ऐप की सेटिंग्स और टाइटल
st.set_page_config(page_title="Sreesa AI Assistant", page_icon="👩‍💻")
st.title("Sreesa AI Assistant 👩‍💻")

# API Key सेटअप
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # साइडबार में फोटो अपलोड का विकल्प
    with st.sidebar:
        st.header("Sreesa Vision")
        uploaded_file = st.file_uploader("कोई भी फोटो अपलोड करें", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.image(uploaded_file, caption="अपलोड की गई फोटो", use_container_width=True)

    # चैट हिस्ट्री (Memory)
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # पहला स्वागत संदेश (Welcome Message)
        welcome_text = "नमस्ते! मेरा नाम श्रीसा है। मैं आपकी अपनी AI असिस्टेंट हूँ। मैं फोटो देख सकती हूँ और आपसे बात भी कर सकती हूँ। बताइए, आज मैं आपकी क्या मदद करूँ?"
        st.session_state.messages.append({"role": "assistant", "content": welcome_text})

    # मैसेज दिखाना
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # यूजर का इनपुट
    if prompt := st.chat_input("श्रीसा से कुछ भी पूछें..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # फोटो के साथ या बिना फोटो के जवाब देना
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content(prompt)
            
            res_text = response.text
            st.markdown(res_text)

            # आवाज़ (Voice) जनरेट करना
            try:
                tts = gTTS(text=res_text, lang='hi')
                tts.save("sreesa_voice.mp3")
                st.audio("sreesa_voice.mp3", format="audio/mp3")
            except:
                st.warning("आवाज़ अभी लोड नहीं हो पाई।")
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})

except Exception as e:
    st.error("सेटअप में गड़बड़ है। कृपया 'Secrets' में API Key चेक करें।")


  
