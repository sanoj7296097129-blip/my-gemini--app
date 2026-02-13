import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import io

# ऐप की सेटिंग्स
st.set_page_config(page_title="Sreesa AI Assistant", page_icon="👩‍💻")
st.title("Sreesa AI Assistant 👩‍💻")

# आपकी सबसे नई API Key
API_KEY = "AIzaSyC4KOEKxXaEmNoTQrvx0H_yCJmE2xTU-Ck"
genai.configure(api_key=API_KEY)

# मॉडल का सबसे स्टेबल नाम (बिना 'models/' के)
model = genai.GenerativeModel('gemini-1.5-flash')

# साइडबार में विज़न फीचर
with st.sidebar:
    st.header("Sreesa Vision")
    uploaded_file = st.file_uploader("फोटो अपलोड करें", type=["jpg", "jpeg", "png"])

# चैट मेमोरी
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_text = "नमस्ते! मैं श्रीसा हूँ। अब मैं जवाब देने के लिए बिल्कुल तैयार हूँ। बताइए, मैं आपकी क्या मदद करूँ?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_text})

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

            # आवाज़ (Voice) जनरेट करना
            tts = gTTS(text=res_text, lang='hi')
            tts.save("sreesa_voice.mp3")
            st.audio("sreesa_voice.mp3", format="audio/mp3")
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})
        except Exception as e:
            st.error(f"क्षमा करें, जवाब देने में दिक्कत हुई। एरर: {e}")





  
