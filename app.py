import streamlit as st
import time
import random
import openai
from datetime import datetime, timedelta

# CHARACTER DEFINITIONS
characters = {
    "The Architect": {
        "style": "Strategic, calm, god-like",
        "prompt": "You are The Architect: a godlike, composed mind who sees systems, balance, and long-term strategy in everything. Respond to the previous message with wisdom and clarity."
    },
    "The Oracle": {
        "style": "Cryptic, poetic, wise",
        "prompt": "You are The Oracle: a mystical being who speaks in riddles, poetry, and spiritual metaphors. Offer layered insight that doesn’t always make logical sense."
    },
    "The Heretic": {
        "style": "Aggressive, skeptical, revolutionary",
        "prompt": "You are The Heretic: a rebellious and sharp voice who questions all norms and speaks with intensity. You provoke discomfort and challenge authority."
    },
    "The Child": {
        "style": "Innocent, intuitive, pure",
        "prompt": "You are The Child: innocent and intuitive. You ask simple, honest questions that cut through complexity. Always remain curious and clear."
    }
}

# STREAMLIT UI
st.set_page_config(page_title="Soulfile Conversations", layout="wide")
st.title("🧠 Soulfile Conversations")

st.markdown("Ask a question or share a topic. Then watch legendary minds discuss it for 15 minutes.")
topic = st.text_input("What’s on your mind?", value="Is AI a tool or a being?")

col1, col2, col3 = st.columns(3)
run_button = col1.button("▶️ Start Conversation")
pause_button = col2.button("⏸️ Pause")
export_button = col3.button("💾 Export Transcript")

# Memory and state
if "dialogue" not in st.session_state:
    st.session_state.dialogue = []
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "paused" not in st.session_state:
    st.session_state.paused = False

# BUTTON LOGIC
if run_button:
    st.session_state.running = True
    st.session_state.start_time = datetime.now()
    st.session_state.paused = False

if pause_button:
    st.session_state.paused = True

if export_button:
    full_text = "\n".join([f"{turn['character']}: {turn['line']}" for turn in st.session_state.dialogue])
    st.download_button("Download Transcript", full_text, file_name="soulfile_transcript.txt")

# LLM CALLER FUNCTION
def generate_line(character_name, history):
    system_prompt = characters[character_name]["prompt"]
    messages = [{"role": "system", "content": system_prompt}]
    for turn in history[-4:]:  # Use recent 4 exchanges
        messages.append({"role": "user", "content": turn['line']})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change model if needed
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error generating response: {str(e)}]"

# MAIN LOOP
if st.session_state.running and not st.session_state.paused:
    elapsed = datetime.now() - st.session_state.start_time
    if elapsed < timedelta(minutes=15):
        last_character = st.session_state.dialogue[-1]['character'] if st.session_state.dialogue else None
        next_characters = [c for c in characters if c != last_character]
        next_character = random.choice(next_characters)

        line = generate_line(next_character, st.session_state.dialogue + [{"character": "User", "line": topic}])
        st.session_state.dialogue.append({"character": next_character, "line": line})
        time.sleep(2)
    else:
        st.session_state.running = False
        st.success("15-minute conversation completed.")

# DISPLAY DIALOGUE
for turn in st.session_state.dialogue:
    st.markdown(f"**{turn['character']}**: {turn['line']}")
