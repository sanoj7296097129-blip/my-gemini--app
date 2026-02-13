import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os

# 1. पेज सेटअप
st.set_page_config(page_title="Sreesa AI Assistant", page_icon="👩‍💻")
st.title("Sreesa AI Assistant 👩‍💻")

# 2. API Key सेटअप
API_KEY = "AIzaSyC4KOEKxXaEmNoTQrvx0H_yCJmE2xTU-Ck"
genai.configure(api_key=API_KEY)

# 3. सबसे स्थिर मॉडल का नाम
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. साइडबार में फोटो फीचर
with st.sidebar:
    st.header("Sreesa Vision")
    uploaded_file = st.file_uploader("कोई भी फोटो अपलोड करें", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="आपकी फोटो", use_container_width=True)

# 5. चैट मेमोरी
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_text = "नमस्ते! मैं श्रीसा हूँ। अब मैं फोटो देख सकती हूँ और आपसे बात भी कर सकती हूँ। बताइए, आज मैं आपकी क्या मदद करूँ?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_text})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. मुख्य चैट फंक्शन
if prompt := st.chat_input("श्रीसा से बात करें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # विज़न और टेक्स्ट का सही तालमेल
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content(prompt)
            
            res_text = response.text
            st.markdown(res_text)

            # आवाज़ फीचर (Errors से बचने के लिए)
            try:
                tts = gTTS(text=res_text, lang='hi')
                tts.save("sreesa_voice.mp3")
                st.audio("sreesa_voice.mp3", format="audio/mp3")
            except:
                pass
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})
        except Exception as e:
            st.error("माफ़ कीजिये, इस समय कनेक्शन में दिक्कत है। कृपया एक बार पेज रिफ्रेश करें।")







  
