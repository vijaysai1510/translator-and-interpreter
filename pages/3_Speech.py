import streamlit as st
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import wave
import googletrans
from gtts import gTTS
from io import BytesIO
import base64

st.set_page_config(
    page_title="TranslaBuddy",
    page_icon="translate.png"
) 

st.header(":microphone: Live Translator") 

langu=googletrans.LANGUAGES
langus = st.selectbox("Your Language",langu.values()) 
def main():
    
                                                     
    lang=googletrans.LANGUAGES
    language = st.selectbox("Target Language",lang.values())
    if st.button("Start Recording"):
        st.success("Recording...")

        # Record audio for 5 seconds (you can change the duration as needed)
        audio_data, sample_rate = record_audio(duration=5)

        # Save the recorded audio as a WAV file
        wav_filename = "recorded_audio.wav"
        save_audio_as_wav(audio_data, sample_rate, wav_filename)

        # Display the recorded audio
        #st.audio(wav_filename, format="audio/wav", start_time=0, sample_rate=sample_rate)

        # Convert audio to text
        texty = convert_audio_to_text(wav_filename)

        # Display the converted text
        st.subheader("Recorded Text:")
        st.text(texty)

        translator=googletrans.Translator()
        translation = translator.translate(texty,dest=language)
        st.subheader("Translated Text:")
        user_output = st.text_area("",translation.text)

        st.subheader("Translated Audio:")
        if user_output:
            # Convert the text to speech
            selected_language_key = next(key for key, value in lang.items() if value == language)
            tts = gTTS(text=user_output, lang=selected_language_key, slow=False)
            speech = BytesIO()
            tts.write_to_fp(speech)
            encoded_speech = base64.b64encode(speech.getvalue()).decode('utf-8')

            # Display the audio player using st.markdown
            st.markdown(f'<audio controls autoplay><source src="data:audio/wav;base64,{encoded_speech}" type="audio/wav" ></audio>', unsafe_allow_html=True)
    
            # Embed JavaScript for autoplay
            st.markdown(
                        """
                        <script>
                        const audio = document.querySelector("audio");
                        audio.autoplay = true;
                        </script>
                        """,
                        unsafe_allow_html=True
                    )

def record_audio(duration=5, sr=44100):
    # Record audio for the specified duration
    audio_data = sd.rec(int(duration * sr), samplerate=sr, channels=2, dtype=np.int16)
    sd.wait()
    return audio_data.flatten(), sr


def save_audio_as_wav(audio_data, sample_rate, filename):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

def convert_audio_to_text(wav_filename):
    for key, value in langu.items():
        if value == langus:
            lang = key
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(wav_filename) as source:
            audio = recognizer.record(source)
            texty = recognizer.recognize_google(audio,language=lang, show_all = True)
            transcript = texty['alternative'][0]['transcript']
            return transcript
    except sr.UnknownValueError as e:
        st.error(f"Speech Recognition could not understand audio: {e}")
        return "Unknown Value Error"
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return f"Request Error: {e}"

if __name__ == "__main__":
    main()
