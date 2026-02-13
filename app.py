import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os

# 1. पेज सेटअप
st.set_page_config(page_title="Sreesa AI Assistant", page_icon="👩‍💻")
st.title("Sreesa AI Assistant 👩‍💻")

# 2. API Key सेटअप (सीधा कोड में ताकि कोई एरर न आए)
API_KEY = "AIzaSyC4KOEKxXaEmNoTQrvx0H_yCJmE2xTU-Ck"
genai.configure(api_key=API_KEY)

# 3. सही मॉडल का नाम (404 एरर को ठीक करने के लिए)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. साइडबार में इमेज अपलोड का फीचर
with st.sidebar:
    st.header("Sreesa Vision")
    uploaded_file = st.file_uploader("कोई भी फोटो अपलोड करें", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="आपकी फोटो", use_container_width=True)

# 5. चैट मेमोरी और स्वागत संदेश
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_text = "नमस्ते! मैं श्रीसा हूँ। आपकी सभी समस्याएँ अब ठीक हो गई हैं। मैं अब फोटो देख सकती हूँ और आपसे बात भी कर सकती हूँ। बताइए, मैं आपकी क्या मदद करूँ?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_text})

# पुरानी बातचीत दिखाना
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. यूजर इनपुट और जवाब (Vision + Voice)
if prompt := st.chat_input("श्रीसा से बात करें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # अगर फोटो है तो उसे AI को भेजें
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content(prompt)
            
            res_text = response.text
            st.markdown(res_text)

            # आवाज़ (Voice) जनरेट करना
            tts = gTTS(text=res_text, lang='hi')
            tts.save("sreesa_voice.mp3")
            st.audio("sreesa_voice.mp3", format="audio/mp3")
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})
        except Exception as e:
            st.error(f"क्षमा करें, जवाब देने में दिक्कत हो रही है। कृपया सुनिश्चित करें कि आपकी इंटरनेट स्पीड सही है।")






  
