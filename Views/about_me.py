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
        'subtitle': 'IT Specialist | Support & Automation',
        'description': 'IT professional with over 10 years of experience in system administration and technical support. Currently focused on improving IT workflows through DevOps practices and AI-driven automation to enhance workplace efficiency.',
        'contact_me': '✉️ Contact Me',
        'download_cv': '⬇️ Download CV',
        'Skills': 'Technical Skills',
        'experience': [
            '● **Programming & Frameworks:** Python (Advanced), TypeScript, React, Vite, Tailwind CSS, C#, JavaScript/jQuery, Basic programming.',
            '● **AI & Automation:** LLM integration (Gemini API, Ollama), Multi-agent systems (AutoGen, Aider), Google Cloud API, PowerPoint VBA automation.',
            '● **DevOps & Cloud:** Docker, Linux (Ubuntu/Debian), CI/CD pipelines, Web Hosting administration, Mac OS.',
            '● **Virtualization & Infrastructure:** VMware, Hyper-V, VirtualBox (Multi-OS environments).',
            '● **System Admin:** Active Directory, G Suite Admin, OS Administration, Network & Security equipment configuration, Hardware & Software maintenance, Network Monitoring.',
            '● **Specialized Tools:** MS Office, Google Suite, Photoshop, Joomla (K2), 3D modeling (Rodin-3D, ComfyUI, .glb), QA Manual course.'
        ],
        'Education': 'Education',
        'skills': [
            '• 2008 / 2012 - Secondary mechanical technical school',
            '• Constructor on the computer and CNC machines',
        ],
        'Projects': 'Key Projects',
        'project_list': [
            '🚀 **AI Help Desk Ticketing System:** Developed a custom Linux-based ticketing application integrated with Gemini API for automated response generation.',
            '🛠️ **Local AI Development Lab:** Built and optimized a high-performance local environment using Ubuntu VMs, Docker, and Ollama for LLM deployment.',
            '🌐 **Web Development Portfolio:** Created modern web interfaces for companies like INTESECO using React and Tailwind CSS.',
            '🤖 **AI 3D Asset Pipeline:** Experimented with generative AI tools (Rodin-3D, DINOv3) for creating and integrating .glb files into web applications.'
        ],
        'Languages': 'Languages',
        'jezici': [
            '● Bosnian (Native)',
            '● English (Level C1)',
            '● German (Basic)'
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
        'subtitle': 'IT Specijalista | Podrška i automatizacija',
        'description': 'IT profesionalac sa preko 10 godina iskustva u sistemskoj administraciji i tehničkoj podršci. Trenutno fokusiran na unapređenje IT procesa kroz DevOps prakse i AI automatizaciju u svrhu poboljšanja efikasnosti rada.',
        'contact_me': '✉️ Kontaktirajte me',
        'download_cv': '⬇️ Preuzmite CV',
        'Skills': 'Tehničke vještine',
        'experience': [
            '● **Programiranje i Frameworks:** Python (Advanced), TypeScript, React, Vite, Tailwind CSS, C#, JavaScript/jQuery, Osnove programiranja.',
            '● **AI i Automatizacija:** LLM integracija (Gemini API, Ollama), Multi-agent sistemi (AutoGen, Aider), Google Cloud API, PowerPoint VBA automatizacija.',
            '● **DevOps i Cloud:** Docker, Linux (Ubuntu/Debian), CI/CD pipelines, Web Hosting administracija, Mac OS.',
            '● **Virtualizacija i Infrastruktura:** VMware, Hyper-V, VirtualBox (Multi-OS okruženja).',
            '● **Sistemska Administracija:** Active Directory, G Suite Admin, Administracija OS, Konfiguracija mrežne i sigurnosne opreme, Održavanje hardvera i softvera, Network monitoring.',
            '● **Specijalizovani Alati:** MS Office, Google Suite, Photoshop, Joomla (K2), 3D modelovanje (Rodin-3D, ComfyUI, .glb), QA Manual kurs.'
        ],
        'Education': 'Edukacija',
        'skills': [
            '• 2008 / 2012 - Srednja mašinska tehnička škola: SMTS',
            '• Konstruktor na računaru i CNC mašinama',
        ],
        'Projects': 'Ključni projekti',
        'project_list': [
            '🚀 **AI Help Desk Ticketing System:** Razvoj prilagođene Linux aplikacije za tiketing integrisane sa Gemini API-jem za automatsko generisanje odgovora.',
            '🛠️ **Local AI Development Lab:** Izgradnja i optimizacija lokalnog okruženja visokih performansi koristeći Ubuntu VM, Docker i Ollama za LLM implementaciju.',
            '🌐 **Web Development Portfolio:** Kreiranje modernih web interfejsa za kompanije poput INTESECO koristeći React i Tailwind CSS.',
            '🤖 **AI 3D Asset Pipeline:** Eksperimentisanje sa generativnim AI alatima (Rodin-3D, DINOv3) za kreiranje i integraciju .glb fajlova u web aplikacije.'
        ],
        'Languages': 'Jezici',
        'jezici': [
            '● Bosanski (Maternji)',
            '● Engleski (Nivo C1)',
            '● Njemački (Osnove)'
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
        'subtitle': 'IT-Spezialist | Support & Automatisierung',
        'description': 'IT-Experte mit über 10 Jahren Erfahrung in der Systemadministration und technischem Support. Derzeit fokussiert auf die Optimierung von IT-Abläufe durch DevOps-Praktiken und KI-Automatisierung zur Steigerung der Arbeitseffizienz.',
        'contact_me': '✉️ Kontaktieren Sie mich',
        'download_cv': '⬇️ CV herunterladen',
        'Skills': 'Technische Fähigkeiten',
        'experience': [
            '● **Programmierung & Frameworks:** Python (Advanced), TypeScript, React, Vite, Tailwind CSS, C#, JavaScript/jQuery, Grundlegende Programmierung.',
            '● **KI & Automatisierung:** LLM-Integration (Gemini API, Ollama), Multi-Agenten-Systeme (AutoGen, Aider), Google Cloud API, PowerPoint VBA-Automatisierung.',
            '● **DevOps & Cloud:** Docker, Linux (Ubuntu/Debian), CI-CD-Pipelines, Web-Hosting-Administration, Mac OS.',
            '● **Virtualisierung & Infrastruktur:** VMware, Hyper-V, VirtualBox (Multi-OS-Umgebungen).',
            '● **Systemadministration:** Active Directory, G Suite Admin, Betriebssystemadministration, Konfiguration von Netzwerk- und Sicherheitsgeräten, Hardware- und Softwarewartung, Netzwerküberwachung.',
            '● **Spezialisierte Tools:** MS Office, Google Suite, Photoshop, Joomla (K2), 3D-Modellierung (Rodin-3D, ComfyUI, .glb), QA-Handbuchkurs.'
        ],
        'Education': 'Die Ausbildung',
        'skills': [
            '• 2008 / 2012 – Technische Mittelschule für Maschinenbau',
            '• Konstrukteur am Computer und an CNC-Maschinen',
        ],
        'Projects': 'Wichtige Projekte',
        'project_list': [
            '🚀 **AI Help Desk Ticketing System:** Entwicklung einer benutzerdefinierten Linux-basierten Ticketing-Anwendung, die mit der Gemini-API für die automatische Antwortgenerierung integriert ist.',
            '🛠️ **Local AI Development Lab:** Aufbau und Optimierung einer lokalen Hochleistungsumgebung mit Ubuntu-VMs, Docker und Ollama für die LLM-Bereitstellung.',
            '🌐 **Web Development Portfolio:** Erstellung moderner Web-Schnittstellen für Unternehmen wie INTESECO mit React und Tailwind CSS.',
            '🤖 **AI 3D Asset Pipeline:** Experimentieren mit generativen KI-Tools (Rodin-3D, DINOv3) zur Erstellung und Integration von .glb-Dateien in Webanwendungen.'
        ],
        'Languages': 'Sprache',
        'jezici': [
            '● Bosnisch (Muttersprache)',
            '● Englisch (Niveau C1)',
            '● Deutsch (Grundlagen)'
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
    st.subheader(texts['subtitle'], anchor=False)
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

# --- Projects ---
st.write("\n")
st.subheader(texts['Projects'], anchor=False)
st.write('\n'.join(texts['project_list']))

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

    # --- Uklonjen st.form blok ---
    # Koristimo 'key' parametar za direktno vezivanje na session_state
    # Kada se koristi st.text_input van forme, podaci se šalju odmah, ali to je OK.
    
    st.text_input(texts['your_name'], key="contact_name")
    st.text_input(texts['your_email'], key="contact_email")
    st.text_area(texts['your_message'], key="contact_message")
    
    # CAPTCHA
    captcha_text = f"{texts['captcha_label']} {st.session_state.captcha_num1} + {st.session_state.captcha_num2}?"
    captcha_response = st.number_input(captcha_text, min_value=0, max_value=100, step=1)
    
    # Obično dugme umjesto form_submit_button
    submit_button = st.button(texts['send'])

    if submit_button:
        name = st.session_state.contact_name
        email = st.session_state.contact_email
        message = st.session_state.contact_message

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
                
                # Clear form (using keys in session_state)
                # Zbog načina na koji widgeti rade sa key, moramo koristiti callback ili rerun da bi se polja ispraznila vizuelno
                # Ali za jednostavnost, postavit ćemo vrijednosti na prazno i uraditi rerun.
                del st.session_state.contact_name
                del st.session_state.contact_email
                del st.session_state.contact_message
                
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
