import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import io

# 1. पेज की सेटिंग्स
st.set_page_config(page_title="Sreesa AI Assistant", page_icon="👩‍💻")
st.title("Sreesa AI Assistant 👩‍💻")

# 2. आपकी सबसे नई API Key (जो आपने अभी AI Studio से ली है)
# नीचे वाली लाइन में अपनी Key को " " के बीच में लिखें
API_KEY = "AIzaSyAb5f2VtEo9trR2tltGIQLBdMU8wPU8SvA"

try:
    genai.configure(api_key=API_KEY)
    # सबसे मज़बूत मॉडल का चुनाव
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 3. साइडबार में फोटो अपलोड फीचर (Vision)
    with st.sidebar:
        st.header("Sreesa Vision")
        uploaded_file = st.file_uploader("कोई भी फोटो अपलोड करें", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="आपकी फोटो", use_container_width=True)

    # 4. चैट की याददाश्त (Memory)
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # प्यारा सा स्वागत संदेश
        welcome = "नमस्ते! मैं श्रीसा हूँ। अब मेरी सारी कमियाँ दूर हो गई हैं। मैं फोटो देख सकती हूँ और बोल भी सकती हूँ। बताइए, आज मैं आपकी क्या मदद करूँ?"
        st.session_state.messages.append({"role": "assistant", "content": welcome})

    # पुरानी बातचीत दिखाना
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. यूजर से सवाल पूछना
    if prompt := st.chat_input("श्रीसा से कुछ भी पूछें..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # जवाब जनरेट करना (फोटो के साथ या बिना फोटो के)
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([prompt, img])
                else:
                    response = model.generate_content(prompt)
                
                res_text = response.text
                st.markdown(res_text)
                
                # 6. आवाज़ (Voice) जनरेट करना
                tts = gTTS(text=res_text[:300], lang='hi')
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                st.audio(audio_buffer, format="audio/mp3")
                
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error("माफ़ कीजिये, जवाब देने में थोड़ी देरी हो रही है। कृपया अपनी इंटरनेट स्पीड चेक करें।")

except Exception as e:
    st.error("सेटअप अधूरा है। कृपया GitHub पर अपनी API Key दोबारा चेक करें।")









  
