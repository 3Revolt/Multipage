import streamlit as st
import random
import re
import time

# --- OPENABLE CONFIGURATION (Optional: OpenAI) ---
# Ako korisnik ima OpenAI ključ u secrets.toml, koristiće se.
# U suprotnom, koristi se napredni interni sistem.
OPENAI_AVAILABLE = False
try:
    import openai
    if "openai" in st.secrets and "api_key" in st.secrets["openai"]:
        openai.api_key = st.secrets["openai"]["api_key"]
        OPENAI_AVAILABLE = True
except Exception:
    pass

# --- BACKGROUND IMAGE ---
page_bg_img = """
<style>
body, html {
    margin: 0;
    padding: 0;
    height: 100%;
}
body {
    background-image: url("https://cdn.prod.website-files.com/624629e0591bdc3b300cb644/6594382bbafcb2ef0818295f_VA-HUb%202.png");
    background-size: cover;  
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
[data-testid="stAppViewContainer"] > .main {
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    padding: 20px;
    max-width: 800px;
    margin: auto;
    margin-top: 50px;
}

/* Ciljamo specifično tekst unutar chat poruka */
[data-testid="stChatMessageContent"] {
    color: #000000 !important;
}

[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] div,
[data-testid="stChatMessageContent"] span,
[data-testid="stChatMessageContent"] li {
    color: #000000 !important;
}

/* Pozadina za chat balončiće */
.stChatMessage {
    background-color: rgba(240, 242, 246, 0.95) !important; /* Blago siva pozadina */
    border-radius: 15px;
    border: 1px solid #ddd;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
}

/* User input polje */
.stChatInputContainer {
    padding-bottom: 20px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- INTERNAL KNOWLEDGE BASE (CV DATA) ---
CV_CONTEXT = {
    "personal": {
        "name": "Amar Helać",
        "email": "amar.helac@outlook.com",
        "role": "IT Support Specialist / System Administrator",
        "location": "Bosnia and Herzegovina",
        "current_job": "Federal Employment Institute (Federalni zavod za zapošljavanje) as Technical Support Officer.",
        "about_en": "I have a keen interest in DevOps practices, combining development and IT operations to improve collaboration and productivity. I can integrate Docker into DevOps pipelines, enabling continuous integration and deployment of applications.",
        "about_bs": "Imam veliki interes za prakse u DevOps-u, koje kombinuju razvoj i IT operacije radi poboljšanja suradnje i produktivnosti. Mogu integrisati Docker u DevOps tokove rada.",
        "about_de": "Ich habe ein starkes Interesse an DevOps-Praktiken, die Entwicklung und IT-Operationen kombinieren, um die Zusammenarbeit und Produktivität zu verbessern."
    },
    "education": {
        "school_en": "Secondary mechanical technical school (2008-2012) - Constructor on computer and CNC machines. QA Manual course.",
        "school_bs": "Srednja mašinska tehnička škola (2008-2012) - Konstruktor na računaru i CNC mašinama. QA Manual kurs.",
        "school_de": "Technische Mittelschule für Maschinenbau (2008-2012) - Konstrukteur am Computer und an CNC-Maschinen. QA-Handbuchkurs."
    },
    "jobs": [
        {
            "company": "Federalni zavod za zapošljavanje (Federal Employment Institute)",
            "period": "02/2024 - Present",
            "role_bs": "Referent za tehničku podršku",
            "role_en": "Technical Support Officer",
            "role_de": "Mitarbeiter für Technischen Support",
            "details_bs": """
- Administracija baze podataka i informacijskih tehnologija
- Administracija korisnika u Active Directory-u
- Konfiguracija mrežne i sigurnosne opreme
- Implementiranje programskih rješenja za potrebe Zavoda
- Ažuriranje podataka i dokumenata na web portalu
- Nadgledanje ispravnosti radnih stanica (printera i ostalih multifunkcijskih uređaja)
- IT podrška korisnicima, pisanje dokumentacije i skripti za automatizaciju
- Implementiranje sigurnosnih mjera na računarima
""",
            "details_en": """
