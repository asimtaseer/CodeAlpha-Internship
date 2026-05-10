import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="Language Translation Tool",
    layout="centered"
)

# --- Custom Styling ---
# Adding modern, clean styling and the CodeAlpha watermark in the corner
st.markdown("""
    <style>
    .codealpha-logo {
        position: fixed;
        top: 10px;
        right: 10px;
        font-size: 14px;
        color: #888;
        font-family: Arial, sans-serif;
        font-weight: bold;
        z-index: 1000;
        background-color: rgba(255, 255, 255, 0.7);
        padding: 5px 10px;
        border-radius: 5px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }
    .main-title {
        color: #1E88E5;
        text-align: center;
        font-weight: 700;
    }
    .stTextArea textarea {
        border-radius: 8px;
    }
    </style>
    <div class="codealpha-logo">CodeAlpha Internship</div>
""", unsafe_allow_html=True)

# --- App Title & Description ---
st.markdown("<h1 class='main-title'>Language Translation Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Fast, accurate, and easy-to-use translator with Text-to-Speech support.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Initialize Translator ---
translator = Translator()

# Get list of supported languages
# LANGUAGES is a dictionary like {'af': 'afrikaans', 'sq': 'albanian', ...}
language_choices = {name.title(): code for code, name in LANGUAGES.items()}
language_names = list(language_choices.keys())

# --- User Interface ---
col1, col2 = st.columns(2)

with col1:
    # Auto-detect is not in the list natively, so we just set english as default
    source_lang_name = st.selectbox("Source Language", ["Auto-Detect"] + language_names, index=0)

with col2:
    # Set default target as Spanish or whichever is convenient
    default_target_index = language_names.index("Spanish") if "Spanish" in language_names else 0
    target_lang_name = st.selectbox("Target Language", language_names, index=default_target_index)

# Text area for user input
text_to_translate = st.text_area("Enter text to translate", height=150, placeholder="Type something here...")

# --- Translation Logic ---
if st.button("Translate", use_container_width=True):
    if text_to_translate.strip() == "":
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            try:
                # Determine source language code
                if source_lang_name == "Auto-Detect":
                    src_code = 'auto'
                else:
                    src_code = language_choices[source_lang_name]
                
                # Determine target language code
                dest_code = language_choices[target_lang_name]
                
                # Perform translation
                result = translator.translate(text_to_translate, src=src_code, dest=dest_code)
                translated_text = result.text
                
                st.success("Translation Complete!")
                
                # Display Translated Text
                st.markdown("### Translated Text:")
                # We use st.code block because it comes with a built-in copy button!
                st.code(translated_text, language="")
                
                # --- Text-to-Speech Feature ---
                st.markdown("### Text-to-Speech")
                try:
                    # Generate speech from translated text
                    tts = gTTS(text=translated_text, lang=dest_code, slow=False)
                    audio_file = "translated_audio.mp3"
                    tts.save(audio_file)
                    
                    # Read the audio file and play it via streamlit
                    audio_bytes = open(audio_file, "rb").read()
                    st.audio(audio_bytes, format="audio/mp3")
                    
                    # Cleanup audio file
                    os.remove(audio_file)
                except Exception as e:
                    st.error(f"Text-to-Speech is currently not supported for the selected language ({target_lang_name}).")
                
            except Exception as e:
                st.error(f"An error occurred during translation: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: gray;'>Built for CodeAlpha  |  Powered by Python & Streamlit</p>", unsafe_allow_html=True)
