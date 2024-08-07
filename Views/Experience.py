import streamlit as st
from pathlib import Path
from PIL import Image
from config import assets_dir  # Import assets_dir


# --- BACKGROUND IMAGE ---
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://wallpaperbat.com/img/664560-workplace-wallpaper.jpg");  /* Podesite putanju do lokalne slike */
    background-size: cover;  /* Promijenjeno u 'cover' */
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;  /* Promijenjeno u 'fixed' */
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# Helper function to load and resize images
def load_and_resize_image(image_name, size=(200, 200)):
    image_path = Path(assets_dir) / image_name
    image = Image.open(image_path)
    image.thumbnail(size)
    return image

# Helper function to display the title based on the selected language
def display_title():
    if st.session_state["selected_language"] == "Bosanski":
        st.title("Radno iskustvo")
    elif st.session_state["selected_language"] == "English":
        st.title("Experience")
    elif st.session_state["selected_language"] == "Deutsch":
        st.title("Arbeitserfahrung")

# Display the title
display_title()





# --- EXAMPLE CONTENT ---
putanja_do_logotipa = load_and_resize_image("foreo.png")
col1, col2 = st.columns([1, 3])
col1.image(putanja_do_logotipa, use_column_width=True)
col1.markdown("[F O R E O](http://www.foreo.com)")

if st.session_state["selected_language"] == "Bosanski":
    col2.write("**F O R E O**")
    col2.write("🚧 **IT support specialist**")
    col2.write("11/2021 - Present")
    col2.write(
        """
        - ► Odgovornost za osnovnu podršku korisnicima
        - ► Instalacija i konfiguracija različitih IT softvera i mrežne opreme
        - ► Instalacija i konfiguracija servera
        - ► Upravljanje korisničkim računima, upravljanje IT opremom
        - ► Konfiguracija i korištenje alata za automatizaciju instalacije i konfiguracije IT softvera
        - ► Pisanje dokumentacije i procedura IT sistema
        - ► Pisanje skripti za automatizaciju
        - ► Pružanje pomoći i tehničke podrške korisnicima ERP sistema i razvojnog tima
        - ► Odgovaranje na upite odjela
        - ► E-mail korespondencija
        - ► Druge aktivnosti u skladu sa zahtjevima nadležne osobe i zahtjevima radnog mjesta
        """
    )
elif st.session_state["selected_language"] == "English":
    col2.write("**F O R E O**")
    col2.write("🚧 **IT support specialist**")
    col2.write("11/2021 - Present")
    col2.write(
        """
        - ► Responsibility for basic customer support
        - ► Installation and configuration of various IT software and network equipment
        - ► Installation and configuration servers 
        - ► Management of user accounts, management of IT equipment
        - ► Configuration and use of automation tools for installation and configuration of IT software
        - ► Writing documentation and procedures of IT systems
        - ► Writing automation scripts 
        - ► Providing assistance and technical support to ERP system users and development team
        - ► Answer department inquiries
        - ► E-mail correspondence
        - ► Other activities in accordance with the request of the competent person, and in accordance with the requirements of the workplace
        """
    )
elif st.session_state["selected_language"] == "Deutsch":
    col2.write("**F O R E O**")
    col2.write("🚧 **IT support specialist**")
    col2.write("11/2021 - Present")
    col2.write(
        """
        - ► Verantwortung für grundlegende Kundenbetreuung
        - ► Installation und Konfiguration verschiedener IT-Software und Netzwerkgeräte
        - ► Installation und Konfiguration von Servern 
        - ► Verwaltung von Benutzerkonten, Verwaltung von IT-Geräten
        - ► Konfiguration und Nutzung von Automatisierungswerkzeugen für die Installation und Konfiguration von IT-Software
        - ► Verfassen von Dokumentationen und Verfahren für IT-Systeme
        - ► Schreiben von Automatisierungsskripten
        - ► Bereitstellung von Unterstützung und technischem Support für ERP-Systembenutzer und Entwicklungsteam
        - ► Beantwortung von Anfragen der Abteilung
        - ► E-Mail-Korrespondenz
        - ► Andere Aktivitäten gemäß dem Wunsch der zuständigen Person und den Anforderungen des Arbeitsplatzes
        """
    )

st.markdown("<br><br><br>", unsafe_allow_html=True)


# --- JOB 2 ---
# --- EXAMPLE CONTENT ---
putanja_do_logotipa = load_and_resize_image("logosoft.png")
col1, col2 = st.columns([1, 3])
col1.image(putanja_do_logotipa, use_column_width=True)
col1.markdown("[LOGOSOFT](https://www.logosoft.ba)")