- Administration of database and information technologies
- Administration of users in Active Directory
- Configuration of network and security equipment
- Implementation of software solutions
- Updating data on the web portal
- Monitoring workstations and printers
- IT support, writing documentation and automation scripts
- Implementing security measures
""",
            "details_de": """
- Verwaltung von Datenbanken und Informationstechnologien
- Benutzerverwaltung im Active Directory
- Konfiguration von Netzwerk- und Sicherheitsgeräten
- Implementierung von Softwarelösungen
- Aktualisierung von Daten auf dem Webportal
- Überwachung von Arbeitsstationen und Druckern
- IT-Support, Erstellung von Dokumentationen und Automatisierungsskripten
- Implementierung von Sicherheitsmaßnahmen
"""
        },
        {
            "company": "Foreo",
            "period": "11/2021 - 02/2024",
            "role_bs": "IT Support Specialist",
            "role_en": "IT Support Specialist",
            "role_de": "IT-Support-Spezialist",
            "details_bs": """
- Instalacija i konfiguracija servera, IT softvera i mrežne opreme
- Upravljanje korisničkim računima i IT opremom
- Automatizacija instalacije i konfiguracije
- Pisanje dokumentacije i skripti za automatizaciju
- Podrška korisnicima ERP sistema i razvojnom timu
""",
            "details_en": """
- Installation and configuration of servers, IT software, and network equipment
- Management of user accounts and IT equipment
- Automation of installation and configuration
- Writing documentation and automation scripts
- Support for ERP system users and development team
""",
            "details_de": """
- Installation und Konfiguration von Servern, Software und Netzwerkgeräten
- Verwaltung von Benutzerkonten und IT-Ausrüstung
- Automatisierung von Installation und Konfiguration
- Erstellung von Dokumentationen und Automatisierungsskripten
- Unterstützung für ERP-Systembenutzer und Entwicklungsteam
"""
        },
        {
            "company": "Logosoft",
            "period": "10/2020 - 11/2021",
            "role_bs": "Tehnička podrška (Rezidencijalni)",
            "role_en": "Technical Support Provider",
            "role_de": "Technischer Support-Anbieter",
            "details_bs": """
- Pružanje tehničke podrške korisnicima (rješavanje problema)
- Konfigurisanje portova na mrežnim otocima
- Praćenje servisa i ispravnog funkcionisanja usluga
- Podrška tehničarima na terenu
""",
            "details_en": """
- Providing technical support to users (troubleshooting)
- Configuring ports on network islands
- Monitoring services and ISP functionality
- Support to field technicians
""",
            "details_de": """
- Bereitstellung technischer Unterstützung für Benutzer (Fehlerbehebung)
- Konfiguration von Ports
- Überwachung von Diensten
- Unterstützung für Außendiensttechniker
"""
        },
        {
            "company": "Capital Market Solutions (CMS)",
            "period": "06/2020 - 10/2020",
            "role_bs": "IT Scientist",
            "role_en": "IT Scientist",
            "role_de": "Informatiker",
            "details_bs": """
- Održavanje IT opreme, video nadzora i mrežne infrastrukture
- Tehnička podrška za zaposlene
- Konfigurisanje internih sistema i VoIP uređaja
- Praćenje cyber sigurnosti
""",
            "details_en": """
- Maintenance of IT equipment, video surveillance, and network infrastructure
- Technical support for employees
- Configuring internal systems and VoIP devices
- Cyber Security monitoring
""",
            "details_de": """
