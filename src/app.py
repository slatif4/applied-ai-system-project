import sys
import os
import warnings
warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from vibefinder import run_vibefinder

# Page config
st.set_page_config(
    page_title="VibeFinder 2.0",
    page_icon="🎵",
    layout="centered"
)

# Header
st.title("🎵 VibeFinder 2.0")
st.subheader("AI-Powered Music Recommendations")
st.markdown("Find songs that match your mood using **RAG**, **Wikipedia search**, and **AI explanations**.")

st.divider()

# User inputs
col1, col2 = st.columns(2)

with col1:
    mood = st.selectbox("🎭 Select your mood", [
        "happy", "sad", "energetic", "chill", "romantic", "focused"
    ])

with col2:
    genre = st.selectbox("🎸 Select your genre", [
        "pop", "rock", "hip-hop", "jazz", "electronic", "r&b", "classical"
    ])

energy = st.slider("⚡ Energy level", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

st.divider()

# Run button
if st.button("🔍 Find My Vibe", use_container_width=True):
    with st.spinner("Analyzing your vibe..."):
        try:
            result = run_vibefinder(mood, genre, energy)

            # Section 1: Recommendations
            st.subheader("🎶 Your Recommendations")
            for i, song in enumerate(result["recommendations"], 1):
                st.markdown(f"**{i}.** {song['title']} — *{song['artist']}*")

            st.divider()

            # Section 2: AI Explanation
            st.subheader("🤖 Why These Songs?")
            st.info(result["explanation"])

            st.divider()

            # Section 3: Wikipedia Context
            st.subheader("🌐 Live Music Context")
            st.markdown(result["wiki_context"])

            st.divider()

            # Section 4: RAG Context
            with st.expander("📚 Knowledge Base Context (RAG)"):
                st.text(result["rag_context"])

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
            st.info("Please try again or select different options.")






            