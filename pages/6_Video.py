import streamlit as st
from moviepy.editor import *
import os
import whisper
import googletrans
from gtts import gTTS
from io import BytesIO

st.set_page_config(
    page_title="TranslaBuddy",
    page_icon="translate.png"
)

def main():
    st.header(":movie_camera: Video Transcriber and Translator")
    
    lang=googletrans.LANGUAGES
    len(lang)
    languag = st.selectbox("Target Language",lang.values())
    # File uploader
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov"])
    
    
    
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        st.markdown("""
    <style>
    video{
        width: 500px !important;
        height: 300px !important;
        margin-left: 100px
    }
    </style>
    """,unsafe_allow_html=True)
        # Create the "temp" directory if it doesn't exist
        if not os.path.exists("temp"):
            os.makedirs("temp")
        
        # Save the uploaded file to a temporary location
        with open(os.path.join("temp", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Read the uploaded video file
        video_clip = VideoFileClip(os.path.join("temp", uploaded_file.name))
        
        # Extract audio from the video
        audio_clip = video_clip.audio
        
        # Output filename
        output_filename = f"{uploaded_file.name.split('.')[0]}_audio.mp3"
        
        # Save the extracted audio
        audio_clip.write_audiofile(output_filename)
        # Display the extracted audio
        #st.audio(output_filename)
        
        video_clip.close()
        audio_clip.close()

        

        model = whisper.load_model("base")
        audio = whisper.load_audio(output_filename)
        audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
        _, probs = model.detect_language(mel)
        la= max(probs, key=probs.get)
        st.subheader(f"Detected language: {la}")
        result = model.transcribe(output_filename)
        texty=result["text"]
        st.subheader("Transcribed Text:")
        st.write(texty)
        #st.text_area("Transcribed Text:", texty, height=250)

        


        if st.button("Translate"):
            translator=googletrans.Translator()
            translation = translator.translate(texty,dest=languag)
            st.subheader("Translated Text:")
            user_output = st.text_area("",translation.text,height=300)
            if user_output:
                # Convert the text to speech
                selected_language_key = next(key for key, value in lang.items() if value == languag)
                tts = gTTS(text=user_output, lang=selected_language_key, slow=False)
                speech = BytesIO()
                tts.write_to_fp(speech)
                st.audio(speech, format="audio/wav")

if __name__ == "__main__":
    main()
