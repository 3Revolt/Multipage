import streamlit as st
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import re
import time
import random
from pathlib import Path

from config import assets_dir
from rate_limiter import RateLimiter, client_keys, default_storage_path, format_wait
from cv_data import (
    PERSONAL, SKILL_CATEGORIES, PROJECTS, LANGUAGES,
    lang_code, skill_category_line, project_line, education_lines,
)

logger = logging.getLogger(__name__)

# --- BACKGROUND IMAGE ---
page_bg_img = """
<style>
body, html {
    margin: 0;
    padding: 0;
    height: 100%;
}

body {
    background-image: url("https://wallpapercave.com/wp/wp9016401.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

[data-testid="stAppViewContainer"] > .main {
    background-color: rgba(255, 255, 255, 0.8); /* Prilagodi boju i transparentnost */
    box-shadow: none; /* Ukloni sjenu ako je primijenjena */
    min-height: 100vh; /* Osiguraj da glavni sadržaj zauzima punu visinu */
}

/* Honeypot polje za botove - nevidljivo za ljude */
.st-key-contact_website {
    position: absolute !important;
    left: -10000px !important;
    height: 0 !important;
    overflow: hidden !important;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# --- LIMITI FORME ---
MAX_NAME_LENGTH = 100
MAX_MESSAGE_LENGTH = 3000
MIN_FILL_SECONDS = 3          # Botovi popune formu brže od čovjeka
# Ostali limiti (pauza između poruka, dnevni limiti, captcha blokada...) su u rate_limiter.py


# Funkcija za provjeru ispravnosti email adrese
def is_valid_email(email):
    try:
        from email_validator import validate_email, EmailNotValidError
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False
    except ImportError:
        return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None

# --- EMAIL CONFIGURATION ---
EMAIL_AVAILABLE = False
try:
    sender_email = st.secrets["email"]["sender_email"]
    sender_password = st.secrets["email"]["sender_password"]
    receiver_email = st.secrets["email"]["receiver_email"]
    smtp_server = st.secrets["email"]["smtp_server"]
    smtp_port = int(st.secrets["email"]["smtp_port"])
    EMAIL_AVAILABLE = True
except Exception:
    EMAIL_AVAILABLE = False

# --- SECURITY: RATE LIMITER ---
@st.cache_resource
def get_rate_limiter():
    """Jedan limiter dijeljen između svih sesija (detalji u rate_limiter.py)."""
    return RateLimiter(storage_path=default_storage_path())

def get_user_keys():
    """
    Identifikuje posjetioca po javnoj IP adresi i po sesiji (limit važi za oba).
    Lokalne/proxy adrese se ignorišu da svi posjetioci ne bi dijelili isti limit.
    """
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(random.getrandbits(128))
    try:
        headers = dict(st.context.headers)
    except Exception:
        headers = {}
    return client_keys(headers, getattr(st.context, "ip_address", None), st.session_state.user_id)

# --- SECURITY: CAPTCHA ---
def init_captcha():
    if 'captcha_num1' not in st.session_state:
        st.session_state.captcha_num1 = random.randint(1, 10)
    if 'captcha_num2' not in st.session_state:
        st.session_state.captcha_num2 = random.randint(1, 10)

def reset_captcha():
    st.session_state.captcha_num1 = random.randint(1, 10)
    st.session_state.captcha_num2 = random.randint(1, 10)

def clean_header(value):
    """Uklanja nove redove iz vrijednosti koje idu u email header (zaštita od header injection)."""
    return re.sub(r"[\r\n]+", " ", value).strip()

# Funkcija za slanje emaila
def send_email(name, email, message, language):
    if not EMAIL_AVAILABLE:
        return False

    name = clean_header(name)
    email = clean_header(email)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Reply-To'] = formataddr((name, email))  # "Odgovori" u mail klijentu ide direktno pošiljaocu
    msg['Subject'] = f"Message from CV Website - {name}"
    body = f"Name: {name}\nEmail: {email}\nLanguage: {language}\n\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=20)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=20)
        with server:
            if smtp_port != 465:
                server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [receiver_email], msg.as_string())
        return True
    except Exception:
        # Detalji greške idu u log, posjetilac vidi samo generičku poruku
        logger.exception("Slanje emaila nije uspjelo")
        return False

@st.cache_data
def read_file_bytes(path):
    return Path(path).read_bytes()

# Definiši prevode (CV sadržaj dolazi iz cv_data.py)
translations = {
    'English': {
        'contact_me': '✉️ Contact Me',
        'download_cv': '⬇️ Download CV',
        'Skills': 'Technical Skills',
        'Education': 'Education',
        'Projects': 'Key Projects',
        'Languages': 'Languages',
        'your_name': 'Your Name',
        'your_email': 'Your Email',
        'your_message': 'Your Message',
        'send': 'Send',
        'error_email': 'Please enter a valid email address.',
        'error_fields': 'Please fill in all fields.',
        'error_length': f'The name may have at most {MAX_NAME_LENGTH} characters and the message at most {MAX_MESSAGE_LENGTH} characters.',
        'error_links_in_name': 'The name must not contain links.',
        'error_too_fast': 'The form was submitted too quickly. Please wait a moment and try again.',
        'sending': 'Sending your message...',
        'success_message': 'Message sent successfully!',
        'error_message': 'An error occurred while sending the message. Please try again later or write directly to',
        'form_disabled': 'The contact form is currently disabled (email server is not configured). You can write directly to',
        'select_page': 'ABOUT ME',
        'captcha_label': 'Security Check: What is',
        'captcha_error': 'Incorrect calculation. Please try again.',
        'rate_limit_error': 'You have reached the daily message limit. Please try again in {wait}.',
        'cooldown_error': 'Please wait {wait} before sending another message.',
        'email_limit_error': 'Too many messages from this email address today. Please try again in {wait}.',
        'duplicate_error': 'This message has already been sent. Thank you!',
        'locked_error': 'Too many incorrect security answers. The form is locked for {wait}.',
        'global_limit_error': 'The contact form is temporarily busy. Please try again in {wait} or write directly to'
    },
    'Bosanski': {
        'contact_me': '✉️ Kontaktirajte me',
        'download_cv': '⬇️ Preuzmite CV',
        'Skills': 'Tehničke vještine',
        'Education': 'Edukacija',
        'Projects': 'Ključni projekti',
        'Languages': 'Jezici',
        'your_name': 'Vaše Ime',
        'your_email': 'Vaš Email',
        'your_message': 'Vaša Poruka',
        'send': 'Pošaljite',
        'error_email': 'Molimo unesite važeću email adresu.',
        'error_fields': 'Molimo popunite sva polja.',
        'error_length': f'Ime može imati najviše {MAX_NAME_LENGTH} znakova, a poruka najviše {MAX_MESSAGE_LENGTH} znakova.',
        'error_links_in_name': 'Ime ne smije sadržavati linkove.',
        'error_too_fast': 'Forma je poslana prebrzo. Sačekajte trenutak i pokušajte ponovo.',
        'sending': 'Šaljem vašu poruku🚀...',
        'success_message': 'Poruka je uspješno poslana!',
        'error_message': 'Došlo je do greške prilikom slanja poruke. Pokušajte kasnije ili pišite direktno na',
        'form_disabled': 'Kontakt forma je trenutno onemogućena (nije podešen email server). Možete pisati direktno na',
        'select_page': 'O MENI',
        'captcha_label': 'Sigurnosna provjera: Koliko je',
        'captcha_error': 'Netačan rezultat. Molimo pokušajte ponovo.',
        'rate_limit_error': 'Dostigli ste dnevni limit poruka. Pokušajte ponovo za {wait}.',
        'cooldown_error': 'Sačekajte {wait} prije slanja sljedeće poruke.',
        'email_limit_error': 'Previše poruka sa ove email adrese danas. Pokušajte ponovo za {wait}.',
        'duplicate_error': 'Ova poruka je već poslana. Hvala!',
        'locked_error': 'Previše pogrešnih sigurnosnih odgovora. Forma je zaključana na {wait}.',
        'global_limit_error': 'Kontakt forma je trenutno opterećena. Pokušajte ponovo za {wait} ili pišite direktno na'
    },
    'Deutsch': {
        'contact_me': '✉️ Kontaktieren Sie mich',
        'download_cv': '⬇️ CV herunterladen',
        'Skills': 'Technische Fähigkeiten',
        'Education': 'Die Ausbildung',
        'Projects': 'Wichtige Projekte',
        'Languages': 'Sprache',
        'your_name': 'Ihr Name',
        'your_email': 'Ihre E-Mail',
        'your_message': 'Ihre Nachricht',
        'send': 'Senden',
        'error_email': 'Bitte geben Sie eine gültige E-Mail-Adresse ein.',
        'error_fields': 'Bitte füllen Sie alle Felder aus.',
        'error_length': f'Der Name darf höchstens {MAX_NAME_LENGTH} Zeichen und die Nachricht höchstens {MAX_MESSAGE_LENGTH} Zeichen haben.',
        'error_links_in_name': 'Der Name darf keine Links enthalten.',
        'error_too_fast': 'Das Formular wurde zu schnell gesendet. Bitte warten Sie einen Moment und versuchen Sie es erneut.',
        'sending': 'Ihre Nachricht wird gesendet...',
        'success_message': 'Nachricht erfolgreich gesendet!',
        'error_message': 'Beim Senden der Nachricht ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut oder schreiben Sie direkt an',
        'form_disabled': 'Das Kontaktformular ist derzeit deaktiviert (kein E-Mail-Server konfiguriert). Sie können direkt schreiben an',
        'select_page': 'ÜBER MICH',
        'captcha_label': 'Sicherheitsüberprüfung: Wie viel ist',
        'captcha_error': 'Falsches Ergebnis. Bitte versuchen Sie es erneut.',
        'rate_limit_error': 'Sie haben das tägliche Nachrichtenlimit erreicht. Bitte versuchen Sie es in {wait} erneut.',
        'cooldown_error': 'Bitte warten Sie {wait}, bevor Sie eine weitere Nachricht senden.',
        'email_limit_error': 'Zu viele Nachrichten von dieser E-Mail-Adresse heute. Bitte versuchen Sie es in {wait} erneut.',
        'duplicate_error': 'Diese Nachricht wurde bereits gesendet. Vielen Dank!',
        'locked_error': 'Zu viele falsche Sicherheitsantworten. Das Formular ist für {wait} gesperrt.',
        'global_limit_error': 'Das Kontaktformular ist vorübergehend ausgelastet. Bitte versuchen Sie es in {wait} erneut oder schreiben Sie direkt an'
    }
}

# Definiši putanje do CV-a za različite jezike
cv_paths = {
    'English': f'{assets_dir}/CVeng.pdf',
    'Bosanski': f'{assets_dir}/CVbos.pdf',
    'Deutsch': f'{assets_dir}/CVde.pdf'
}

# Postavi podrazumevani jezik na Bosanski ako nije već postavljen
if st.session_state.get('selected_language') not in translations:
    st.session_state.selected_language = 'Bosanski'

selected_language = st.session_state.selected_language
lang = lang_code(selected_language)

# Učitaj prevode na osnovu odabranog jezika
texts = translations[selected_language]

# Prikaz natpisa "Select a page" u skladu sa izabranim jezikom
header_text = f"## {texts['select_page']}"
st.markdown(header_text)

# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image(f"{assets_dir}/cv.gif", use_container_width=True)


with col2:
    st.title(PERSONAL['name'], anchor=False)
    st.subheader(PERSONAL['role'][lang], anchor=False)
    st.write(PERSONAL['description'][lang])

    # Dugme za skrolovanje koristeći HTML
    contact_button_html = f'<a href="#contact-me" style="text-decoration: none;"><button>{texts["contact_me"]}</button></a>'
    st.markdown(contact_button_html, unsafe_allow_html=True)

    # Dugme za preuzimanje CV-a na osnovu odabranog jezika
    cv_filename = f"CV_{selected_language}.pdf"
    st.download_button(
        label=texts['download_cv'],
        data=read_file_bytes(cv_paths[selected_language]),
        file_name=cv_filename,  # Promenjeno ime datoteke
        mime='application/pdf'
    )

# --- Skills ---
st.write("\n")
st.subheader(texts['Skills'], anchor=False)
st.write('\n'.join(skill_category_line(category, lang) for category in SKILL_CATEGORIES))

# --- Projects ---
st.write("\n")
st.subheader(texts['Projects'], anchor=False)
st.write('\n'.join(project_line(project, lang) for project in PROJECTS))

# --- Education ---
st.write("\n")
st.subheader(texts['Education'], anchor=False)
st.write('\n'.join(education_lines(lang)))

# --- Languages ---
st.write("\n")
st.subheader(texts['Languages'], anchor=False)
st.write('\n'.join(f"● {language['label'][lang]}" for language in LANGUAGES))

# --- CONTACT FORM ---
st.write("\n")
st.subheader(texts['contact_me'], anchor="contact-me")

# Inicijalizacija ključeva za formu
if 'contact_name' not in st.session_state: st.session_state.contact_name = ""
if 'contact_email' not in st.session_state: st.session_state.contact_email = ""
if 'contact_message' not in st.session_state: st.session_state.contact_message = ""
if 'form_success' not in st.session_state: st.session_state.form_success = ""
if 'form_loaded_at' not in st.session_state: st.session_state.form_loaded_at = time.time()

# Generate captcha
init_captcha()

# Funkcija za prikaz forme
def show_contact_form():
    if not EMAIL_AVAILABLE:
        st.info(f"{texts['form_disabled']} **{PERSONAL['email']}**.")
        return

    # Identify user (javna IP adresa + sesija)
    user_keys = get_user_keys()
    limiter = get_rate_limiter()

    # Koristimo 'key' parametar za direktno vezivanje na session_state
    st.text_input(texts['your_name'], key="contact_name")
    st.text_input(texts['your_email'], key="contact_email")
    st.text_area(texts['your_message'], key="contact_message")

    # Honeypot: čovjek ne vidi ovo polje, bot ga popuni
    st.text_input("Website", key="contact_website", label_visibility="collapsed")

    # CAPTCHA
    captcha_text = f"{texts['captcha_label']} {st.session_state.captcha_num1} + {st.session_state.captcha_num2}?"
    captcha_response = st.number_input(captcha_text, min_value=0, max_value=100, step=1)

    # Obično dugme umjesto form_submit_button
    submit_button = st.button(texts['send'])

    if submit_button:
        name = st.session_state.contact_name.strip()
        email = st.session_state.contact_email.strip()
        message = st.session_state.contact_message.strip()

        # 0. Bot provjere (tiho odbijanje - bot ne dobija informaciju zašto)
        if st.session_state.get("contact_website"):
            st.session_state.form_success = texts['success_message']
            st.rerun()

        if time.time() - st.session_state.form_loaded_at < MIN_FILL_SECONDS:
            st.error(texts['error_too_fast'])
            return

        # 1. Validation
        if not (name and email and message):
            st.error(texts['error_fields'])
            return

        if len(name) > MAX_NAME_LENGTH or len(message) > MAX_MESSAGE_LENGTH:
            st.error(texts['error_length'])
            return

        if re.search(r"https?://|www\.", name, re.IGNORECASE):
            st.error(texts['error_links_in_name'])
            return

        if not is_valid_email(email):
            st.error(texts['error_email'])
            return

        # 2. CAPTCHA Check
        correct_sum = st.session_state.captcha_num1 + st.session_state.captcha_num2
        allowed, reason, wait = limiter.check(user_keys)
        if reason == "locked":
            st.error(texts['locked_error'].format(wait=format_wait(wait, lang)))
            return

        if captcha_response != correct_sum:
            if limiter.record_captcha_failure(user_keys):
                st.error(texts['locked_error'].format(wait=format_wait(limiter.rules["captcha_lockout"], lang)))
            else:
                st.error(texts['captcha_error'])
            reset_captcha()
            return

        # 3. Rate Limit Check (pauza, dnevni limit, ista email adresa, duplikat, globalni limit)
        allowed, reason, wait = limiter.check(user_keys, email=email, message=message)
        if not allowed:
            error_key = {
                "cooldown": "cooldown_error", "client_limit": "rate_limit_error", "email_limit": "email_limit_error",
                "duplicate": "duplicate_error", "global_limit": "global_limit_error", "locked": "locked_error",
            }[reason]
            error_text = texts[error_key].format(wait=format_wait(wait, lang))
            if reason == "global_limit":
                error_text += f" **{PERSONAL['email']}**."
            if reason == "duplicate":
                st.info(error_text)
            else:
                st.error(error_text)
            return

        # 4. Send Email
        with st.spinner(texts['sending']):
            if send_email(name, email, message, selected_language):
                limiter.record_sent(user_keys, email=email, message=message)
                st.session_state.form_success = texts['success_message']

                # Očisti formu i uradi rerun da se polja vizuelno isprazne
                del st.session_state.contact_name
                del st.session_state.contact_email
                del st.session_state.contact_message
                st.session_state.form_loaded_at = time.time()

                reset_captcha()
                st.rerun()
            else:
                st.error(f"{texts['error_message']} **{PERSONAL['email']}**.")

    # Display success message outside form
    if st.session_state.form_success:
        st.success(st.session_state.form_success)
        st.session_state.form_success = "" # Clear after showing

# Prikaz forme
show_contact_form()
