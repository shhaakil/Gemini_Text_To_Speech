import streamlit as st
from google import genai
from google.genai import types
import wave
import base64

# =========================
# Function to save wave file
# =========================
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

# =========================
# Voice list
# =========================
voices = [
    ("Zephyr", "Bright (F)"),
    ("Puck", "Upbeat (M)"),
    ("Charon", "Informative (M)"),
    ("Kore", "Firm (F)"),
    ("Fenrir", "Excitable (M)"),
    ("Leda", "Youthful (F)"),
    ("Orus", "Firm (M)"),
    ("Aoede", "Breezy (F)"),
    ("Callirrhoe", "Easy-going (F)"),
    ("Autonoe", "Bright (F)"),
    ("Enceladus", "Breathy (M)"),
    ("Iapetus", "Clear (M)"),
    ("Umbriel", "Easy-going (M)"),
    ("Algieba", "Smooth (M)"),
    ("Despina", "Smooth (F)"),
    ("Erinome", "Clear (F)"),
    ("Algenib", "Gravelly (M)"),
    ("Rasalgethi", "Informative (M)"),
    ("Laomedeia", "Upbeat (F)"),
    ("Achernar", "Soft (F)"),
    ("Alnilam", "Firm (M)"),
    ("Schedar", "Even (M)"),
    ("Gacrux", "Mature (F)"),
    ("Pulcherrima", "Forward (M)"),
    ("Achird", "Friendly (M)"),
    ("Zubenelgenubi", "Casual (M)"),
    ("Vindemiatrix", "Gentle (F)"),
    ("Sadachbia", "Lively (M)"),
    ("Sadaltager", "Knowledgeable (M)"),
    ("Sulafat", "Warm (F)")
]

# =========================
# Streamlit App
# =========================
st.set_page_config(
    page_title="Gemini TTS Generator",
    page_icon="🎙️",
    layout="centered"
)

# Sidebar - API key
st.sidebar.header("🔑 Gemini API Key")
api_key = st.sidebar.text_input(
    "Enter your API Key",
    type="password",
    placeholder="sk-xxxxxxxxxxxxxxxx"
)

# Main title
st.title("🎙️ Gemini Text-to-Speech")
st.markdown(
    """
    Generate **high-quality speech** from text using **Google Gemini**.
    Just enter your API key, choose a voice, and write your script.
    """
)

# Voice dropdown
voice_display = [f"{name} — {desc}" for name, desc in voices]
selected_voice = st.selectbox(
    "🎤 Select Voice",
    options=voice_display,
    index=3  # Default to Kore (Firm F)
)
voice_name = voices[voice_display.index(selected_voice)][0]

# Speaking style
prompt = st.text_input(
    "🎭 Speaking Style",
    placeholder="Example: Calm and friendly tone"
)

# Sript to speak

text = st.text_area(
    "📝 Script to Speak",
    placeholder="Type your text here...",
    height=600
)
# Generate button
if st.button("🎧 Generate Audio"):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    elif not prompt or not text:
        st.error("Please enter both a speaking style and script.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            with st.spinner("Generating audio... ⏳"):
                response = client.models.generate_content(
                    model="gemini-2.5-flash-preview-tts",
                    contents=f"{prompt}: {text}",
                    config=types.GenerateContentConfig(
                        response_modalities=["AUDIO"],
                        speech_config=types.SpeechConfig(
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=voice_name
                                )
                            )
                        ),
                    )
                )
                data = response.candidates[0].content.parts[0].inline_data.data
                file_name = "output.wav"
                wave_file(file_name, data)

            # Read and encode file for download
            with open(file_name, "rb") as f:
                audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()

            st.success("✅ Audio generated successfully!")
            st.audio(audio_bytes, format="audio/wav")

            st.download_button(
                label="⬇️ Download Audio",
                data=audio_bytes,
                file_name="output.wav",
                mime="audio/wav"
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")
