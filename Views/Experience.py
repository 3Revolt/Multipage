import streamlit as st
from pathlib import Path
from PIL import Image
from config import assets_dir  # Import assets_dir
from cv_data import JOBS, format_period, lang_code, tr


# --- BACKGROUND IMAGE ---
page_bg_img = """
<style>
body, html {
    margin: 0;
    padding: 0;
    height: 100%;
}

body {
    background-image: url("https://wallpaperbat.com/img/664560-workplace-wallpaper.jpg");
    background-size: cover;  
    background-position: center;
    background-repeat: no-repeat;
}

[data-testid="stAppViewContainer"] > .main {
    background-color: rgba(255, 255, 255, 0.8); /* Prilagodi boju i transparentnost */
    box-shadow: none; /* Ukloni sjenu ako je primijenjena */
    min-height: 100vh; /* Osiguraj da glavni sadržaj zauzima punu visinu */
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


# Helper function to load and resize images (keširano - slike se ne čitaju s diska pri svakom kliku)
@st.cache_resource
def load_and_resize_image(image_name, size=(200, 200)):
    image_path = Path(assets_dir) / image_name
    image = Image.open(image_path)
    image.thumbnail(size)
    return image

PAGE_TITLES = {"bs": "Radno iskustvo", "en": "Experience", "de": "Arbeitserfahrung"}

lang = lang_code(st.session_state.get("selected_language", "Bosanski"))

# Display the title
st.title(PAGE_TITLES[lang])

# --- JOBS (podaci iz cv_data.py) ---
for index, job in enumerate(JOBS):
    if index > 0:
        st.markdown("<br><br><br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    col1.image(load_and_resize_image(job["logo"]), use_container_width=True)
    col1.markdown(job["logo_caption"])

    col2.write(f"**{tr(job['header'], lang)}**")
    col2.write(f"🚧 **{tr(job['subheader'], lang)}**")
    col2.write(format_period(job, lang))
    col2.write("\n".join(f"- ► {duty}" for duty in job["duties"][lang]))
