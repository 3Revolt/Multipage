import streamlit as st
from pathlib import Path
from PIL import Image
from config import assets_dir


# --- BACKGROUND IMAGE AND IMPROVED TIMELINE CSS ---
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

/* Poboljšani Timeline dizajn */
.job-wrapper {
    position: relative;
    padding-left: 30px;
    border-left: 3px solid #00FF00; /* Deblja i vidljivija linija */
    margin-left: 15px;
    padding-bottom: 50px;
}

.timeline-dot {
    position: absolute;
    left: -11px; /* Centriranje na liniju */
    top: 0;
    width: 18px;
    height: 18px;
    background-color: #00FF00;
    border-radius: 50%;
    border: 3px solid white;
    box-shadow: 0 0 5px rgba(0,255,0,0.5);
    z-index: 10;
}

/* Uklanjanje linije sa zadnjeg elementa */
.last-job {
    border-left: 3px solid transparent !important;
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

# Helper function to display the title
def display_title():
    if st.session_state["selected_language"] == "Bosanski":
        st.title("Radno iskustvo")
    elif st.session_state["selected_language"] == "English":
        st.title("Experience")
    elif st.session_state["selected_language"] == "Deutsch":
        st.title("Arbeitserfahrung")

display_title()

# --- JOB 1: FZZZ ---
st.markdown('<div class="job-wrapper"><div class="timeline-dot"></div>', unsafe_allow_html=True)
putanja_do_logotipa = load_and_resize_image("fzzz.png")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(putanja_do_logotipa, use_container_width=True)
    st.markdown("[Federalni zavod za zapošljavanje](https://fzzz.ba/)")
with col2:
    if st.session_state["selected_language"] == "Bosanski":
        st.write("**Federalni zavod za zapošljavanje**\n\n🚧 **Referent za tehničku podršku**\n\n02/2024 - Present")
        st.write("- ► Odgovornost za blagovremeno zakonito pravilno i kvalitetno obavljanje poslova\n- ► Administracija baze podataka i informacijskih tehnologija\n- ► Administracija korisnika u Active Directory-u\n- ► Konfiguracija mrežne i sigurnosne opreme\n- ► Implementiranje programskih rješenja za potrebe Zavoda\n- ► Ažuriranje podataka i dokumenata na web portalu\n- ► Nadgledanje ispravnosti radnih stanica\n- ► IT podrška korisnicima, pisanje dokumentacije i skripti\n- ► Implementiranje sigurnosnih mjera\n- ► Pripremanje opreme u sali za sastanke\n- ► Dnevno kontroliranje internet konekcije")
    elif st.session_state["selected_language"] == "English":
        st.write("**Federal Employment Institute**\n\n🚧 **Technical Support Officer**\n\n02/2024 - Present")
        st.write("- ► Responsibility for timely and quality performance\n- ► Database and IT administration\n- ► Active Directory user management\n- ► Network and security equipment configuration\n- ► Software solutions implementation\n- ► Web portal updates\n- ► Workstation monitoring\n- ► IT support and automation scripting\n- ► Security measures implementation\n- ► Meeting room equipment prep\n- ► Daily internet monitoring")
    elif st.session_state["selected_language"] == "Deutsch":
        st.write("**Bundesagentur für Arbeit**\n\n🚧 **Mitarbeiter für Technischen Support**\n\n02/2024 - Present")
        st.write("- ► Verantwortung für qualitativ hochwertige Aufgabenerledigung\n- ► Datenbank- und IT-Verwaltung\n- ► Active Directory Benutzerverwaltung\n- ► Netzwerkkonfiguration\n- ► Implementierung von Softwarelösungen\n- ► Webportal-Aktualisierung\n- ► Überwachung von Arbeitsstationen\n- ► IT-Support und Automatisierungsskripte\n- ► Sicherheitsmaßnahmen\n- ► Besprechungsraum-Vorbereitung\n- ► Internetverbindungskontrolle")
st.markdown('</div>', unsafe_allow_html=True)

# --- JOB 2: FOREO ---
st.markdown('<div class="job-wrapper"><div class="timeline-dot"></div>', unsafe_allow_html=True)
putanja_do_logotipa = load_and_resize_image("foreo.png")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(putanja_do_logotipa, use_container_width=True)
    st.markdown("[F O R E O](http://www.foreo.com)")
with col2:
    if st.session_state["selected_language"] == "Bosanski":
        st.write("**F O R E O**\n\n🚧 **IT support specialist**\n\n11/2021 - 02/2024")
        st.write("- ► Osnovna podrška korisnicima\n- ► Instalacija softvera i mrežne opreme\n- ► Konfiguracija servera\n- ► Upravljanje korisničkim računima i IT opremom\n- ► Automatizacija instalacija\n- ► Pisanje dokumentacije i skripti\n- ► Podrška ERP korisnicima i dev timu")
    elif st.session_state["selected_language"] == "English":
        st.write("**F O R E O**\n\n🚧 **IT support specialist**\n\n11/2021 - 02/2024")
        st.write("- ► Basic customer support\n- ► Software and network equipment installation\n- ► Server configuration\n- ► User account and IT equipment management\n- ► Installation automation\n- ► Documentation and scripts\n- ► ERP and dev team support")
    elif st.session_state["selected_language"] == "Deutsch":
        st.write("**F O R E O**\n\n🚧 **IT support specialist**\n\n11/2021 - 02/2024")
        st.write("- ► Grundlegende Kundenbetreuung\n- ► Installation von Software und Netzwerkgeräten\n- ► Serverkonfiguration\n- ► Benutzer- und IT-Geräteverwaltung\n- ► Automatisierung\n- ► Dokumentation und Skripte\n- ► ERP- und Entwicklerteam-Support")
st.markdown('</div>', unsafe_allow_html=True)

# --- JOB 3: LOGOSOFT ---
st.markdown('<div class="job-wrapper"><div class="timeline-dot"></div>', unsafe_allow_html=True)
putanja_do_logotipa = load_and_resize_image("logosoft.png")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(putanja_do_logotipa, use_container_width=True)
    st.markdown("[LOGOSOFT](https://www.logosoft.ba)")
with col2:
    if st.session_state["selected_language"] == "Bosanski":
        st.write("**LOGOSOFT**\n\n🚧 **TECHNICAL SUPPORT PROVIDER**\n\n10/2020 - 11/2021")
        st.write("- ► Tehnička podrška korisnicima\n- ► Konfigurisanje portova na mrežnim otocima\n- ► Praćenje ispravnosti ISP servisa\n- ► Podrška tehničarima na terenu\n- ► Unos podataka u baze")
    elif st.session_state["selected_language"] == "English":
        st.write("**LOGOSOFT**\n\n🚧 **TECHNICAL SUPPORT PROVIDER**\n\n10/2020 - 11/2021")
        st.write("- ► Technical support to users\n- ► Port configuration on network islands\n- ► ISP service monitoring\n- ► Field technician support\n- ► Data entry")
    elif st.session_state["selected_language"] == "Deutsch":
        st.write("**LOGOSOFT**\n\n🚧 **TECHNICAL SUPPORT PROVIDER**\n\n10/2020 - 11/2021")
        st.write("- ► Technischer Support für Benutzer\n- ► Portkonfiguration\n- ► ISP-Service-Überwachung\n- ► Außendienstunterstützung\n- ► Dateneingabe")
st.markdown('</div>', unsafe_allow_html=True)

# --- JOB 4: CMS ---
st.markdown('<div class="job-wrapper"><div class="timeline-dot"></div>', unsafe_allow_html=True)
putanja_do_logotipa = load_and_resize_image("cms.png")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(putanja_do_logotipa, use_container_width=True)
    st.markdown("CMS")
with col2:
    if st.session_state["selected_language"] == "Bosanski":
        st.write("**CAPITAL MARKET SOLUTIONS**\n\n🚧 **IT SCIENTIST**\n\n06/2020 - 10/2020")
        st.write("- ► Održavanje IT opreme i video nadzora\n- ► Tehnička podrška zaposlenima\n- ► Konfigurisanje VoIP uređaja\n- ► Praćenje cyber sigurnosti\n- ► Sistemi za rad na daljinu")
    elif st.session_state["selected_language"] == "English":
        st.write("**CAPITAL MARKET SOLUTIONS**\n\n🚧 **IT SCIENTIST**\n\n06/2020 - 10/2020")
        st.write("- ► IT equipment and CCTV maintenance\n- ► Employee technical support\n- ► VoIP configuration\n- ► Cyber security monitoring\n- ► Remote work systems")
    elif st.session_state["selected_language"] == "Deutsch":
        st.write("**CAPITAL MARKET SOLUTIONS**\n\n🚧 **IT SCIENTIST**\n\n06/2020 - 10/2020")
        st.write("- ► Wartung von IT-Geräten und Videoüberwachung\n- ► Support für Mitarbeiter\n- ► VoIP-Konfiguration\n- ► Cybersicherheitsüberwachung\n- ► Remote-Work-Systeme")
st.markdown('</div>', unsafe_allow_html=True)

# --- JOB 5: PAYTEN ---
st.markdown('<div class="job-wrapper"><div class="timeline-dot"></div>', unsafe_allow_html=True)
putanja_do_logotipa = load_and_resize_image("payten.png")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(putanja_do_logotipa, use_container_width=True)
    st.markdown("[PAYTEN](https://www.payten.com/en/)")
with col2:
    if st.session_state["selected_language"] == "Bosanski":
        st.write("**PAYTEN**\n\n🚧 **HELP DESK POS SUPPORT**\n\n03/2019 - 02/2020")
        st.write("- ► Podrška za POS uređaje i bankomate\n- ► Korespondencija s bankama\n- ► Testiranje i priprema terminala")
    elif st.session_state["selected_language"] == "English":
        st.write("**PAYTEN**\n\n🚧 **HELP DESK POS SUPPORT**\n\n03/2019 - 02/2020")
        st.write("- ► POS and ATM support\n- ► Bank correspondence\n- ► Terminal testing and prep")
    elif st.session_state["selected_language"] == "Deutsch":
        st.write("**PAYTEN**\n\n🚧 **HELP DESK POS SUPPORT**\n\n03/2019 - 02/2020")
        st.write("- ► POS- und ATM-Support\n- ► Bankkorrespondenz\n- ► Terminal-Tests und Vorbereitung")
st.markdown('</div>', unsafe_allow_html=True)

# --- JOB 6: ATACO ---
st.markdown('<div class="job-wrapper"><div class="timeline-dot"></div>', unsafe_allow_html=True)
payten_logo = load_and_resize_image("ataco.png")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(payten_logo, use_container_width=True)
    st.markdown("[A T A C O](https://ataco-bih.com/)")
with col2:
    if st.session_state["selected_language"] == "Bosanski":
        st.write("**ATACO COMMERCE**\n\n🚧 **KOMERCIJALISTA**\n\n09/2017 - 03/2018")
        st.write("- ► Plan dostave i kontrola robe\n- ► Pregovaranje o narudžbama\n- ► Upravljanje povratima u skladište")
    elif st.session_state["selected_language"] == "English":
        st.write("**ATACO COMMERCE**\n\n🚧 **COMMERCIALIST**\n\n09/2017 - 03/2018")
        st.write("- ► Delivery planning and goods control\n- ► Order negotiation\n- ► Warehouse return management")
    elif st.session_state["selected_language"] == "Deutsch":
        st.write("**ATACO COMMERCE**\n\n🚧 **KAUFMANN**\n\n09/2017 - 03/2018")
        st.write("- ► Lieferplanung und Warenkontrolle\n- ► Auftragsverhandlung\n- ► Lagerrückgabemanagement")
st.markdown('</div>', unsafe_allow_html=True)

# --- JOB 7: TELINVEST ---
st.markdown('<div class="job-wrapper"><div class="timeline-dot"></div>', unsafe_allow_html=True)
ataco_logo = load_and_resize_image("telinvest.png")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(ataco_logo, use_container_width=True)
    st.markdown("[TELINVEST](https://www.telinvest.ba/)")
with col2:
    if st.session_state["selected_language"] == "Bosanski":
        st.write("**TELINVEST (BH Telecom)**\n\n🚧 **TEHNIČKA PODRŠKA (BUSINESS)**\n\n07/2015 - 09/2017")
        st.write("- ► Podrška za ADSL, IPTV, VOIP i hosting usluge\n- ► Praćenje i prijavljivanje općih problema\n- ► Unos korisničkih podataka u baze")
    elif st.session_state["selected_language"] == "English":
        st.write("**TELINVEST (BH Telecom)**\n\n🚧 **TECHNICAL SUPPORT (BUSINESS)**\n\n07/2015 - 09/2017")
        st.write("- ► Support for ADSL, IPTV, VOIP, and hosting services\n- ► General problem monitoring and reporting\n- ► Database entry")
    elif st.session_state["selected_language"] == "Deutsch":
        st.write("**TELINVEST (BH Telecom)**\n\n🚧 **TECHNISCHER SUPPORT (GESCHÄFT)**\n\n07/2015 - 09/2017")
        st.write("- ► Support für ADSL-, IPTV-, VOIP- und Hosting-Dienste\n- ► Überwachung allgemeiner Probleme\n- ► Dateneingabe")
st.markdown('</div>', unsafe_allow_html=True)

# --- JOB 8: BH TELECOM ---
st.markdown('<div class="job-wrapper"><div class="timeline-dot"></div>', unsafe_allow_html=True)
putanja_do_logotipa = load_and_resize_image("bhtelecom.png")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(putanja_do_logotipa, use_container_width=True)
    st.markdown("[BH Telecom](https://www.bhtelecom.ba)")
with col2:
    if st.session_state["selected_language"] == "Bosanski":
        st.write("**BH TELECOM SARAJEVO**\n\n🚧 **TEHNIČKA PODRŠKA (RESIDENTIAL)**\n\n01/2015 - 07/2015")
        st.write("- ► Podrška za ADSL, IPTV, POTS i VOIP usluge\n- ► Podrška tehničarima na terenu\n- ► Unos podataka u baze")
    elif st.session_state["selected_language"] == "English":
        st.write("**BH TELECOM SARAJEVO**\n\n🚧 **TECHNICAL SUPPORT (RESIDENTIAL)**\n\n01/2015 - 07/2015")
        st.write("- ► Support for ADSL, IPTV, POTS, and VOIP\n- ► Support to field technicians\n- ► Data entry")
    elif st.session_state["selected_language"] == "Deutsch":
        st.write("**BH TELECOM SARAJEVO**\n\n🚧 **TECHNISCHER SUPPORT (PRIVAT)**\n\n01/2015 - 07/2015")
        st.write("- ► Support für ADSL, IPTV, POTS und VOIP\n- ► Außendienstunterstützung\n- ► Dateneingabe")
st.markdown('</div>', unsafe_allow_html=True)

# --- JOB 9: SEE CONTACT ---
st.markdown('<div class="job-wrapper last-job"><div class="timeline-dot"></div>', unsafe_allow_html=True)
putanja_do_logotipa = load_and_resize_image("see.png")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(putanja_do_logotipa, use_container_width=True)
    st.markdown("SEE Contact")
with col2:
    if st.session_state["selected_language"] == "Bosanski":
        st.write("**SEE CONTACT (BH Telecom)**\n\n🚧 **TEHNIČKA PODRŠKA**\n\n08/2014 - 12/2014")
        st.write("- ► Pružanje tehničke podrške u prostorijama BH Telecoma\n- ► Podrška za ADSL, IPTV, POTS i VOIP")
    elif st.session_state["selected_language"] == "English":
        st.write("**SEE CONTACT (BH Telecom)**\n\n🚧 **TECHNICAL SUPPORT**\n\n08/2014 - 12/2014")
        st.write("- ► Technical support at BH Telecom premises\n- ► Support for ADSL, IPTV, POTS, and VOIP")
    elif st.session_state["selected_language"] == "Deutsch":
        st.write("**SEE CONTACT (BH Telecom)**\n\n🚧 **TECHNISCHER SUPPORT**\n\n08/2014 - 12/2014")
        st.write("- ► Technischer Support bei BH Telecom\n- ► Support für ADSL, IPTV, POTS und VOIP")
st.markdown('</div>', unsafe_allow_html=True)
