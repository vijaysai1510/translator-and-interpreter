import PyPDF2
from docx import Document
import os
import streamlit as st
import googletrans
from gtts import gTTS
from io import BytesIO

st.set_page_config(
    page_title="TranslaBuddy",
    page_icon="translate.png"
)
st.header(":memo: Document Translation")

def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        text += add_spaces_to_text(page_text)
    return text

def add_spaces_to_text(text):
    new_text = ""
    for char in text:
        if char.isalnum() or char.isspace():
            new_text += char
        else:
            new_text += " " + char + " "
    return new_text
def extract_text_from_docx(uploaded_file):
    text = ""
    doc = Document(uploaded_file)
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(uploaded_file):
    text = uploaded_file.getvalue().decode("utf-8")
    return text

def main():
    
    uploaded_file = st.file_uploader("Upload a file", type=['pdf', 'docx', 'txt'])
    lang=googletrans.LANGUAGES
    language = st.selectbox("Target Language",lang.values())
    if st.button("Extract and Translate"):
        if uploaded_file is not None:
            if uploaded_file.type == 'application/pdf':
                text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                text = extract_text_from_docx(uploaded_file)
            elif uploaded_file.type == 'text/plain':
                text = extract_text_from_txt(uploaded_file)
            else:
                st.error("Unsupported file format")
                return
        
        st.write("Extracted text:")
        st.text(text)
        
        translator=googletrans.Translator()
        translation = translator.translate(text,dest=language)
        user_output = st.text_area("Translated Text",translation.text,height=250)
        if user_output:
            #Convert the text to speech
            selected_language_key = next(key for key, value in lang.items() if value == language)
            tts = gTTS(text=user_output, lang=selected_language_key, slow=False)
            speech = BytesIO()
            tts.write_to_fp(speech)
            st.audio(speech, format="audio/wav")

if __name__ == "__main__":
    main()
