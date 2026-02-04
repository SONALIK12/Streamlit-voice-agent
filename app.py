import streamlit as st
from streamlit_mic_recorder import mic_recorder
from openai import AzureOpenAI
import os
import time
import base64
import streamlit.components.v1 as components
from dotenv import load_dotenv
import json
from pathlib import Path

# Load environment variables
load_dotenv()

# --- Language detection (Hindi vs English) ---
def detect_hi_en(text: str) -> str:
    """Return 'hi' if text is predominantly Hindi (Devanagari), else 'en'."""
    if not text:
        return 'en'
    devanagari = sum(1 for ch in text if '\u0900' <= ch <= '\u097F')
    letters = sum(1 for ch in text if ch.isalpha())
    # If at least 30% of letters are Devanagari, treat as Hindi
    if letters > 0 and (devanagari / letters) >= 0.3:
        return 'hi'
    return 'en'

# Helpers to create per-service clients (chat, stt, tts)
def make_client(prefix: str) -> AzureOpenAI:
    api_key = os.getenv(f"{prefix}_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv(f"{prefix}_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv(f"{prefix}_API_VERSION") or os.getenv("AZURE_OPENAI_API_VERSION")
    return AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=endpoint)

# Helper to validate that either per-service or global credentials exist
def _missing_creds(prefix: str) -> list[str]:
    api_key = os.getenv(f"{prefix}_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv(f"{prefix}_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv(f"{prefix}_API_VERSION") or os.getenv("AZURE_OPENAI_API_VERSION")
    missing: list[str] = []
    if not api_key:
        missing.append(f"{prefix}_API_KEY or AZURE_OPENAI_API_KEY")
    if not endpoint:
        missing.append(f"{prefix}_ENDPOINT or AZURE_OPENAI_ENDPOINT")
    if not api_version:
        missing.append(f"{prefix}_API_VERSION or AZURE_OPENAI_API_VERSION")
    return missing

# Page configuration
st.set_page_config(
    page_title="Voice Chat Agent",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Voice Chat Agent")
st.write("Speak into the mic → AI listens → replies back in voice!")

# Add some styling
st.markdown("""
<style>
    .stAudio {
        margin-top: 10px;
        margin-bottom: 10px;
    }
        /* Container spacing for custom audio with avatar */
        .cat-audio-container { margin: 8px 0 12px; }
</style>
""", unsafe_allow_html=True)

# --- Smart memory (preferences) ---
MEMORY_PATH = Path(__file__).parent / "memory.json"

def load_memory():
    try:
        if MEMORY_PATH.exists():
            with open(MEMORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {
        "preferred_name": "",
        "speak_style": "normal",  # normal | slower | faster
    }

def save_memory(mem: dict):
    try:
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(mem, f, ensure_ascii=False, indent=2)
    except Exception:
        # Non-fatal; just ignore save errors
        pass

if "memory" not in st.session_state:
    st.session_state["memory"] = load_memory()
# Render a speaking avatar synced to audio (shows on play, hides on end)
def render_cat_audio(audio_bytes: bytes, label: str = "AI speaking…"):
        data_url = "data:audio/mpeg;base64," + base64.b64encode(audio_bytes).decode("ascii")
        html = f"""
        <div class="cat-audio-container" id="cat-audio">
            <style>
                .cat-wrap {{ display:none; align-items:center; gap:12px; margin: 6px 0 4px; }}
                .cat {{ position:relative; width:64px; height:64px; border-radius:16px; background:linear-gradient(180deg,#fbbf24,#eab308); box-shadow:0 8px 16px rgba(0,0,0,0.15); border:1px solid rgba(0,0,0,0.05); }}
                .cat:before, .cat:after {{ content:""; position:absolute; top:-6px; width:18px; height:18px; background:linear-gradient(180deg,#fcd34d,#f59e0b); transform: rotate(45deg); }}
                .cat:before {{ left:8px; border-top-left-radius:4px; }}
                .cat:after {{ right:8px; border-top-right-radius:4px; }}
                .cat-eye {{ position:absolute; top:22px; width:10px; height:10px; background:#111827; border-radius:50%; }}
                .cat-eye.left {{ left:18px; }}
                .cat-eye.right {{ right:18px; }}
                .cat-mouth {{ position:absolute; left:50%; transform:translateX(-50%); bottom:14px; width:24px; height:6px; background:#111827; border-radius:3px; animation:catTalk 520ms ease-in-out infinite; }}
                @keyframes catTalk {{ 0%,100%{{height:6px}} 50%{{height:16px}} }}
                .cat-label {{ font-size:0.95rem; opacity:0.85; color:#374151; }}
                .audio-wrap {{ margin-top: 6px; }}
            </style>
            <div class="cat-wrap">
                <div class="cat">
                    <span class="cat-eye left"></span>
                    <span class="cat-eye right"></span>
                    <span class="cat-mouth"></span>
                </div>
                <div class="cat-label">{label}</div>
            </div>
            <div class="audio-wrap">
                <audio id="cat-audio-el" src="{data_url}" controls autoplay></audio>
            </div>
      
            <script>
                (function() {{
                    const wrap = window.parent.document.querySelector('#cat-audio .cat-wrap') || document.querySelector('#cat-audio .cat-wrap');
                    const audio = window.parent.document.querySelector('#cat-audio-el') || document.getElementById('cat-audio-el');
                    if (!wrap || !audio) return;
                    wrap.style.display = 'none';
                    const show = () => wrap.style.display = 'flex';
                    const hide = () => wrap.style.display = 'none';
                    audio.addEventListener('play', show);
                    audio.addEventListener('playing', show);
                    audio.addEventListener('ended', hide);
                    audio.addEventListener('pause', () => {{ if (audio.currentTime >= audio.duration - 0.25) hide(); }});
                }})();
            </script>
        </div>
        """
        components.html(html, height=150)

# Manual test panel removed as requested

# Validate credentials per service (allowing per-service overrides or global fallbacks)
missing_chat = _missing_creds("AZURE_OPENAI_CHAT")
missing_stt = _missing_creds("AZURE_OPENAI_WHISPER")
missing_tts = _missing_creds("AZURE_OPENAI_TTS")

if missing_chat or missing_stt or missing_tts:
    st.error("⚠️ Missing Azure OpenAI configuration.")
    if missing_chat:
        st.write("Chat missing:", ", ".join(missing_chat))
    if missing_stt:
        st.write("Speech-to-Text missing:", ", ".join(missing_stt))
    if missing_tts:
        st.write("Text-to-Speech missing:", ", ".join(missing_tts))
    st.info("Set these in a local `.env` (not committed) or in Streamlit Cloud → Settings → Environment variables. See `.env.example` for names and versions.")
    st.stop()

# Create clients only after validation so app fails gracefully if env vars are absent
chat_client = make_client("AZURE_OPENAI_CHAT")
stt_client = make_client("AZURE_OPENAI_WHISPER")
tts_client = make_client("AZURE_OPENAI_TTS")

# Record audio
audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹️ Stop Recording",
    key="mic"
)

# If audio was recorded
if audio:
    # The audio data is stored directly in the 'bytes' key or as the audio variable itself
    audio_bytes = audio.get("bytes") if isinstance(audio, dict) else audio
    
    st.audio(audio_bytes, format="audio/wav")

    try:
        # --- Speech to text ---
        with st.spinner("⏳ Transcribing your voice..."):
            whisper_deployment = os.getenv("AZURE_OPENAI_WHISPER_DEPLOYMENT", "whisper")
            try:
                user_text = stt_client.audio.transcriptions.create(
                    file=("audio.wav", audio_bytes),
                    model=whisper_deployment
                ).text
            except Exception as stt_err:
                st.error("Speech-to-text failed. Check that your Whisper deployment name and endpoint match.")
                st.info(
                    "Using endpoint: " + (os.getenv('AZURE_OPENAI_WHISPER_ENDPOINT') or os.getenv('AZURE_OPENAI_ENDPOINT', 'Not set'))
                )
                raise stt_err

        st.success("**You said:**")
        st.write(user_text)

        # --- Language detection ---
        detected_lang = detect_hi_en(user_text) if st.session_state.get("auto_lang", True) else 'en'
        st.caption(f"Detected language: {'Hindi' if detected_lang=='hi' else 'English'}")

        # --- LLM reply ---
        with st.spinner("🤔 AI is thinking..."):
            chat_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4")
            # Apply smart memory to system prompt
            mem = st.session_state.get("memory", {"preferred_name":"","speak_style":"normal"})
            name_clause = f" Address the user as {mem['preferred_name']}." if mem.get("preferred_name") else ""
            style_clause = {
                "normal": "",
                "slower": " Speak a bit slower and clearer.",
                "faster": " Speak a bit faster and energetic."
            }.get(mem.get("speak_style","normal"), "")
            base_hint_hi = "You are a helpful voice assistant. Reply in Hindi. Keep responses concise and conversational."
            base_hint_en = "You are a helpful voice assistant. Reply in English. Keep responses concise and conversational."
            system_hint = (base_hint_hi if detected_lang=='hi' else base_hint_en) + name_clause + style_clause
            reply_text = chat_client.chat.completions.create(
                model=chat_deployment,
                messages=[
                    {"role": "system", "content": system_hint},
                    {"role": "user", "content": user_text}
                ]
            ).choices[0].message.content

        st.success("**AI Response:**")
        st.write(reply_text)

        # --- Text to speech ---
        try:
            with st.spinner("🔊 Generating voice response..."):
                tts_deployment = os.getenv("AZURE_OPENAI_TTS_DEPLOYMENT", "tts")
                reply_audio = tts_client.audio.speech.create(
                    model=tts_deployment,
                    voice=st.session_state.get("voice", "nova"),
                    input=reply_text
                ).read()

            # Render cat avatar + audio; cat shows on play, hides on ended
            render_cat_audio(reply_audio)
        except Exception as tts_error:
            st.warning("⚠️ Text-to-speech is not available yet. You can read the response above.")
            st.info(f"TTS Error: {str(tts_error)[:160]}")
            st.caption(
                "Using endpoint: "
                + (os.getenv("AZURE_OPENAI_TTS_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT", "Not set"))
                + " | API version: "
                + (os.getenv("AZURE_OPENAI_TTS_API_VERSION") or os.getenv("AZURE_OPENAI_API_VERSION", "Not set"))
                + " | Deployment: "
                + (os.getenv("AZURE_OPENAI_TTS_DEPLOYMENT") or "tts")
            )

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Make sure your Azure OpenAI credentials are valid and your deployments are correctly configured in Azure Portal.")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This voice chat agent uses:
    - **Azure OpenAI Whisper** for speech-to-text
    - **Azure OpenAI GPT-4** for intelligent responses
    - **Azure OpenAI TTS** for text-to-speech
    """)
    
    st.header("🔧 Configuration")
    st.write("**Chat endpoint:** " + (os.getenv('AZURE_OPENAI_CHAT_ENDPOINT') or os.getenv('AZURE_OPENAI_ENDPOINT', 'Not set')))
    st.write("**STT endpoint:** " + (os.getenv('AZURE_OPENAI_WHISPER_ENDPOINT') or os.getenv('AZURE_OPENAI_ENDPOINT', 'Not set')))
    st.write("**TTS endpoint:** " + (os.getenv('AZURE_OPENAI_TTS_ENDPOINT') or os.getenv('AZURE_OPENAI_ENDPOINT', 'Not set')))
    st.write(f"**API Version:** {os.getenv('AZURE_OPENAI_API_VERSION', 'Not set')}")
    
    st.header("🎨 Voice Options")
    voices = ["nova", "alloy", "echo", "fable", "onyx", "shimmer"]
    _default_voice = st.session_state.get("voice", "nova")
    try:
        _default_index = voices.index(_default_voice)
    except ValueError:
        _default_index = 0
    selected_voice = st.selectbox("Select TTS voice", voices, index=_default_index)
    st.session_state["voice"] = selected_voice
    st.write(f"Current voice: **{selected_voice.title()}**")

    st.header("🌐 Language")
    auto_lang = st.checkbox("Auto-detect Hindi/English", value=True, key="auto_lang")
    st.caption("If enabled, the assistant will reply in the same language as your speech.")

    st.header("🧠 Preferences (Memory)")
    mem = st.session_state["memory"]
    preferred_name = st.text_input("What should I call you?", value=mem.get("preferred_name", ""))
    speak_style = st.selectbox("Speaking style", ["normal", "slower", "faster"], index=["normal","slower","faster"].index(mem.get("speak_style","normal")))
    if st.button("Save preferences"):
        st.session_state["memory"] = {"preferred_name": preferred_name.strip(), "speak_style": speak_style}
        save_memory(st.session_state["memory"]) 
        st.success("Preferences saved.")
    
    st.header("💡 Tips")
    st.write("""
    - Speak clearly into your microphone
    - Keep questions concise
    - Wait for the recording to stop before processing
    """)

    with st.expander("🩺 Diagnostics", expanded=False):
        def _mask(v: str | None):
            if not v:
                return "Not set"
            return (v[:4] + "…" + v[-4:]) if len(v) > 8 else "••••"

        st.markdown("**Chat**")
        st.write("Endpoint:", os.getenv('AZURE_OPENAI_CHAT_ENDPOINT') or os.getenv('AZURE_OPENAI_ENDPOINT', 'Not set'))
        st.write("API Version:", os.getenv('AZURE_OPENAI_CHAT_API_VERSION') or os.getenv('AZURE_OPENAI_API_VERSION', 'Not set'))
        st.write("Deployment:", os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT') or 'gpt-4.1')
        st.write("Key:", _mask(os.getenv('AZURE_OPENAI_CHAT_API_KEY') or os.getenv('AZURE_OPENAI_API_KEY')))

        st.markdown("**Speech-to-Text (Whisper)**")
        st.write("Endpoint:", os.getenv('AZURE_OPENAI_WHISPER_ENDPOINT') or os.getenv('AZURE_OPENAI_ENDPOINT', 'Not set'))
        st.write("API Version:", os.getenv('AZURE_OPENAI_WHISPER_API_VERSION') or os.getenv('AZURE_OPENAI_API_VERSION', 'Not set'))
        st.write("Deployment:", os.getenv('AZURE_OPENAI_WHISPER_DEPLOYMENT') or 'whisper')
        st.write("Key:", _mask(os.getenv('AZURE_OPENAI_WHISPER_API_KEY') or os.getenv('AZURE_OPENAI_API_KEY')))

        st.markdown("**Text-to-Speech (TTS)**")
        st.write("Endpoint:", os.getenv('AZURE_OPENAI_TTS_ENDPOINT') or os.getenv('AZURE_OPENAI_ENDPOINT', 'Not set'))
        st.write("API Version:", os.getenv('AZURE_OPENAI_TTS_API_VERSION') or os.getenv('AZURE_OPENAI_API_VERSION', 'Not set'))
        st.write("Deployment:", os.getenv('AZURE_OPENAI_TTS_DEPLOYMENT') or 'tts')
        st.write("Key:", _mask(os.getenv('AZURE_OPENAI_TTS_API_KEY') or os.getenv('AZURE_OPENAI_API_KEY')))