if st.session_state["selected_language"] == "Bosanski":
    col2.write("**LOGOSOFT**")
    col2.write("🚧 **TECHNICAL SUPPORT PROVIDER FOR RESIDENTIAL SUBJECTS**")
    col2.write("10/2020 - 11/2021")
    col2.write(
        """
        - ► Pružanje osnovne tehničke podrške korisnicima usluga (rješavanje problema) s eskalacijom problema na viši nivo.
        - ► Konfigurisanje portova na mrežnim otocima za nove korisnike
        - ► Pozivanje korisnika, posebno u slučaju većih prekida i tehničkih problema
        - ► Unos svih relevantnih podataka korisnika u odgovarajuće baze podataka i aplikacije
        - ► Prodaja usluga stambenim korisnicima i drugih ponuda pružatelja usluga
        - ► Praćenje ispravnog funkcionisanja usluge pružatelja internet usluga
        - ► Praćenje i sprovođenje obaveznog gašenja TV sadržaja
        - ► Pružanje potrebne podrške tehničarima za eksploataciju
        - ► Predlaganje budžeta i praćenje implementacije budžeta
        """
    )
elif st.session_state["selected_language"] == "English":
    col2.write("**LOGOSOFT**")
    col2.write("🚧 **TECHNICAL SUPPORT PROVIDER FOR RESIDENTIAL SUBJECTS**")
    col2.write("10/2020 - 11/2021")
    col2.write(
        """
        - ► Providing primary technical support to service users (problem solving) with problem escalation to higher levels.
        - ► Configuring ports on network islands for new users
        - ► Calling users, especially in case of major outages and technical problems
        - ► Entering all relevant user data into the appropriate databases and applications
        - ► Sale of services for residential users and other offers of providers
        - ► Monitoring the correct functioning of the ISP service
        - ► Monitoring and implementation of mandatory blackout of TV content
        - ► Providing necessary support to technicians for exploitation
        - ► Proposing the budget and monitoring the implementation of the budget
        """
    )
elif st.session_state["selected_language"] == "Deutsch":
    col2.write("**LOGOSOFT**")
    col2.write("🚧 **TECHNICAL SUPPORT PROVIDER FOR RESIDENTIAL SUBJECTS**")
    col2.write("10/2020 - 11/2021")
    col2.write(
        """
        - ► Bereitstellung primärer technischer Unterstützung für Servicenutzer (Problembehebung) mit Eskalation von Problemen auf höhere Ebenen.
        - ► Konfiguration von Ports auf Netzwerkinseln für neue Benutzer
        - ► Anrufen von Benutzern, besonders im Falle größerer Ausfälle und technischer Probleme
        - ► Eingabe aller relevanten Benutzerdaten in die entsprechenden Datenbanken und Anwendungen
        - ► Verkauf von Dienstleistungen für Privatnutzer und anderen Angeboten von Anbietern
        - ► Überwachung der korrekten Funktion des Internetdienstleisters (ISP)
        - ► Überwachung und Umsetzung der obligatorischen Abschaltung von TV-Inhalten
        - ► Bereitstellung notwendiger Unterstützung für Techniker zur Ausnutzung
        - ► Vorschlag des Budgets und Überwachung der Umsetzung des Budgets
        """
    )

st.markdown("<br><br><br>", unsafe_allow_html=True)

# --- JOB 3 ---
# --- EXAMPLE CONTENT ---
putanja_do_logotipa = load_and_resize_image("cms.png")
col1, col2 = st.columns([1, 3])
col1.image(putanja_do_logotipa, use_column_width=True)
col1.markdown("CMS")

if st.session_state["selected_language"] == "Bosanski":
    col2.write("**CAPITAL MARKET SOLUTIONS**")
    col2.write("🚧 **IT SCIENTIST**")
    col2.write("06/2020 - 10/2020")
    col2.write(
        """
        - ► Održavanje IT opreme, video nadzora i mrežne infrastrukture
        - ► Tehnička podrška za zaposlene
        - ► Konfigurisanje internih sistema i VoIP uređaja
        - ► Praćenje cyber sigurnosti
        - ► Uspostavljanje sistema za rad na daljinu
        - ► Kreiranje budžeta, upravljanje troškovima i nabavka opreme
        """
    )
