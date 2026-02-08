import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import time
import random

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
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Funkcija za provjeru ispravnosti email adrese
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# --- EMAIL CONFIGURATION ---
EMAIL_AVAILABLE = False
try:
    sender_email = st.secrets["email"]["sender_email"]
    sender_password = st.secrets["email"]["sender_password"]
    receiver_email = st.secrets["email"]["receiver_email"]
    smtp_server = st.secrets["email"]["smtp_server"]
    smtp_port = st.secrets["email"]["smtp_port"]
    EMAIL_AVAILABLE = True
except (KeyError, FileNotFoundError, Exception):
    EMAIL_AVAILABLE = False

# --- SECURITY: RATE LIMITER ---
@st.cache_resource
def get_rate_limiter_storage():
    """
    Vraća rječnik koji se dijeli između svih sesija.
    Format: { "korisnik_id": [timestamp1, timestamp2, ...] }
    """
    return {}

def is_rate_limited(user_key, limit=5, period=86400):
    """
    Provjerava da li je korisnik prešao limit poruka.
    limit: Maksimalan broj poruka (default 5).
    period: Vremenski period u sekundama (default 24h = 86400s).
    """
    storage = get_rate_limiter_storage()
    now = time.time()
    
    # Inicijalizacija ako korisnik ne postoji
    if user_key not in storage:
        storage[user_key] = []
    
    # Očisti stare zapise (starije od 'period')
    storage[user_key] = [t for t in storage[user_key] if now - t < period]
    
    # Provjeri limit
    if len(storage[user_key]) >= limit:
        return True
    
    return False

def log_attempt(user_key):
    """Bilježi uspješno slanje poruke."""
    storage = get_rate_limiter_storage()
    if user_key not in storage:
        storage[user_key] = []
    storage[user_key].append(time.time())

# --- SECURITY: CAPTCHA ---
def init_captcha():
    if 'captcha_num1' not in st.session_state:
        st.session_state.captcha_num1 = random.randint(1, 10)
    if 'captcha_num2' not in st.session_state:
        st.session_state.captcha_num2 = random.randint(1, 10)

def reset_captcha():
    st.session_state.captcha_num1 = random.randint(1, 10)
    st.session_state.captcha_num2 = random.randint(1, 10)

