import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

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

# Učitavanje kredencijala i SMTP postavki iz `st.secrets`
try:
    sender_email = st.secrets["email"]["sender_email"]
    sender_password = st.secrets["email"]["sender_password"]
    receiver_email = st.secrets["email"]["receiver_email"]
    smtp_server = st.secrets["email"]["smtp_server"]
    smtp_port = st.secrets["email"]["smtp_port"]
except KeyError as e:
    st.error(f"Missing key in secrets.toml: {e}")
    st.stop()

# Funkcija za slanje emaila
def send_email(name, email, message):
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
        'select_page': 'ABOUT ME'
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
        'select_page': 'O MENI'
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
        'select_page': 'ÜBER MICH'
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
st.markdown(f'## {texts["select_page"]}')

# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("assets/cv.gif", use_column_width=True)

with col2:
    st.title(texts['title'], anchor=False)
    st.write(texts['description'])

    # Dugme za skrolovanje koristeći HTML
    st.markdown(f'<a href="#contact-me" style="text-decoration: none;"><button>{texts["contact_me"]}</button></a>', unsafe_allow_html=True)

    # Dugme za preuzimanje CV-a na osnovu odabranog jezika
    st.download_button(
        label=texts['download_cv'],
        data=open(cv_paths[selected_language], 'rb').read(),
        file_name=f'CV_{selected_language}.pdf',  # Promenjeno ime datoteke
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

# Inicijalizacija session state za praćenje stanja forme
if 'contact_form' not in st.session_state:
    st.session_state.contact_form = {
        'name': '',
        'email': '',
        'message': '',
        'submitted': False,
        'success_message': ''
    }

# Funkcija za prikaz forme
def show_contact_form():
    # Display the contact form
    name = st.text_input(texts['your_name'], value=st.session_state.contact_form['name'])
    email = st.text_input(texts['your_email'], value=st.session_state.contact_form['email'])
    message = st.text_area(texts['your_message'], value=st.session_state.contact_form['message'])
    submit_button = st.button(texts['send'])

    if submit_button:
        if name and email and message:
            if not is_valid_email(email):
                st.error(texts['error_email'])
            else:
                with st.spinner(texts['sending']):
                    if send_email(name, email, message):
                        st.session_state.contact_form['submitted'] = True
                        st.session_state.contact_form['success_message'] = texts['success_message']
                        # Clear the form after successful submission
                        st.session_state.contact_form['name'] = ''
                        st.session_state.contact_form['email'] = ''
                        st.session_state.contact_form['message'] = ''
                    else:
                        st.error(texts['error_message'])
        else:
            st.error(texts['error_fields'])
    
    # If the message is successfully sent, display success message
    if st.session_state.contact_form['submitted']:
        st.success(st.session_state.contact_form['success_message'])
        # Clear the success message and form fields
        st.session_state.contact_form['submitted'] = False
        st.session_state.contact_form['success_message'] = ''

# Prikaz forme
show_contact_form()