elif st.session_state["selected_language"] == "English":
    col2.write("**CAPITAL MARKET SOLUTIONS**")
    col2.write("🚧 **IT SCIENTIST**")
    col2.write("06/2020 - 10/2020")
    col2.write(
        """
        - ► Maintenance of IT equipment, video surveillance and network infrastructure
        - ► Technical support for employees
        - ► Configuring internal systems and VoIP devices
        - ► Cyber Security Monitoring 
        - ► Establishing a system for remote work
        - ► Creating a budget, managing costs and purchasing equipment
        """
    )
elif st.session_state["selected_language"] == "Deutsch":
    col2.write("**CAPITAL MARKET SOLUTIONS**")
    col2.write("🚧 **IT SCIENTIST**")
    col2.write("06/2020 - 10/2020")
    col2.write(
        """
        - ► Wartung von IT-Geräten, Videosicherheit und Netzwerkinfrastruktur
        - ► Technische Unterstützung für Mitarbeiter
        - ► Konfiguration interner Systeme und VoIP-Geräte
        - ► Überwachung der Cybersicherheit
        - ► Einrichtung eines Systems für die Arbeit im Homeoffice
        - ► Erstellung eines Budgets, Kostenmanagement und Beschaffung von Ausrüstung
        """
    )

st.markdown("<br><br><br>", unsafe_allow_html=True)

# --- JOB 4 ---
# --- EXAMPLE CONTENT ---
putanja_do_logotipa = load_and_resize_image("payten.png")
col1, col2 = st.columns([1, 3])
col1.image(putanja_do_logotipa, use_column_width=True)
col1.markdown("[PAYTEN](https://www.payten.com/en/)")
if st.session_state["selected_language"] == "Bosanski":
    col2.write("**PAYTEN**")
    col2.write("🚧 **HELP DESK POS SUPPORT ASSOCIATE**")
    col2.write("03/2019 - 02/2020")
    col2.write(
        """
        - ► Korespondencija s bankama
        - ► Testiranje
        - ► Podrška za POS uređaje (rješavanje problema vezanih za rad POS terminala)
        - ► Rješavanje prijavljenih problema
        - ► Priprema terminala u vezi s instalacijom i intervencijom
        - ► Podrška za bankomate (ATM)
        """
    )
elif st.session_state["selected_language"] == "English":
    col2.write("**PAYTEN**")
    col2.write("🚧 **HELP DESK POS SUPPORT ASSOCIATE**")
    col2.write("03/2019 - 02/2020")
    col2.write(
        """
        - ► Correspondence with Banks
        - ► Testing
        - ► POS Support (resolving problems related to the operation of POS terminals)
        - ► Solving reported problems
        - ► Preparation of terminals regarding installation and intervention
        - ► ATM Support
        """
    )
elif st.session_state["selected_language"] == "Deutsch":
    col2.write("**PAYTEN**")
    col2.write("🚧 **HELP DESK POS SUPPORT ASSOCIATE**")
    col2.write("03/2019 - 02/2020")
    col2.write(
        """
        - ► Korrespondenz mit Banken
        - ► Testen
        - ► POS-Unterstützung (Lösung von Problemen im Zusammenhang mit dem Betrieb von POS-Terminals)
        - ► Lösung gemeldeter Probleme
        - ► Vorbereitung von Terminals in Bezug auf Installation und Intervention
        - ► Unterstützung für Geldautomaten (ATM)
        """
    )

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Load and resize company logo for PAYTEN
payten_logo = load_and_resize_image("ataco.png")
col1, col2 = st.columns([1, 3])
col1.image(payten_logo, use_column_width=True)
col1.markdown("[A T A C O](https://ataco-bih.com/)")

# --- JOB 5 ---
if st.session_state["selected_language"] == "Bosanski":
    col2.write("**COMMERCIALIST**")
    col2.write("🚧 **ATACO COMMERCE**")
    col2.write("09/2017 - 03/2018")
    col2.write(
        """
        - ► Primanje dnevnog plana dostave i ostalih dnevnih zadataka od dispečera
        - ► Dostava vraćenih proizvoda u skladište u skladu s internim postupkom
        - ► Primanje dnevnog plana dostave i ostalih dnevnih zadataka od dispečera
        - ► Kontrola, brojanje, prikupljanje i utovar robe iz skladišta
        - ► Pregovaranje o novim narudžbama s kupcima
        """
    )
