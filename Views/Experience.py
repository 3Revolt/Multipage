import streamlit as st
from pathlib import Path
from PIL import Image
from config import assets_dir  # Import assets_dir


# --- BACKGROUND IMAGE AND TIMELINE CSS ---
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
    background-color: rgba(255, 255, 255, 0.9);
    box-shadow: none;
    min-height: 100vh;
}

/* Timeline CSS */
.timeline-container {
    position: relative;
    padding-left: 40px;
    margin-bottom: 20px;
    border-left: 2px solid #00FF00;
}

.timeline-dot {
    position: absolute;
    left: -9px;
    top: 5px;
    width: 16px;
    height: 16px;
    background-color: #00FF00;
    border-radius: 50%;
    border: 2px solid white;
    z-index: 10;
}

.job-card {
    background-color: rgba(255, 255, 255, 0.5);
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #eee;
    margin-bottom: 40px;
}
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

# --- START TIMELINE ---
st.markdown('<div style="margin-left: 20px;">', unsafe_allow_html=True)

# --- Job 1: FZZZ ---
with st.container():
    st.markdown('<div class="timeline-container"><div class="timeline-dot"></div>', unsafe_allow_html=True)
    putanja_do_logotipa = load_and_resize_image("fzzz.png")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(putanja_do_logotipa, use_container_width=True)
        st.markdown("[Federalni zavod za zapošljavanje](https://fzzz.ba/)")
    
    with col2:
        if st.session_state["selected_language"] == "Bosanski":
            st.write("**Federalni zavod za zapošljavanje**")
            st.write("🚧 **Referent za tehničku podršku**")
            st.write("02/2024 - Present")
            st.write("""
                - ► Odgovornost za blagovremeno zakonito pravilno i kvalitetno obavljanje poslova
                - ► Administracija baze podataka i informacijskih tehnologija
                - ► Administracija korisnika u Active Directory-u
                - ► Konfiguracija mrežne i sigurnosne opreme
                - ► Implementiranje programskih rješenja za potrebe Zavoda
                - ► Ažuriranje podataka i dokumenata na web portalu
                - ► Nadgledanje ispravnosti radnih stanica(printera i ostalih multifunkcijskih uređaja)
                - ► IT podrška korisnicima za rad u poslovnom sustavu uključujući nadogranje sustava ovisno o potrebama korisnika
                - ► Pisanje dokumentacije i procedura IT sistema
                - ► Pisanje skripti za automatizaciju
                - ► Identificiranje zahtijeva korisnika i zaprimanje različitih upita kao i pružanje pomoći i otklanjanje kvarova
                - ► Implementiranje sigurnosnih mjera na računarima
                - ► Pripremanje i instalacija opreme u sali za održavanje sastanaka
                - ► Druge aktivnosti u skladu sa zahtjevima nadležne osobe i zahtjevima radnog mjesta
                - ► Dnevno kontroliranje internet konekcije u zavodu
                - ► Obavljanje i drugih poslova po nalogu rukovoditelja jedinice
            """)
        elif st.session_state["selected_language"] == "English":
            st.write("**Federal Employment Institute**")
            st.write("🚧 **Technical Support Officer**")
            st.write("02/2024 - Present")
            st.write("""
                - ► Responsibility for timely, lawful, proper, and quality performance of tasks
                - ► Administration of database and information technologies
                - ► Administration of users in Active Directory
                - ► Configuration of network and security equipment
                - ► Implementation of software solutions for the needs of the Institute
                - ► Updating data and documents on the web portal
                - ► Monitoring the functionality of workstations (printers and other multifunction devices)
                - ► IT support for users working within the business system, including system upgrades based on user needs
                - ► Writing documentation and procedures for the IT system
                - ► Writing scripts for automation
                - ► Identifying user requirements, receiving various inquiries, providing assistance, and troubleshooting
                - ► Implementing security measures on computer
                - ► Preparing and installing equipment in the meeting room
                - ► Other activities in accordance with the requirements of the supervisor and the job position
                - ► Daily monitoring of the internet connection at the Institute
                - ► Performing other tasks as directed by the unit manager
            """)
        elif st.session_state["selected_language"] == "Deutsch":
            st.write("**Bundesagentur für Arbeit**")
            st.write("🚧 **Mitarbeiter für Technischen Support**")
            st.write("02/2024 - Present")
            st.write("""
                - ► Verantwortung für die rechtzeitige, gesetzmäßige, ordnungsgemäße und qualitativ hochwertige Erledigung der Aufgaben
                - ► Verwaltung von Datenbanken und Informationstechnologien
                - ► Benutzerverwaltung im Active Directory
                - ► Konfiguration von Netzwerk- und Sicherheitsgeräten
                - ► Implementierung von Softwarelösungen für die Bedürfnisse des Instituts
                - ► Aktualisierung von Daten und Dokumenten auf dem Webporta
                - ► Überwachung der Funktionsfähigkeit von Arbeitsstationen (Druckern und anderen Multifunktionsgeräten)
                - ► IT-Support für Benutzer im Geschäftssystem, einschließlich System-Upgrades je nach Benutzeranforderungen
                - ► Erstellung von Dokumentationen und Verfahren für das IT-System
                - ► Schreiben von Skripten zur Automatisierung
                - ► Identifizierung der Benutzeranforderungen, Entgegennahme verschiedener Anfragen, Bereitstellung von Unterstützung und Fehlerbehebung
                - ► Implementierung von Sicherheitsmaßnahmen auf Computern
                - ► Vorbereitung und Installation von Geräten im Besprechungsraum
                - ► Weitere Aktivitäten gemäß den Anforderungen des Vorgesetzten und des Arbeitsplatzes
                - ► Tägliche Überprüfung der Internetverbindung im Institut
                - ► Ausführung weiterer Aufgaben auf Anweisung des Abteilungsleiters
            """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Job 2: FOREO ---
with st.container():
    st.markdown('<div class="timeline-container"><div class="timeline-dot"></div>', unsafe_allow_html=True)
    putanja_do_logotipa = load_and_resize_image("foreo.png")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(putanja_do_logotipa, use_container_width=True)
        st.markdown("[F O R E O](http://www.foreo.com)")
    
    with col2:
        if st.session_state["selected_language"] == "Bosanski":
            st.write("**F O R E O**")
            st.write("🚧 **IT support specialist**")
            st.write("11/2021 - 02/2024")
            st.write("""
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
            """)
        elif st.session_state["selected_language"] == "English":
            st.write("**F O R E O**")
            st.write("🚧 **IT support specialist**")
            st.write("11/2021 - 02/2024")
            st.write("""
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
            """)
        elif st.session_state["selected_language"] == "Deutsch":
            st.write("**F O R E O**")
            st.write("🚧 **IT support specialist**")
            st.write("11/2021 - 02/2024")
            st.write("""
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
            """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Job 3: LOGOSOFT ---
with st.container():
    st.markdown('<div class="timeline-container"><div class="timeline-dot"></div>', unsafe_allow_html=True)
    putanja_do_logotipa = load_and_resize_image("logosoft.png")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(putanja_do_logotipa, use_container_width=True)
        st.markdown("[LOGOSOFT](https://www.logosoft.ba)")
    
    with col2:
        if st.session_state["selected_language"] == "Bosanski":
            st.write("**LOGOSOFT**")
            st.write("🚧 **TECHNICAL SUPPORT PROVIDER FOR RESIDENTIAL SUBJECTS**")
            st.write("10/2020 - 11/2021")
            st.write("""
                - ► Pružanje osnovne tehničke podrške korisnicima usluga (rješavanje problema) s eskalacijom problema na viši nivo.
                - ► Konfigurisanje portova na mrežnim otocima za nove korisnike
                - ► Pozivanje korisnika, posebno u slučaju većih prekida i tehničkih problema
                - ► Unos svih relevantnih podataka korisnika u odgovarajuće baze podataka i aplikacije
                - ► Prodaja usluga stambenim korisnicima i drugih ponuda pružatelja usluga
                - ► Praćenje ispravnog funkcionisanja usluge pružatelja internet usluga
                - ► Praćenje i sprovođenje obaveznog gašenja TV sadržaja
                - ► Pružanje potrebne podrške tehničarima za eksploataciju
                - ► Predlaganje budžeta i praćenje implementacije budžeta
            """)
        elif st.session_state["selected_language"] == "English":
            st.write("**LOGOSOFT**")
            st.write("🚧 **TECHNICAL SUPPORT PROVIDER FOR RESIDENTIAL SUBJECTS**")
            st.write("10/2020 - 11/2021")
            st.write("""
                - ► Providing primary technical support to service users (problem solving) with problem escalation to higher levels.
                - ► Configuring ports on network islands for new users
                - ► Calling users, especially in case of major outages and technical problems
                - ► Entering all relevant user data into the appropriate databases and applications
                - ► Sale of services for residential users and other offers of providers
                - ► Monitoring the correct functioning of the ISP service
                - ► Monitoring and implementation of mandatory blackout of TV content
                - ► Providing necessary support to technicians for exploitation
                - ► Proposing the budget and monitoring the implementation of the budget
            """)
        elif st.session_state["selected_language"] == "Deutsch":
            st.write("**LOGOSOFT**")
            st.write("🚧 **TECHNICAL SUPPORT PROVIDER FOR RESIDENTIAL SUBJECTS**")
            st.write("10/2020 - 11/2021")
            st.write("""
                - ► Bereitstellung primärer technischer Unterstützung für Servicenutzer (Problembehebung) mit Eskalation von Problemen auf höhere Ebenen.
                - ► Konfiguration von Ports auf Netzwerkinseln für neue Benutzer
                - ► Anrufen von Benutzern, besonders im Falle größerer Ausfälle und technischer Probleme
                - ► Eingabe aller relevanten Benutzerdaten in die entsprechenden Datenbanken und Anwendungen
                - ► Verkauf von Dienstleistungen für Privatnutzer und anderen Angeboten von Anbietern
                - ► Überwachung der korrekten Funktion des Internetdienstleisters (ISP)
                - ► Überwachung und Umsetzung der obligatorischen Abschaltung von TV-Inhalten
                - ► Bereitstellung notwendiger Unterstützung für Techniker zur Ausnutzung
                - ► Vorschlag des Budgets und Überwachung der Umsetzung des Budgets
            """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Job 4: CMS ---
with st.container():
    st.markdown('<div class="timeline-container"><div class="timeline-dot"></div>', unsafe_allow_html=True)
    putanja_do_logotipa = load_and_resize_image("cms.png")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(putanja_do_logotipa, use_container_width=True)
        st.markdown("CMS")
    
    with col2:
        if st.session_state["selected_language"] == "Bosanski":
            st.write("**CAPITAL MARKET SOLUTIONS**")
            st.write("🚧 **IT SCIENTIST**")
            st.write("06/2020 - 10/2020")
            st.write("""
                - ► Održavanje IT opreme, video nadzora i mrežne infrastrukture
                - ► Tehnička podrška za zaposlene
                - ► Konfigurisanje internih sistema i VoIP uređaja
                - ► Praćenje cyber sigurnosti
                - ► Uspostavljanje sistema za rad na daljinu
                - ► Kreiranje budžeta, upravljanje troškovima i nabavka opreme
            """)
        elif st.session_state["selected_language"] == "English":
            st.write("**CAPITAL MARKET SOLUTIONS**")
            st.write("🚧 **IT SCIENTIST**")
            st.write("06/2020 - 10/2020")
            st.write("""
                - ► Maintenance of IT equipment, video surveillance and network infrastructure
                - ► Technical support for employees
                - ► Configuring internal systems and VoIP devices
                - ► Cyber Security Monitoring 
                - ► Establishing a system for remote work
                - ► Creating a budget, managing costs and purchasing equipment
            """)
        elif st.session_state["selected_language"] == "Deutsch":
            st.write("**CAPITAL MARKET SOLUTIONS**")
            st.write("🚧 **IT SCIENTIST**")
            st.write("06/2020 - 10/2020")
            st.write("""
                - ► Wartung von IT-Geräten, Videosicherheit und Netzwerkinfrastruktur
                - ► Technische Unterstützung für Mitarbeiter
                - ► Konfiguration interner Systeme und VoIP-Geräte
                - ► Überwachung der Cybersicherheit
                - ► Einrichtung eines Systems für die Arbeit im Homeoffice
                - ► Erstellung eines Budgets, Kostenmanagement und Beschaffung von Ausrüstung
            """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Job 5: PAYTEN ---
with st.container():
    st.markdown('<div class="timeline-container"><div class="timeline-dot"></div>', unsafe_allow_html=True)
    putanja_do_logotipa = load_and_resize_image("payten.png")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(putanja_do_logotipa, use_container_width=True)
        st.markdown("[PAYTEN](https://www.payten.com/en/)")
    
    with col2:
        if st.session_state["selected_language"] == "Bosanski":
            st.write("**PAYTEN**")
            st.write("🚧 **HELP DESK POS SUPPORT ASSOCIATE**")
            st.write("03/2019 - 02/2020")
            st.write("""
                - ► Korespondencija s bankama
                - ► Testiranje
                - ► Podrška za POS uređaje (rješavanje problema vezanih za rad POS terminala)
                - ► Rješavanje prijavljenih problema
                - ► Priprema terminala u vezi s instalacijom i intervencijom
                - ► Podrška za bankomate (ATM)
            """)
        elif st.session_state["selected_language"] == "English":
            st.write("**PAYTEN**")
            st.write("🚧 **HELP DESK POS SUPPORT ASSOCIATE**")
            st.write("03/2019 - 02/2020")
            st.write("""
                - ► Correspondence with Banks
                - ► Testing
                - ► POS Support (resolving problems related to the operation of POS terminals)
                - ► Solving reported problems
                - ► Preparation of terminals regarding installation and intervention
                - ► ATM Support
            """)
        elif st.session_state["selected_language"] == "Deutsch":
            st.write("**PAYTEN**")
            st.write("🚧 **HELP DESK POS SUPPORT ASSOCIATE**")
            st.write("03/2019 - 02/2020")
            st.write("""
                - ► Korrespondenz mit Banken
                - ► Testen
                - ► POS-Unterstützung (Lösung von Problemen im Zusammenhang mit dem Betrieb von POS-Terminals)
                - ► Lösung gemeldeter Probleme
                - ► Vorbereitung von Terminals in Bezug auf Installation und Intervention
                - ► Unterstützung für Geldautomaten (ATM)
            """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Job 6: ATACO ---
with st.container():
    st.markdown('<div class="timeline-container"><div class="timeline-dot"></div>', unsafe_allow_html=True)
    payten_logo = load_and_resize_image("ataco.png")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(payten_logo, use_container_width=True)
        st.markdown("[A T A C O](https://ataco-bih.com/)")
    
    with col2:
        if st.session_state["selected_language"] == "Bosanski":
            st.write("**COMMERCIALIST**")
            st.write("🚧 **ATACO COMMERCE**")
            st.write("09/2017 - 03/2018")
            st.write("""
                - ► Primanje dnevnog plana dostave i ostalih dnevnih zadataka od dispečera
                - ► Dostava vraćenih proizvoda u skladište u skladu s internim postupkom
                - ► Primanje dnevnog plana dostave i ostalih dnevnih zadataka od dispečera
                - ► Kontrola, brojanje, prikupljanje i utovar robe iz skladišta
                - ► Pregovaranje o novim narudžbama s kupcima
            """)
        elif st.session_state["selected_language"] == "English":
            st.write("**COMMERCIALIST**")
            st.write("🚧 **ATACO COMMERCE**")
            st.write("09/2017 - 03/2018")
            st.write("""
                - ► Receiving the daily delivery plan and other daily tasks from the dispatcher
                - ► Delivery of returned goods to the warehouse in accordance with the internal procedure
                - ► Receiving the daily delivery plan and other daily tasks from the dispatcher
                - ► Checking, counting, picking up, and loading goods from the warehouse
                - ► Negotiating new orders with customers
            """)
        elif st.session_state["selected_language"] == "Deutsch":
            st.write("**COMMERCIALIST**")
            st.write("🚧 **ATACO COMMERCE**")
            st.write("09/2017 - 03/2018")
            st.write("""
                - ► Empfang des täglichen Lieferplans und anderer täglicher Aufgaben vom Disponenten
                - ► Rücklieferung der Waren gemäß dem internen Verfahren ins Lager
                - ► Empfang des täglichen Lieferplans und anderer täglicher Aufgaben vom Disponenten
                - ► Kontrolle, Zählung, Aufnahme und Beladung von Waren aus dem Lager
                - ► Verhandlung neuer Bestellungen mit Kunden
            """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Job 7: TELINVEST ---
with st.container():
    st.markdown('<div class="timeline-container"><div class="timeline-dot"></div>', unsafe_allow_html=True)
    ataco_logo = load_and_resize_image("telinvest.png")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(ataco_logo, use_container_width=True)
        st.markdown("[TELINVEST](https://www.telinvest.ba/)")
    
    with col2:
        if st.session_state["selected_language"] == "English":
            st.write("**TECHNICAL SUPPORT FOR BUSINESS USERS**")
            st.write("🚧 **TELINVEST**")
            st.write("07/2015 - 09/2017")
            st.write("""
                - ► Engaged as an executor for technical support tasks in the premises of BH TELECOM
                - ► Providing primary technical support to business users
                - ► Providing technical support to business users for ADSL, IPTV, mobile networks, POTS, VOIP, HOSTING, Web email services
                - ► Monitoring and reporting of general problems, escalation of problems to a higher level to other services
                - ► Performing the duties of an operator on duty
                - ► Providing necessary support to technicians for exploitation
                - ► Entering all relevant user data into the appropriate databases and applications
            """)
        elif st.session_state["selected_language"] == "Bosanski":
            st.write("**TECHNICAL SUPPORT FOR BUSINESS USERS**")
            st.write("🚧 **TELINVEST**")
            st.write("07/2015 - 09/2017")
            st.write("""
                - ► Angažiran kao izvršilac tehničkih podrški u prostorijama BH TELECOM-a
                - ► Pružanje osnovne tehničke podrške poslovnim korisnicima
                - ► Pružanje tehničke podrške poslovnim korisnicima za ADSL, IPTV, mobilne mreže, POTS, VOIP, HOSTING, Web email usluge
                - ► Praćenje i prijavljivanje općih problema, eskalacija problema na viši nivo drugim servisima
                - ► Obavljanje dužnosti operatera dežurnog tima
                - ► Pružanje potrebne podrške tehničarima za eksploataciju
                - ► Unos svih relevantnih podataka korisnika u odgovarajuće baze podataka i aplikacije
            """)
        elif st.session_state["selected_language"] == "Deutsch":
            st.write("**TECHNICAL SUPPORT FOR BUSINESS USERS**")
            st.write("🚧 **TELINVEST**")
            st.write("07/2015 - 09/2017")
            st.write("""
                - ► Engagiert als Ausführender für technische Supportaufgaben in den Räumlichkeiten von BH TELECOM
                - ► Bereitstellung von grundlegender technischer Unterstützung für Geschäftskunden
                - ► Bereitstellung von technischem Support für Geschäftskunden für ADSL, IPTV, Mobilfunknetze, POTS, VOIP, HOSTING, Web-E-Mail-Dienste
                - ► Überwachung und Meldung allgemeiner Probleme, Eskalation von Problemen auf eine höhere Ebene zu anderen Diensten
                - ► Ausführung der Aufgaben eines diensthabenden Operators
                - ► Bereitstellung notwendiger Unterstützung für Techniker zur Ausnutzung
                - ► Eingabe aller relevanten Benutzerdaten in die entsprechenden Datenbanken und Anwendungen
            """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Job 8: BH TELECOM ---
with st.container():
    st.markdown('<div class="timeline-container"><div class="timeline-dot"></div>', unsafe_allow_html=True)
    putanja_do_logotipa = load_and_resize_image("bhtelecom.png")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(putanja_do_logotipa, use_container_width=True)
        st.markdown("[BH Telecom](https://www.bhtelecom.ba)")
    
    with col2:
        if st.session_state["selected_language"] == "Bosanski":
            st.write("**TECHNICAL SUPPORT FOR RESIDENTIAL USERS**")
            st.write("🚧 **BH TELECOM SARAJEVO**")
            st.write("01/2015 - 07/2015")
            st.write("""
                - ► Pružanje osnovne tehničke podrške korisnicima stambenih objekata
                - ► Pružanje tehničke podrške poslovnim korisnicima za ADSL, IPTV, POTS, VOIP
                - ► Pružanje potrebne podrške tehničarima za eksploataciju
                - ► Unos svih relevantnih podataka korisnika u odgovarajuće baze podataka i aplikacije
            """)
        elif st.session_state["selected_language"] == "English":
            st.write("**TECHNICAL SUPPORT FOR RESIDENTIAL USERS**")
            st.write("🚧 **BH TELECOM SARAJEVO**")
            st.write("01/2015 - 07/2015")
            st.write("""
                - ► Providing primary technical support for Residential users
                - ► Providing technical support to business users for ADSL, IPTV, POTS, VOIP
                - ► Providing necessary support to technicians for exploitation
                - ► Entering all relevant user data into the appropriate databases and applications
            """)
        elif st.session_state["selected_language"] == "Deutsch":
            st.write("**TECHNICAL SUPPORT FOR RESIDENTIAL USERS**")
            st.write("🚧 **BH TELECOM SARAJEVO**")
            st.write("01/2015 - 07/2015")
            st.write("""
                - ► Bereitstellung von primärer technischer Unterstützung für Privatkunden
                - ► Bereitstellung von technischem Support für Geschäftskunden für ADSL, IPTV, POTS, VOIP
                - ► Bereitstellung notwendiger Unterstützung für Techniker zur Ausnutzung
                - ► Eingabe aller relevanten Benutzerdaten in die entsprechenden Datenbanken und Anwendungen
            """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Job 9: SEE CONTACT ---
with st.container():
    st.markdown('<div class="timeline-container" style="border-left: none;"><div class="timeline-dot"></div>', unsafe_allow_html=True)
    putanja_do_logotipa = load_and_resize_image("see.png")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(putanja_do_logotipa, use_container_width=True)
        st.markdown("SEE Contact")
    
    with col2:
        if st.session_state["selected_language"] == "Bosanski":
            st.write("**TECHNICAL SUPPORT FOR RESIDENTIAL USERS**")
            st.write("🚧 **SEE CONTACT**")
            st.write("08/2014 - 12/2014")
            st.write("""
                - ► Angažovan kao izvršitelj za tehničke podrške u prostorijama BH TELECOM-a
                - ► Pružanje osnovne tehničke podrške korisnicima stambenih objekata
                - ► Pružanje tehničke podrške poslovnim korisnicima za ADSL, IPTV, POTS, VOIP
                - ► Pružanje potrebne podrške tehničarima za eksploataciju
                - ► Unos svih relevantnih podataka korisnika u odgovarajuće baze podataka i aplikacije
            """)
        elif st.session_state["selected_language"] == "English":
            st.write("**TECHNICAL SUPPORT FOR RESIDENTIAL USERS**")
            st.write("🚧 **SEE CONTACT**")
            st.write("08/2014 - 12/2014")
            st.write("""
                - ► Engaged as an executor for technical support tasks in the premises of BH TELECOM
                - ► Providing primary technical support for Residential users
                - ► Providing technical support to business users for ADSL, IPTV, POTS, VOIP
                - ► Providing necessary support to technicians for exploitation
                - ► Entering all relevant user data into the appropriate databases and applications
            """)
        elif st.session_state["selected_language"] == "Deutsch":
            st.write("**TECHNICAL SUPPORT FOR RESIDENTIAL USERS**")
            st.write("🚧 **SEE CONTACT**")
            st.write("08/2014 - 12/2014")
            st.write("""
                - ► Tätig als Ausführender für technische Supportaufgaben in den Räumlichkeiten von BH TELECOM
                - ► Bereitstellung primärer technischer Unterstützung für Privatkunden
                - ► Bereitstellung von technischem Support für Geschäftskunden für ADSL, IPTV, POTS, VOIP
                - ► Bereitstellung notwendiger Unterstützung für Techniker zur Ausnutzung
                - ► Eingabe aller relevanten Benutzerdaten in die entsprechenden Datenbanken und Anwendungen
            """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