- Wartung von IT-Geräten, Videoüberwachung und Netzwerkinfrastruktur
- Technische Unterstützung für Mitarbeiter
- Konfiguration interner Systeme und VoIP-Geräte
- Überwachung der Cybersicherheit
"""
        },
        {
            "company": "Payten",
            "period": "03/2019 - 02/2020",
            "role_bs": "Podrška za POS i ATM",
            "role_en": "POS & ATM Support",
            "role_de": "POS & ATM Unterstützung",
            "details_bs": "Podrška za POS terminale i bankomate, korespondencija s bankama, testiranje.",
            "details_en": "Support for POS terminals and ATMs, correspondence with banks, testing.",
            "details_de": "Unterstützung für POS-Terminals und Geldautomaten, Korrespondenz mit Banken, Testen."
        },
        {
            "company": "Ataco Commerce",
            "period": "09/2017 - 03/2018",
            "role_bs": "Komercijalista",
            "role_en": "Commercialist",
            "role_de": "Kaufmann",
            "details_bs": "Dostava, kontrola robe, pregovaranje.",
            "details_en": "Delivery, goods control, negotiation.",
            "details_de": "Lieferung, Warenkontrolle, Verhandlung."
        },
        {
            "company": "Telinvest",
            "period": "07/2015 - 09/2017",
            "role_bs": "Tehnička podrška (Business)",
            "role_en": "Technical Support (Business)",
            "role_de": "Technischer Support (Geschäft)",
            "details_bs": "Podrška poslovnim korisnicima (ADSL, IPTV, VOIP, Hosting).",
            "details_en": "Business user support (ADSL, IPTV, VOIP, Hosting).",
            "details_de": "Geschäftskunden-Support (ADSL, IPTV, VOIP, Hosting)."
        },
        {
            "company": "BH Telecom",
            "period": "01/2015 - 07/2015",
            "role_bs": "Tehnička podrška",
            "role_en": "Technical Support",
            "role_de": "Technischer Support",
            "details_bs": "Podrška rezidencijalnim i poslovnim korisnicima.",
            "details_en": "Residential and business user support.",
            "details_de": "Privat- und Geschäftskunden-Support."
        },
        {
            "company": "See Contact",
            "period": "08/2014 - 12/2014",
            "role_bs": "Tehnička podrška",
            "role_en": "Technical Support",
            "role_de": "Technischer Support",
            "details_bs": "Podrška rezidencijalnim korisnicima.",
            "details_en": "Residential user support.",
            "details_de": "Privatkunden-Support."
        }
    ],
    "skills": ["Python", "C#", "Docker", "Linux", "Windows Server", "Active Directory", "VMware", "Hyper-V", "Networking", "DevOps", "Photoshop", "MS Office", "Google Suite"],
    "soft_skills_bs": "Komunikacija, timski rad, rješavanje problema, pregovaranje, organizacija, prilagodljivost.",
    "soft_skills_en": "Communication, teamwork, problem solving, negotiation, organization, adaptability.",
    "soft_skills_de": "Kommunikation, Teamarbeit, Problemlösung, Verhandlung, Organisation, Anpassungsfähigkeit.",
    "languages": ["Bosnian (Native)", "English (C1)", "German (Basic)"]
}

# --- HELPER FUNCTIONS ---

def normalize_text(text):
    """
    Uklanja kvačice i pretvara tekst u mala slova radi lakšeg prepoznavanja.
    npr. "Šta radiš?" -> "sta radis?"
    """
    text = text.lower()
    replacements = {
        'č': 'c', 'ć': 'c', 'š': 's', 'đ': 'd', 'ž': 'z',
        'Č': 'c', 'Ć': 'c', 'Š': 's', 'Đ': 'd', 'Ž': 'z',
        'ä': 'a', 'ö': 'o', 'ü': 'u', 'ß': 'ss'
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text

def detect_language(text):
    """
    Detektuje jezik na osnovu riječi u tekstu.
    Prioritizira sesiju ako je detekcija slaba.
    """
    text = normalize_text(text)
    # Tokenizacija na riječi (word boundary)
    tokens = set(re.findall(r"\\w+", text))
    
    de_words = {"hallo", "wie", "arbeit", "jahr", "wann", "wo", "danke", "bitte", "lebenslauf", "sprache", "was", "ist", "dein", "ich", "bin", "erfahrung", "guten", "tag", "auf", "wiedersehen", "tschuss", "warum"}
    bs_words = {"zdravo", "kako", "posao", "rad", "godina", "gdje", "hvala", "molim", "iskustvo", "jezik", "sta", "koji", "tvoj", "zoves", "ime", "ko", "si", "radno", "znas", "radio", "reci", "mi", "zasto"}
    en_words = {"hello", "how", "work", "year", "when", "where", "thanks", "please", "cv", "resume", "language", "what", "is", "your", "i", "am", "experience", "know", "skills", "tell", "me", "why"}

    score_de = len(tokens.intersection(de_words))
    score_bs = len(tokens.intersection(bs_words))
    score_en = len(tokens.intersection(en_words))
    
    # Ako imamo jasan pogodak
    if score_de > score_bs and score_de > score_en:
        return "de"
    if score_bs > score_de and score_bs > score_en:
        return "bs"
    if score_en > score_de and score_en > score_bs:
        return "en"
        
    # Ako nismo sigurni, koristi jezik iz sesije (ako postoji)
    # Mapping "Bosanski" -> "bs", "English" -> "en", "Deutsch" -> "de"
    session_lang = st.session_state.get("selected_language", "English")
    if session_lang == "Bosanski":
        return "bs"
    elif session_lang == "Deutsch":
        return "de"
    else:
        return "en"

def get_job_info(query, lang):
    query = normalize_text(query)
    
    # Normalize query for company names
    companies = {
        "federal": CV_CONTEXT["jobs"][0], "fzzz": CV_CONTEXT["jobs"][0], "employment": CV_CONTEXT["jobs"][0], "zavod": CV_CONTEXT["jobs"][0],
        "foreo": CV_CONTEXT["jobs"][1],
        "logosoft": CV_CONTEXT["jobs"][2],
        "cms": CV_CONTEXT["jobs"][3], "capital": CV_CONTEXT["jobs"][3],
        "payten": CV_CONTEXT["jobs"][4],
        "ataco": CV_CONTEXT["jobs"][5],
        "telinvest": CV_CONTEXT["jobs"][6],
        "bh telecom": CV_CONTEXT["jobs"][7], "telecom": CV_CONTEXT["jobs"][7], "bhtelecom": CV_CONTEXT["jobs"][7],
        "see contact": CV_CONTEXT["jobs"][8], "see": CV_CONTEXT["jobs"][8]
    }
    
    for key, job in companies.items():
        if key in query:
            return job
            
    return None

def generate_smart_response(prompt):
    # 1. Normalize and Detect Language
    prompt_norm = normalize_text(prompt)
    lang = detect_language(prompt)
    
    # 2. Check for "Who are you" / "Name" / "Intro"
    if any(x in prompt_norm for x in ["name", "who", "ime", "zoves", "zove", "wer", "heiss", "ko si", "predstavi", "intro", "about", "o tebi", "über dich"]):
        if lang == "bs": return f"Ja sam {CV_CONTEXT['personal']['name']}, {CV_CONTEXT['personal']['role']}. {CV_CONTEXT['personal']['about_bs']}"
        if lang == "de": return f"Ich bin {CV_CONTEXT['personal']['name']}, {CV_CONTEXT['personal']['role']}. {CV_CONTEXT['personal']['about_de']}"
        return f"I am {CV_CONTEXT['personal']['name']}, {CV_CONTEXT['personal']['role']}. {CV_CONTEXT['personal']['about_en']}"

    # 3. Check for "Contact" / "Email" / "Location"
    if any(x in prompt_norm for x in ["contact", "email", "mail", "kontakt", "reach", "javi", "pisi", "telefon", "phone", "nummer", "broj"]):
        email = CV_CONTEXT['personal']['email']
        if lang == "bs": 
            return f"Možete me kontaktirati direktno putem emaila: **{email}**.\n\nTakođer, možete popuniti **[kontakt formu na početnoj stranici 'O meni'](/#contact-me)**."
        if lang == "de": 
            return f"Sie können mich direkt per E-Mail erreichen: **{email}**.\n\nAlternativ können Sie das **[Kontaktformular auf der Startseite 'Über mich'](/#contact-me)** ausfüllen."
        return f"You can contact me directly via email: **{email}**.\n\nAlternatively, you can fill out the **[contact form on the 'About Me' home page](/#contact-me)**."

    # Location / Relocation
    if any(x in prompt_norm for x in ["where", "live", "location", "relocate", "move", "gdje", "zivis", "lokacija", "preseli", "wo", "wohnst", "ort", "umzieh"]):
        loc = CV_CONTEXT['personal']['location']
        if lang == "bs": return f"Trenutno živim u **{loc}**. Za pitanja o preseljenju ili radu na daljinu, molim vas kontaktirajte me direktno."
        if lang == "de": return f"Ich lebe derzeit in **{loc}**. Bei Fragen zu Umzug oder Remote-Arbeit kontaktieren Sie mich bitte direkt."
        return f"I currently live in **{loc}**. For questions about relocation or remote work, please contact me directly."

    # 4. Check for Specific Job Queries
    job_match = get_job_info(prompt_norm, lang)
    if job_match:
        # Determine specific question type (When? What? Where?)
        is_time = any(x in prompt_norm for x in ["when", "year", "period", "kada", "godin", "vrijeme", "wann", "jahr", "zeit", "how long", "dugo"])
        
        company = job_match['company']
        period = job_match['period']
        
        if lang == "bs":
            role = job_match['role_bs']
            desc = job_match['details_bs']
            if is_time:
                return f"U kompaniji **{company}** sam radio u periodu: **{period}**."
            return f"U **{company}** ({period}) sam radio kao **{role}**.\n\nKljučne odgovornosti:\n{desc}"
            
        elif lang == "de":
            role = job_match['role_de']
            desc = job_match['details_de']
            if is_time:
                return f"Ich habe bei **{company}** im Zeitraum **{period}** gearbeitet."
            return f"Bei **{company}** ({period}) war ich als **{role}** tätig.\n\nHauptaufgaben:\n{desc}"
            
        else: # English
            role = job_match['role_en']
            desc = job_match['details_en']
            if is_time:
                return f"I worked at **{company}** during the period: **{period}**."
            return f"At **{company}** ({period}), I worked as a **{role}**.\n\nKey responsibilities:\n{desc}"

    # 5. General Experience / Work History
    if any(x in prompt_norm for x in ["experience", "work", "history", "jobs", "companies", "iskustvo", "rad", "posao", "firm", "erfahrung", "arbeit", "unternehmen"]):
        # List recent jobs
        jobs_list = CV_CONTEXT['jobs'][:3] # Show top 3
        if lang == "bs":
            response = "Moje radno iskustvo uključuje:\n\n"
            for job in jobs_list:
                response += f"- **{job['company']}** ({job['period']}): {job['role_bs']}\n"
            response += "\nZa detalje o specifičnoj firmi, slobodno pitajte (npr. 'Šta si radio u Foreo?')."
            return response
        elif lang == "de":
            response = "Meine Berufserfahrung umfasst:\n\n"
            for job in jobs_list:
                response += f"- **{job['company']}** ({job['period']}): {job['role_de']}\n"
            response += "\nFür Details zu einer bestimmten Firma fragen Sie einfach (z. B. 'Was hast du bei Foreo gemacht?')."
            return response
        else:
            response = "My work experience includes:\n\n"
            for job in jobs_list:
                response += f"- **{job['company']}** ({job['period']}): {job['role_en']}\n"
            response += "\nFor details about a specific company, feel free to ask (e.g. 'What did you do at Foreo?')."
            return response

    # 6. Check for "Skills" (Technical & Soft)
    if any(x in prompt_norm for x in ["skill", "vjestin", "znanj", "tech", "fahigkeit", "znas", "stack"]):
        skills = ", ".join(CV_CONTEXT["skills"])
        if lang == "bs": 
            return f"**Tehničke vještine:** {skills}.\n\n**Soft Skills:** {CV_CONTEXT['soft_skills_bs']}"
        if lang == "de": 
            return f"**Technische Fähigkeiten:** {skills}.\n\n**Soft Skills:** {CV_CONTEXT['soft_skills_de']}"
        return f"**Technical Skills:** {skills}.\n\n**Soft Skills:** {CV_CONTEXT['soft_skills_en']}"

    # 7. Education & Certifications
    if any(x in prompt_norm for x in ["education", "school", "university", "degree", "edukacij", "skol", "obrazovan", "ausbildung", "studium", "schule", "certificat", "kurs", "certifikat"]):
        if lang == "bs": return f"Moje obrazovanje: {CV_CONTEXT['education']['school_bs']}"
        if lang == "de": return f"Meine Ausbildung: {CV_CONTEXT['education']['school_de']}"
        return f"My education: {CV_CONTEXT['education']['school_en']}"

    # 8. Languages
    if any(x in prompt_norm for x in ["language", "german", "english", "speak", "jezik", "njemack", "englesk", "pricas", "sprache", "deutsch", "englisch", "sprechen"]):
        langs = ", ".join(CV_CONTEXT["languages"])
        if lang == "bs": return f"Govorim sljedeće jezike: {langs}."
        if lang == "de": return f"Ich spreche folgende Sprachen: {langs}."
        return f"I speak the following languages: {langs}."

    # 9. "Why Hire You" / Strengths
    if any(x in prompt_norm for x in ["why", "hire", "strong", "strength", "zasto", "zaposli", "snaga", "jaca", "warum", "einstell", "stark"]):
        if lang == "bs": return "Posjedujem kombinaciju tehničkog znanja (Sistemska administracija, DevOps) i iskustva u podršci korisnicima. Brzo učim, prilagodljiv sam i imam dokazano iskustvo u rješavanju kompleksnih problema u različitim IT okruženjima."
        if lang == "de": return "Ich verfüge über eine Kombination aus technischem Wissen (Systemadministration, DevOps) und Erfahrung im Kundensupport. Ich lerne schnell, bin anpassungsfähig und habe nachweisliche Erfahrung in der Lösung komplexer Probleme in verschiedenen IT-Umgebungen."
        return "I possess a combination of technical knowledge (System Administration, DevOps) and experience in customer support. I am a fast learner, adaptable, and have proven experience in solving complex problems in various IT environments."

    # 10. Current Job
    if any(x in prompt_norm for x in ["current", "now", "today", "trenutno", "sada", "jetzt", "aktuell"]):
        if lang == "bs": return f"Trenutno radim u: {CV_CONTEXT['jobs'][0]['company']}."
        if lang == "de": return f"Derzeit arbeite ich bei: {CV_CONTEXT['jobs'][0]['company']}."
        return f"I am currently working at: {CV_CONTEXT['jobs'][0]['company']}."

    # 11. Salary / Availability
    if any(x in prompt_norm for x in ["salary", "pay", "money", "plata", "novac", "gehalt", "bezahl", "available", "dostupan", "verfugbar", "when start", "kada poceti", "wann anfangen"]):
         if lang == "bs": return "Za pitanja o plaći i dostupnosti, molim vas da me kontaktirate direktno putem emaila."
         if lang == "de": return "Für Fragen zu Gehalt und Verfügbarkeit kontaktieren Sie mich bitte direkt per E-Mail."
         return "For questions regarding salary and availability, please contact me directly via email."

    # 12. Fallback / Small Talk
    if lang == "bs":
        return "Hvala na pitanju. Kao AI asistent specijaliziran za ovaj CV, mogu vam reći detalje o radnom iskustvu, vještinama, edukaciji ili kako stupiti u kontakt s Amarom. Šta vas zanima?"
    elif lang == "de":
        return "Danke für die Frage. Als auf diesen Lebenslauf spezialisierter KI-Assistent kann ich Ihnen Details zu Berufserfahrung, Fähigkeiten, Ausbildung oder Kontaktmöglichkeiten geben. Woran sind Sie interessiert?"
    else:
        return "Thanks for asking. As an AI assistant specialized for this CV, I can tell you about work experience, skills, education, or how to contact Amar. What would you like to know?"

# --- OPENAI HANDLER (If key exists) ---
def ask_openai(messages):
    try:
        # Create a system prompt with the CV Context
        system_msg = f"""
        You are a helpful assistant representing Amar Helać. You are answering questions based *strictly* on his CV.
        Here is the CV Context:
        Name: {CV_CONTEXT['personal']['name']}
        Role: {CV_CONTEXT['personal']['role']}
        Skills: {', '.join(CV_CONTEXT['skills'])}
        Languages: {', '.join(CV_CONTEXT['languages'])}
        
        Work Experience:
        """
        for job in CV_CONTEXT['jobs']:
            system_msg += f"- {job['company']} ({job['period']}): {job['role_en']} / {job['details_en']}\n"
            
        system_msg += "\nIf the user asks in Bosnian or German, answer in that language. Be professional, friendly, and concise."
        
        # Prepare API call
        full_messages = [{"role": "system", "content": system_msg}] + messages
        
        if hasattr(openai, "ChatCompletion"):
             response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=full_messages,
                temperature=0.7
            )
             return response.choices[0].message['content']
        else:
            # Fallback for very old versions if any
            return "OpenAI library version mismatch."
            
    except Exception as e:
        return f"Error with AI service: {str(e)}"

# --- MAIN UI ---

st.title("💬 Chat Assistant")
st.markdown("Ask me anything about Amar's experience, skills, or background.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initial greeting based on selected language
    greeting = "Hello! I am Amar's virtual assistant. How can I help you today? / Zdravo! Ja sam Amarov virtualni asistent. Kako vam mogu pomoći?"
    
    current_lang = st.session_state.get("selected_language", "English")
    if current_lang == "Bosanski":
        greeting = "Zdravo! Ja sam Amarov virtualni asistent. Kako vam mogu pomoći? Možete me pitati o mom iskustvu, vještinama ili projektima."
    elif current_lang == "Deutsch":
        greeting = "Hallo! Ich bin Amars virtueller Assistent. Wie kann ich Ihnen heute helfen? Sie können mich nach meiner Erfahrung, meinen Fähigkeiten oder Projekten fragen."
    else:
        greeting = "Hello! I am Amar's virtual assistant. How can I help you today? You can ask me about my experience, skills, or projects."
        
    st.session_state.messages.append({"role": "assistant", "content": greeting})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type your question here..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Simulate thinking for realism
        with st.spinner("Thinking..."):
            time.sleep(0.5) 
            
            if OPENAI_AVAILABLE:
                # Use OpenAI if available
                formatted_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m["role"] != "system"]
                full_response = ask_openai(formatted_history[-5:]) # Send last 5 messages for context
            else:
                # Use Smart Local Logic
                full_response = generate_smart_response(prompt)

        # Typing effect
        displayed_response = ""
        for chunk in full_response.split():
            displayed_response += chunk + " "
            message_placeholder.markdown(displayed_response + "▌")
            time.sleep(0.05)
        message_placeholder.markdown(displayed_response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})