elif st.session_state["selected_language"] == "English":
    col2.write("**COMMERCIALIST**")
    col2.write("🚧 **ATACO COMMERCE**")
    col2.write("09/2017 - 03/2018")
    col2.write(
        """
        - ► Receiving the daily delivery plan and other daily tasks from the dispatcher
        - ► Delivery of returned goods to the warehouse in accordance with the internal procedure
        - ► Receiving the daily delivery plan and other daily tasks from the dispatcher
        - ► Checking, counting, picking up, and loading goods from the warehouse
        - ► Negotiating new orders with customers
        """
    )
elif st.session_state["selected_language"] == "Deutsch":
    col2.write("**COMMERCIALIST**")
    col2.write("🚧 **ATACO COMMERCE**")
    col2.write("09/2017 - 03/2018")
    col2.write(
        """
        - ► Empfang des täglichen Lieferplans und anderer täglicher Aufgaben vom Disponenten
        - ► Rücklieferung der Waren gemäß dem internen Verfahren ins Lager
        - ► Empfang des täglichen Lieferplans und anderer täglicher Aufgaben vom Disponenten
        - ► Kontrolle, Zählung, Aufnahme und Beladung von Waren aus dem Lager
        - ► Verhandlung neuer Bestellungen mit Kunden
        """
    )

st.markdown("<br><br><br>", unsafe_allow_html=True)

# Load and resize company logo for ATACO
ataco_logo = load_and_resize_image("telinvest.png")
col1, col2 = st.columns([1, 3])
col1.image(ataco_logo, use_column_width=True)
col1.markdown("[TELINVEST](https://www.telinvest.ba/)")

# --- JOB 6 ---
if st.session_state["selected_language"] == "English":
    col2.write("**TECHNICAL SUPPORT FOR BUSINESS USERS**")
    col2.write("🚧 **TELINVEST**")
    col2.write("07/2015 - 09/2017")
    col2.write(
        """
        - ► Engaged as an executor for technical support tasks in the premises of BH TELECOM
        - ► Providing primary technical support to business users
        - ► Providing technical support to business users for ADSL, IPTV, mobile networks, POTS, VOIP, HOSTING, Web email services
        - ► Monitoring and reporting of general problems, escalation of problems to a higher level to other services
        - ► Performing the duties of an operator on duty
        - ► Providing necessary support to technicians for exploitation
        - ► Entering all relevant user data into the appropriate databases and applications
        """
    )
elif st.session_state["selected_language"] == "Bosanski":
    col2.write("**TECHNICAL SUPPORT FOR BUSINESS USERS**")
    col2.write("🚧 **TELINVEST**")
    col2.write("07/2015 - 09/2017")
    col2.write(
        """
        - ► Angažiran kao izvršilac tehničkih podrški u prostorijama BH TELECOM-a
        - ► Pružanje osnovne tehničke podrške poslovnim korisnicima
        - ► Pružanje tehničke podrške poslovnim korisnicima za ADSL, IPTV, mobilne mreže, POTS, VOIP, HOSTING, Web email usluge
        - ► Praćenje i prijavljivanje općih problema, eskalacija problema na viši nivo drugim servisima
        - ► Obavljanje dužnosti operatera dežurnog tima
        - ► Pružanje potrebne podrške tehničarima za eksploataciju
        - ► Unos svih relevantnih podataka korisnika u odgovarajuće baze podataka i aplikacije
        """
    )
elif st.session_state["selected_language"] == "Deutsch":
    col2.write("**TECHNICAL SUPPORT FOR BUSINESS USERS**")
    col2.write("🚧 **TELINVEST**")
    col2.write("07/2015 - 09/2017")
    col2.write(
        """
        - ► Engagiert als Ausführender für technische Supportaufgaben in den Räumlichkeiten von BH TELECOM
        - ► Bereitstellung von grundlegender technischer Unterstützung für Geschäftskunden
        - ► Bereitstellung von technischem Support für Geschäftskunden für ADSL, IPTV, Mobilfunknetze, POTS, VOIP, HOSTING, Web-E-Mail-Dienste
        - ► Überwachung und Meldung allgemeiner Probleme, Eskalation von Problemen auf eine höhere Ebene zu anderen Diensten
        - ► Ausführung der Aufgaben eines diensthabenden Operators
        - ► Bereitstellung notwendiger Unterstützung für Techniker zur Ausnutzung
        - ► Eingabe aller relevanten Benutzerdaten in die entsprechenden Datenbanken und Anwendungen
        """
    )

st.markdown("<br><br><br>", unsafe_allow_html=True)

# --- JOB 7 ---
putanja_do_logotipa = load_and_resize_image("bhtelecom.png")
col1, col2 = st.columns([1, 3])
col1.image(putanja_do_logotipa, use_column_width=True)
col1.markdown("[BH Telecom](https://www.bhtelecom.ba)")