# Funkcija za slanje emaila
def send_email(name, email, message):
    if not EMAIL_AVAILABLE:
        return False
        
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Message from CV Website"
    msg.attach(MIMEText(f"Name: {name}\nEmail: {email}\n\nMessage: {message}", 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# Definiši prevode
translations = {
    'English': {
        'title': 'Amar Helać',
        'description': 'Moreover, I have a keen interest in DevOps practices, combining development and IT operations to improve collaboration and productivity. I can integrate Docker into DevOps pipelines, enabling continuous integration and deployment of applications. This integration ensures that code changes are automatically built, tested, and deployed, leading to faster and more reliable software delivery.',
        'contact_me': '✉️ Contact Me',
        'download_cv': '⬇️ Download CV',
        'Skills': 'Skills',
        'experience': [
            '● MS office, Google Suite, Photoshop             ',
            '● Operating System Administration, Web Administration, etc              ',
            '● Hardware and software maintenance, network equipment, Network Monitoring, etc...             ',
            '● Web Hosting, Active Directory, G Suite Admin             ',
            '● System virtualization technologie (VMware, Hyper-V,)            ',
            '● Linux , Docker , Mac os             ',
            '● Basic Programmierung (C#, Python)             ',
            '● QA Manual course.      '
        ],
        'Education': 'Education',
        'skills': [
            '• 2008 / 2012 - Secondary mechanical technical school                 ',
            '• Constructor on the computer and CNC machines',
        ],
        'Languages': 'Languages',
        'jezici': [
            '● Bosnian                      ',
            '● English(Level C1)               ',
            '● Basic of German                          '
        ],
        'your_name': 'Your Name',
        'your_email': 'Your Email',
        'your_message': 'Your Message',
        'send': 'Send',
        'error_email': 'Please enter a valid email address.',
        'error_fields': 'Please fill in all fields.',
        'sending': 'Sending your message...',
        'success_message': 'Message sent successfully!',
        'error_message': 'An error occurred while sending the message.',
        'select_page': 'ABOUT ME',
        'captcha_label': 'Security Check: What is',
        'captcha_error': 'Incorrect calculation. Please try again.',
        'rate_limit_error': 'You have reached the limit of 5 messages per day. Please try again later.'
    },
    'Bosanski': {
        'title': 'Amar Helać',
        'description': 'Osim toga, imam veliki interes za prakse u DevOps-u, koje kombinuju razvoj i IT operacije radi poboljšanja suradnje i produktivnosti. Mogu integrisati Docker u DevOps tokove rada, omogućavajući kontinuiranu integraciju i implementaciju aplikacija.',
        'contact_me': '✉️ Kontaktirajte me',
        'download_cv': '⬇️ Preuzmite CV',
        'Skills': 'Skills',
        'experience': [
            '● MS office, Google Suite, Photoshop            ',
            '● Administracija OS, Web administracija i sl.              ',
            '● Održavanje hardvera i softvera, mrežne opreme, Network monitoring                  ',
            '● WEB Hosting, Active Directory, Gsuite admin,                ',
            '● Tehnologije virtualizacije sistema (VMware, Hyper-V,)                 ',
            '● Linux, Docker, Mac OS           ',
            '● Osnove Programiranja (C# , Python)                ',
            '● QA Manual kurs.           '
        ],
        'Education': 'Edukacija',
        'skills': [
            '• 2008 / 2012 - Srednja mašinska tehnička škola: SMTS             ',
            '• Konstruktor na računaru i CNC mašinama',
        ],
        'Languages': 'Jezici',
        'jezici': [
            '● Bosnian                      ',
            '● English(Level C1)               ',
            '● Osnove Njemačkog                           '
        ],
        'your_name': 'Vaše Ime',
        'your_email': 'Vaš Email',
        'your_message': 'Vaša Poruka',
        'send': 'Pošaljite',
        'error_email': 'Molimo unesite važeću email adresu.',
        'error_fields': 'Molimo popunite sva polja.',
        'sending': 'Šaljem vašu poruku🚀...',
        'success_message': 'Poruka je uspješno poslana!',
        'error_message': 'Došlo je do greške prilikom slanja poruke.',
        'select_page': 'O MENI',
        'captcha_label': 'Sigurnosna provjera: Koliko je',
        'captcha_error': 'Netračan rezultat. Molimo pokušajte ponovo.',
        'rate_limit_error': 'Dostigli ste limit od 5 poruka dnevno. Molimo pokušajte kasnije.'
    },
    'Deutsch': {
        'title': 'Amar Helać',
        'description': 'Außerdem habe ich ein starkes Interesse an DevOps-Praktiken, die Entwicklung und IT-Operationen kombinieren, um die Zusammenarbeit und Produktivität zu verbessern. Ich kann Docker in DevOps-Pipelines integrieren, um kontinuierliche Integration und Bereitstellung von Anwendungen zu ermöglichen. Diese Integration stellt sicher, dass Code-Änderungen automatisch erstellt, getestet und bereitgestellt werden, was zu schnellerer und zuverlässigerer Software-Lieferung führt.',
        'contact_me': '✉️ Kontaktieren Sie mich',
        'download_cv': '⬇️ CV herunterladen',
        'Skills': 'Fähigkeit',
        'experience': [
            '● Microsoft Office, Google Suite, Photoshop               ',
            '● Betriebssystemadministration, Webadministration, usw.         ',
            '●  Webhosting, Active Directory, G Suite-Verwaltung                        ',
            '● Systemvirtualisterungstechnologien (VMware, Hyper-V,)                        ',
            '● Linux, Docker, Mac OS                       ',
            '● Grundlegende Programmierung (C#, Python)                       ',
            '● QA-Handbuchkurs.                           '
        ],
        'Education': 'Die Ausbildung',
        'skills': [
            '•   2008 / 2012 – Technische Mittelschule für Maschinenbau         ',
            '•   Konstrukteur am Computer und an CNC-Maschinen',
        ],
        'Languages': 'Sprache',
        'jezici': [
            '● Bosnian                      ',
            '● English(Level C1)               ',
            '● Grundlegend Deutschland                           '
        ],
        'your_name': 'Ihr Name',
        'your_email': 'Ihre E-Mail',
        'your_message': 'Ihre Nachricht',
        'send': 'Senden',
        'error_email': 'Bitte geben Sie eine gültige E-Mail-Adresse ein.',
        'error_fields': 'Bitte füllen Sie alle Felder aus.',
        'sending': 'Ihre Nachricht wird gesendet...',
        'success_message': 'Nachricht erfolgreich gesendet!',
        'error_message': 'Ein Fehler ist beim Senden der Nachricht aufgetreten.',
        'select_page': 'ÜBER MICH',
        'captcha_label': 'Sicherheitsüberprüfung: Wie viel ist',
        'captcha_error': 'Falsches Ergebnis. Bitte versuchen Sie es erneut.',
        'rate_limit_error': 'Sie haben das Limit von 5 Nachrichten pro Tag erreicht. Bitte versuchen Sie es später erneut.'
    }
}

# Definiši putanje do CV-a za različite jezike
cv_paths = {
    'English': 'assets/CVeng.pdf',
    'Bosanski': 'assets/CVbos.pdf',
    'Deutsch': 'assets/CVde.pdf'
}

# Postavi podrazumevani jezik na Bosanski ako nije već postavljen
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'Bosanski'

selected_language = st.session_state.selected_language

# Učitaj prevode na osnovu odabranog jezika
texts = translations[selected_language]

# Prikaz natpisa "Select a page" u skladu sa izabranim jezikom
header_text = f"## {texts['select_page']}"
st.markdown(header_text)

# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("assets/cv.gif", use_container_width=True)


with col2:
    st.title(texts['title'], anchor=False)
    st.write(texts['description'])

    # Dugme za skrolovanje koristeći HTML
    contact_button_html = f'<a href="#contact-me" style="text-decoration: none;"><button>{texts["contact_me"]}</button></a>'
    st.markdown(contact_button_html, unsafe_allow_html=True)

    # Dugme za preuzimanje CV-a na osnovu odabranog jezika
    cv_filename = f"CV_{selected_language}.pdf"
    st.download_button(
        label=texts['download_cv'],
        data=open(cv_paths[selected_language], 'rb').read(),
        file_name=cv_filename,  # Promenjeno ime datoteke
        mime='application/pdf'
    )

# --- Skills ---
st.write("\n")
st.subheader(texts['Skills'], anchor=False)
st.write('\n'.join(texts['experience']))

# --- Education ---
st.write("\n")
st.subheader(texts['Education'], anchor=False)
st.write('\n'.join(texts['skills']))

# --- Languages ---
st.write("\n")
st.subheader(texts['Languages'], anchor=False)
st.write('\n'.join(texts['jezici']))

# --- CONTACT FORM ---
st.write("\n")
st.subheader(texts['contact_me'], anchor="contact-me")

# Inicijalizacija ključeva za formu
if 'contact_name' not in st.session_state: st.session_state.contact_name = ""
if 'contact_email' not in st.session_state: st.session_state.contact_email = ""
if 'contact_message' not in st.session_state: st.session_state.contact_message = ""
if 'form_success' not in st.session_state: st.session_state.form_success = ""

# Generate captcha
init_captcha()

# Funkcija za prikaz forme
def show_contact_form():
    if not EMAIL_AVAILABLE:
        st.info("Kontakt forma je trenutno onemogućena (nije podešen email server).")
        return

    # Identify user
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(random.getrandbits(128))
    user_key = st.session_state.user_id

    # Check Limit
    limit_reached = is_rate_limited(user_key)

    with st.form("contact_form"):
        # Koristimo 'key' parametar za direktno vezivanje na session_state
        name = st.text_input(texts['your_name'], key="contact_name")
        email = st.text_input(texts['your_email'], key="contact_email")
        message = st.text_area(texts['your_message'], key="contact_message")
        
        # CAPTCHA
        captcha_text = f"{texts['captcha_label']} {st.session_state.captcha_num1} + {st.session_state.captcha_num2}?"
        captcha_response = st.number_input(captcha_text, min_value=0, max_value=100, step=1)
        
        submit_button = st.form_submit_button(texts['send'])

    if submit_button:
        # 1. Validation
        if not (name and email and message):
            st.error(texts['error_fields'])
            return

        if not is_valid_email(email):
            st.error(texts['error_email'])
            return

        # 2. CAPTCHA Check
        correct_sum = st.session_state.captcha_num1 + st.session_state.captcha_num2
        if captcha_response != correct_sum:
            st.error(texts['captcha_error'])
            reset_captcha()
            return

        # 3. Rate Limit Check
        if is_rate_limited(user_key):
            st.error(texts['rate_limit_error'])
            return

        # 4. Send Email
        with st.spinner(texts['sending']):
            if send_email(name, email, message):
                log_attempt(user_key)
                st.session_state.form_success = texts['success_message']
                
                # Clear form (using keys)
                st.session_state.contact_name = ""
                st.session_state.contact_email = ""
                st.session_state.contact_message = ""
                reset_captcha()
                st.rerun()
            else:
                st.error(texts['error_message'])
    
    # Display success message outside form
    if st.session_state.form_success:
        st.success(st.session_state.form_success)
        st.session_state.form_success = "" # Clear after showing

# Prikaz forme
show_contact_form()