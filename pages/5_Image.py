import streamlit as st
import os
import googletrans
from gtts import gTTS
from io import BytesIO
import cv2
import easyocr
import numpy as np

st.set_page_config(
    page_title="TranslaBuddy",
    page_icon="translate.png"
)

def main():
    st.header(":camera: Image Translator")

    
    lang = googletrans.LANGUAGES

    langu= st.selectbox("Language of image", lang.values())
    
    language = st.selectbox("Target Language", lang.values())
    # File uploader
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", width=300)

        # Convert the uploaded image to bytes
        image_bytes = uploaded_image.read()

        # Convert the bytes to a numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        selected_language_key_0 = next(key for key, value in lang.items() if value == langu)

        reader = easyocr.Reader([selected_language_key_0], gpu=False)

        text_ = reader.readtext(img)

        threshold = 0.25

        # Accumulate text into a single paragraph
        paragraph = ""
        st.subheader("Extracted Text:")
        for t in text_:
            bbox, text, score = t
            paragraph += text + " "

        # Display the paragraph
        st.write(paragraph)

        if st.button("Translate"):
            translator=googletrans.Translator()
            translation = translator.translate(paragraph,dest=language)
            st.subheader("Translated Text:")
            user_output = translation.text
            st.write(translation.text)
            if user_output:
                # Convert the text to speech
                selected_language_key = next(key for key, value in lang.items() if value == language)
                tts = gTTS(text=user_output, lang=selected_language_key, slow=False)
                speech = BytesIO()
                tts.write_to_fp(speech)
                st.audio(speech, format="audio/wav")

if __name__ == "__main__":
    main()
