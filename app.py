import asyncio
import os
import tempfile

import edge_tts
import streamlit as st

MAX_WORDS = 5000

st.set_page_config(page_title="गहरी आवाज़ TTS", page_icon="🎙️")
st.title("🎙️ गहरी आवाज़ – Text to Speech")

text = st.text_area("टेक्स्ट लिखिए", height=220)
words = len(text.split())
st.caption(f"{words} / {MAX_WORDS} शब्द")

voice = st.selectbox(
    "आवाज़",
    [
        "hi-IN-MadhurNeural",
        "hi-IN-SwaraNeural",
        "en-IN-PrabhatNeural",
        "en-US-GuyNeural",
    ],
)
pitch = st.slider("गहराई (कम = ज़्यादा गहरी)", -50, 0, -20)
rate = st.slider("रफ़्तार", -30, 30, -5)

if st.button("🔊 आवाज़ बनाओ", use_container_width=True):
    if not text.strip():
        st.warning("पहले टेक्स्ट लिखिए।")
    elif words > MAX_WORDS:
        st.error(f"टेक्स्ट {MAX_WORDS} शब्द से ज़्यादा है। थोड़ा छोटा कीजिए।")
    else:
        path = os.path.join(tempfile.gettempdir(), "out.mp3")

        async def make():
            comm = edge_tts.Communicate(
                text, voice, rate=f"{rate:+d}%", pitch=f"{pitch:+d}Hz"
            )
            await comm.save(path)

        try:
            with st.spinner("आवाज़ बन रही है..."):
                asyncio.run(make())
            with open(path, "rb") as f:
                data = f.read()
            st.audio(data, format="audio/mp3")
            st.download_button(
                "⬇️ MP3 डाउनलोड करें",
                data,
                file_name="audio.mp3",
                mime="audio/mpeg",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"कुछ गड़बड़ हुई: {e}")
