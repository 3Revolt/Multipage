import streamlit as st
import re
import time

from chatbot_engine import respond, greeting_message
from cv_data import lang_code

# Chatbot radi potpuno OFFLINE - bez interneta i bez API ključeva.
# Sva logika je u chatbot_engine.py, a podaci u cv_data.py.

# --- BACKGROUND IMAGE ---
page_bg_img = """
<style>
body, html {
    margin: 0;
    padding: 0;
    height: 100%;
}
body {
    background-image: url("https://cdn.prod.website-files.com/624629e0591bdc3b300cb644/6594382bbafcb2ef0818295f_VA-HUb%202.png");
    background-size: cover;  
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
[data-testid="stAppViewContainer"] > .main {
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    padding: 20px;
    max-width: 800px;
    margin: auto;
    margin-top: 50px;
}

/* Ciljamo specifično tekst unutar chat poruka */
[data-testid="stChatMessageContent"] {
    color: #000000 !important;
}

[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] div,
[data-testid="stChatMessageContent"] span,
[data-testid="stChatMessageContent"] li {
    color: #000000 !important;
}

/* Pozadina za chat balončiće */
.stChatMessage {
    background-color: rgba(240, 242, 246, 0.95) !important; /* Blago siva pozadina */
    border-radius: 15px;
    border: 1px solid #ddd;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
}

/* User input polje */
.stChatInputContainer {
    padding-bottom: 20px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

UI_TEXTS = {
    "bs": {"intro": "Pitajte me bilo šta o Amarovom iskustvu, vještinama ili obrazovanju.",
           "placeholder": "Upišite pitanje...", "thinking": "Razmišljam..."},
    "en": {"intro": "Ask me anything about Amar's experience, skills, or background.",
           "placeholder": "Type your question here...", "thinking": "Thinking..."},
    "de": {"intro": "Fragen Sie mich alles über Amars Erfahrung, Fähigkeiten oder Werdegang.",
           "placeholder": "Geben Sie Ihre Frage ein...", "thinking": "Denke nach..."},
}

current_language = st.session_state.get("selected_language", "Bosanski")
ui = UI_TEXTS[lang_code(current_language)]

# --- MAIN UI ---

st.title("💬 Chat Assistant")
st.markdown(ui["intro"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": greeting_message(current_language), "greeting": True}]

# Ako je promijenjen jezik prije prvog pitanja - prevedi pozdrav
if len(st.session_state.messages) == 1 and st.session_state.messages[0].get("greeting"):
    st.session_state.messages[0]["content"] = greeting_message(current_language)

# Kontekst razgovora (zadnja firma, tema, jezik) - omogućava pitanja tipa "A koliko dugo?"
if "chat_state" not in st.session_state:
    st.session_state.chat_state = {}

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input(ui["placeholder"]):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        with st.spinner(ui["thinking"]):
            time.sleep(0.3)  # Kratka pauza radi prirodnijeg osjećaja
            full_response = respond(prompt, current_language, st.session_state.chat_state)

        # Typing effect (čuva nove redove, pa liste i formatiranje ostaju ispravni)
        displayed_response = ""
        for chunk in re.split(r"(\s+)", full_response):
            displayed_response += chunk
            if chunk.strip():
                message_placeholder.markdown(displayed_response + "▌")
                time.sleep(0.02)
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
