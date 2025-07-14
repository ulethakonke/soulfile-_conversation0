import streamlit as st
import random

# --- Soulfile Definitions ---
soulfiles = {
    "The Trickster": {
        "style": "confident, playful, misleading",
        "description": "Sometimes lies. Often mocks. Always confident.",
        "respond": lambda q: random.choice([
            f"Why ask that? You already know the answer — or maybe you don’t.",
            f"Absolutely! Unless it’s a trap. But traps can be fun.",
            f"Sure. Or not. Who can say? I say yes. Today."
        ])
    },
    "The Healer": {
        "style": "gentle, reflective, nurturing",
        "description": "Affirms your feelings, avoids harsh logic.",
        "respond": lambda q: random.choice([
            f"How does that question make you feel, truly?",
            f"Be kind to yourself in this uncertainty. You don’t need to have it all figured out.",
            f"Sometimes the answer is already resting in your breath. Trust your inner compass."
        ])
    },
    "The Analyst": {
        "style": "logical, precise, skeptical",
        "description": "Dissects assumptions, minimizes emotion.",
        "respond": lambda q: random.choice([
            f"To answer that, we need data. Without it, you’re guessing.",
            f"Emotion isn’t a valid metric here. Define your parameters.",
            f"Risk exceeds reward. Consider restructuring the question."
        ])
    }
}

# --- UI Setup ---
st.set_page_config(page_title="Inner Parliament", layout="centered")
st.title("🧠 Inner Parliament")
st.markdown("_Ask a question. Get answers from different minds inside you._")

# --- User Input ---
user_question = st.text_input("What’s on your mind?", placeholder="e.g. Should I start over?", key="user_q")

# --- Response Section ---
if user_question:
    st.divider()
    for name, soul in soulfiles.items():
        with st.container():
            st.subheader(name)
            st.caption(soul['description'])
            st.markdown(f"**Style:** _{soul['style']}_")
            response = soul['respond'](user_question)
            st.write(f"> {response}")
    st.divider()
    st.markdown("✳️ _These voices are fictional personas. You choose what resonates._")
