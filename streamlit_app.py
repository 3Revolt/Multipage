import streamlit as st
from config import selected_language as default_language  # Import from config.py

# --- LANGUAGE SETUP ---
# Set the default language if not in session state
LANGUAGE_OPTIONS = ["Bosanski", "English", "Deutsch"]
if st.session_state.get('selected_language') not in LANGUAGE_OPTIONS:
    st.session_state.selected_language = default_language

# Language selection in sidebar
selected_language = st.sidebar.selectbox(
    "Select Language / Izaberite jezik / Sprache auswählen", 
    options=LANGUAGE_OPTIONS,
    index=LANGUAGE_OPTIONS.index(st.session_state.selected_language)  # Use the language from session state
)

# Store selected language in session state
st.session_state["selected_language"] = selected_language

# Define titles and page names based on the selected language
if selected_language == "Deutsch":
    page_titles = {
        "About Me": "Über mich",
        "Experience": "Erfahrung",
        "Chat Bot": "Chat Bot"
    }
elif selected_language == "Bosanski":
    page_titles = {
        "About Me": "O meni",
        "Experience": "Iskustvo",
        "Chat Bot": "Chat Bot"
    }
else:
    page_titles = {
        "About Me": "About Me",
        "Experience": "Experience",
        "Chat Bot": "Chat Bot"
    }

# --- PAGE SETUP ---
about_page = st.Page(
    "Views/about_me.py",
    title=page_titles["About Me"],
    icon=":material/account_circle:",
    default=True,
)
experience_page = st.Page(
    "Views/Experience.py",
    title=page_titles["Experience"],
    icon=":material/work:",
)
chat_bot_page = st.Page(
    "Views/chatbot.py",
    title=page_titles["Chat Bot"],
    icon=":material/smart_toy:",
)

# --- NAVIGATION SETUP [WITH SECTIONS] ---
pg = st.navigation(
    {
        "Info": [about_page],
        "Projects": [experience_page, chat_bot_page],
    }
)

# --- SHARED ON ALL PAGES ---
st.sidebar.markdown("Digital CV by Amar Helać")

# --- SIDEBAR BACKGROUND GIF ---
# GIF (~19 MB) se servira kao statički fajl (static/Background.gif) umjesto da se kao base64
# šalje kroz WebSocket pri svakom kliku - to je rušilo vezu sa serverom na Streamlit Cloudu.
SIDEBAR_GIF_URL = "app/static/Background.gif"

# --- SIDEBAR BACKGROUND IMAGE AND TEXT COLOR ---
sidebar_bg_img_and_text_color = f"""
<style>
[data-testid="stSidebar"] > div:first-child {{
    background-image: url("{SIDEBAR_GIF_URL}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: local;
}}
[data-testid="stSidebar"] * {{
    color: #00FF00;  /* Set text color */
}}
</style>
"""
st.markdown(sidebar_bg_img_and_text_color, unsafe_allow_html=True)

# --- RUN NAVIGATION ---
pg.run()