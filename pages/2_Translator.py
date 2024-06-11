import streamlit as st
import googletrans
from gtts import gTTS
from io import BytesIO

st.set_page_config(
    page_title="TranslaBuddy",
    page_icon="translate.png",
) 

st.header(":pencil2: Translator and Interpreter")
lang=googletrans.LANGUAGES
user_input = st.text_input("Enter text:")
language = st.selectbox("Target Language",lang.values())



if st.button("Translate"):
    translator=googletrans.Translator()
    translation = translator.translate(user_input,dest=language)
    user_output = st.text_area("target",translation.text)
    if user_output:
        # Convert the text to speech
        selected_language_key = next(key for key, value in lang.items() if value == language)
        tts = gTTS(text=user_output, lang=selected_language_key, tld="co.in", slow=False)
        speech = BytesIO()
        tts.write_to_fp(speech)
        st.audio(speech, format="audio/wav")