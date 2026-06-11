import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import tempfile

# --- Page Config ---
st.set_page_config(
    page_title="Language Translation Tool",
    layout="centered"
)

# --- Styling ---
st.markdown("""
    <style>
    .codealpha-logo {
        position: fixed;
        top: 10px;
        right: 10px;
        font-size: 14px;
        color: #888;
        font-weight: bold;
        background: rgba(255,255,255,0.8);
        padding: 5px 10px;
        border-radius: 5px;
    }
    .main-title {
        text-align: center;
        color: #1E88E5;
    }
    </style>
    <div class="codealpha-logo">CodeAlpha Internship</div>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 class='main-title'>Language Translation Tool</h1>", unsafe_allow_html=True)
st.markdown("### Fast & Simple Translator with Speech Support")

# --- Language List ---
LANGUAGES = {
    "English": "en",
    "Urdu": "ur",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Hindi": "hi",
    "Arabic": "ar"
}

# --- UI ---
col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("Source Language", ["Auto"] + list(LANGUAGES.keys()))

with col2:
    target_lang = st.selectbox("Target Language", list(LANGUAGES.keys()), index=0)

text = st.text_area("Enter text")

# --- Translate ---
if st.button("Translate"):
    if text.strip() == "":
        st.warning("Please enter text")
    else:
        try:
            src = "auto" if source_lang == "Auto" else LANGUAGES[source_lang]
            dest = LANGUAGES[target_lang]

            translated = GoogleTranslator(
                source=src,
                target=dest
            ).translate(text)

            st.success("Translation Complete")
            st.code(translated)

            # --- TTS ---
            try:
                tts = gTTS(text=translated, lang=dest)

                # Use a temp file so it works on Streamlit Cloud (read-only filesystem)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    tmp_path = tmp_file.name

                tts.save(tmp_path)

                with open(tmp_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()

                st.audio(audio_bytes, format="audio/mp3")
                os.remove(tmp_path)

            except Exception as tts_error:
                st.warning(f"Text-to-Speech not available for this language. ({tts_error})")

        except Exception as e:
            st.error(f"Translation Error: {e}")