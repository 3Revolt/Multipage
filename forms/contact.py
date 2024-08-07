import re
import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Funkcija za provjeru ispravnosti email adrese
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# Definisanje opcija za jezik
language_options = {
    "Bosanski": "bs",
    "English": "en",
    "Deutsch": "de"
}

# Učitavanje kredencijala i SMTP postavki iz fajla
with open('credentials.txt', 'r') as file:
    sender_email, sender_password, receiver_email, smtp_server, smtp_port = file.read().strip().split(':')

# Pretvaranje SMTP porta u integer
smtp_port = int(smtp_port)

# Izbor jezika
selected_language = st.selectbox("Choose your language", options=list(language_options.keys()))

# Unos email-a i poruke na osnovu odabranog jezika
if selected_language == "Bosanski":
    st.subheader("Kontaktirajte me")
    email = st.text_input("Vaš email")
    message = st.text_area("Vaša poruka")

elif selected_language == "English":
    st.subheader("Contact me")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")

elif selected_language == "Deutsch":
    st.subheader("Kontaktiere mich")
    email = st.text_input("Deine E-Mail")
    message = st.text_area("Deine Nachricht")

# Ako je dugme za slanje pritisnuto
if st.button("Send"):
    if email and message:
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
        else:
            # Prikaz vrtnje dok se poruka šalje
            with st.spinner("Sending your message..."):
                # Kreiranje poruke
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = "Message from CV Website"
                msg.attach(MIMEText(f"Email: {email}\n\nMessage: {message}", 'plain'))

                # Slanje email-a
                try:
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.sendmail(sender_email, receiver_email, msg.as_string())
                    st.success("Message sent successfully!")
                except Exception as e:
                    st.error("An error occurred while sending the message.")
                    print(e)
    else:
        st.error("Please fill in both email and message fields.")