if st.session_state["selected_language"] == "Bosanski":
    col2.write("**TECHNICAL SUPPORT FOR RESIDENTIAL USERS**")
    col2.write("🚧 **BH TELECOM SARAJEVO**")
    col2.write("01/2015 - 07/2015")
    col2.write(
        """
        - ► Pružanje osnovne tehničke podrške korisnicima stambenih objekata
        - ► Pružanje tehničke podrške poslovnim korisnicima za ADSL, IPTV, POTS, VOIP
        - ► Pružanje potrebne podrške tehničarima za eksploataciju
        - ► Unos svih relevantnih podataka korisnika u odgovarajuće baze podataka i aplikacije
        """
    )
elif st.session_state["selected_language"] == "English":
    col2.write("**TECHNICAL SUPPORT FOR RESIDENTIAL USERS**")
    col2.write("🚧 **BH TELECOM SARAJEVO**")
    col2.write("01/2015 - 07/2015")
    col2.write(
        """
        - ► Providing primary technical support for Residential users
        - ► Providing technical support to business users for ADSL, IPTV, POTS, VOIP
        - ► Providing necessary support to technicians for exploitation
        - ► Entering all relevant user data into the appropriate databases and applications
        """
    )
elif st.session_state["selected_language"] == "Deutsch":
    col2.write("**TECHNICAL SUPPORT FOR RESIDENTIAL USERS**")
    col2.write("🚧 **BH TELECOM SARAJEVO**")
    col2.write("01/2015 - 07/2015")
    col2.write(
        """
        - ► Bereitstellung von primärer technischer Unterstützung für Privatkunden
        - ► Bereitstellung von technischem Support für Geschäftskunden für ADSL, IPTV, POTS, VOIP
        - ► Bereitstellung notwendiger Unterstützung für Techniker zur Ausnutzung
        - ► Eingabe aller relevanten Benutzerdaten in die entsprechenden Datenbanken und Anwendungen
        """
    )

st.markdown("<br><br><br>", unsafe_allow_html=True)

putanja_do_logotipa = load_and_resize_image("see.png")
col1, col2 = st.columns([1, 3])
col1.image(putanja_do_logotipa, use_column_width=True)
col1.markdown("SEE Contact")

# --- JOB 8 ---
if st.session_state["selected_language"] == "Bosanski":
    col2.write("**TECHNICAL SUPPORT FOR RESIDENTIAL USERS**")
    col2.write("🚧 **SEE CONTACT**")
    col2.write("08/2014 - 12/2014")
    col2.write(
        """
        - ► Angažovan kao izvršitelj za tehničke podrške u prostorijama BH TELECOM-a
        - ► Pružanje osnovne tehničke podrške korisnicima stambenih objekata
        - ► Pružanje tehničke podrške poslovnim korisnicima za ADSL, IPTV, POTS, VOIP
        - ► Pružanje potrebne podrške tehničarima za eksploataciju
        - ► Unos svih relevantnih podataka korisnika u odgovarajuće baze podataka i aplikacije
        """
    )
elif st.session_state["selected_language"] == "English":
    col2.write("**TECHNICAL SUPPORT FOR RESIDENTIAL USERS**")
    col2.write("🚧 **SEE CONTACT**")
    col2.write("08/2014 - 12/2014")
    col2.write(
        """
        - ► Engaged as an executor for technical support tasks in the premises of BH TELECOM
        - ► Providing primary technical support for Residential users
        - ► Providing technical support to business users for ADSL, IPTV, POTS, VOIP
        - ► Providing necessary support to technicians for exploitation
        - ► Entering all relevant user data into the appropriate databases and applications
        """
    )
elif st.session_state["selected_language"] == "Deutsch":
    col2.write("**TECHNICAL SUPPORT FOR RESIDENTIAL USERS**")
    col2.write("🚧 **SEE CONTACT**")
    col2.write("08/2014 - 12/2014")
    col2.write(
        """
        - ► Tätig als Ausführender für technische Supportaufgaben in den Räumlichkeiten von BH TELECOM
        - ► Bereitstellung primärer technischer Unterstützung für Privatkunden
        - ► Bereitstellung von technischem Support für Geschäftskunden für ADSL, IPTV, POTS, VOIP
        - ► Bereitstellung notwendiger Unterstützung für Techniker zur Ausnutzung
        - ► Eingabe aller relevanten Benutzerdaten in die entsprechenden Datenbanken und Anwendungen
        """
    )
