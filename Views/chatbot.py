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
.stChatMessage {
    background-color: rgba(255,255,255, 0.8);
    border-radius: 10px;
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
        "current_job": "Federal Employment Institute (Federalni zavod za zapošljavanje) as Technical Support Officer (Referent za tehničku podršku).",
        "interests": "DevOps, Docker, CI/CD, System Administration, Automation."
    },
    "jobs": [
        {
            "company": "Federalni zavod za zapošljavanje (Federal Employment Institute)",
            "period": "02/2024 - Present",
            "role_bs": "Referent za tehničku podršku",
            "role_en": "Technical Support Officer",
            "role_de": "Mitarbeiter für Technischen Support",
            "details_bs": "Administracija baze podataka, Active Directory, mrežna i sigurnosna oprema, IT podrška, pisanje dokumentacije, automatizacija.",
            "details_en": "Database administration, Active Directory, network and security equipment, IT support, documentation writing, automation.",
            "details_de": "Datenbankverwaltung, Active Directory, Netzwerk- und Sicherheitsausrüstung, IT-Support, Dokumentationserstellung, Automatisierung."
        },
        {
            "company": "Foreo",
            "period": "11/2021 - 02/2024",
            "role_bs": "IT Support Specialist",
            "role_en": "IT Support Specialist",
            "role_de": "IT-Support-Spezialist",
            "details_bs": "Instalacija servera, konfiguracija mrežne opreme, automatizacija, ERP podrška.",
            "details_en": "Server installation, network configuration, automation, ERP support.",
            "details_de": "Serverinstallation, Netzwerkkonfiguration, Automatisierung, ERP-Support."
        },
        {
            "company": "Logosoft",
            "period": "10/2020 - 11/2021",
            "role_bs": "Tehnička podrška (Rezidencijalni)",
            "role_en": "Technical Support Provider",
            "role_de": "Technischer Support-Anbieter",
            "details_bs": "Podrška korisnicima, konfiguracija portova, praćenje servisa.",
            "details_en": "User support, port configuration, service monitoring.",
            "details_de": "Benutzerunterstützung, Portkonfiguration, Serviceüberwachung."
        },
        {
            "company": "Capital Market Solutions (CMS)",
            "period": "06/2020 - 10/2020",
            "role_bs": "IT Scientist",
            "role_en": "IT Scientist",
            "role_de": "Informatiker",
            "details_bs": "Održavanje IT opreme, Cyber Security, VoIP.",
            "details_en": "IT equipment maintenance, Cyber Security, VoIP.",
            "details_de": "Wartung von IT-Geräten, Cyber-Sicherheit, VoIP."
        },
        {
            "company": "Payten",
            "period": "03/2019 - 02/2020",
            "role_bs": "Podrška za POS i ATM",
            "role_en": "POS & ATM Support",
            "role_de": "POS & ATM Unterstützung",
            "details_bs": "Podrška za POS terminale i bankomate.",
            "details_en": "Support for POS terminals and ATMs.",
            "details_de": "Unterstützung für POS-Terminals und Geldautomaten."
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
            "details_bs": "Podrška poslovnim korisnicima (ADSL, IPTV, VOIP).",
            "details_en": "Business user support (ADSL, IPTV, VOIP).",
            "details_de": "Geschäftskunden-Support (ADSL, IPTV, VOIP)."
        },
        {
            "company": "BH Telecom",
            "period": "01/2015 - 07/2015",
            "role_bs": "Tehnička podrška",
            "role_en": "Technical Support",
            "role_de": "Technischer Support",
            "details_bs": "Podrška rezidencijalnim korisnicima.",
            "details_en": "Residential user support.",
            "details_de": "Privatkunden-Support."
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
    "skills": ["Python", "C#", "Docker", "Linux", "Windows Server", "Active Directory", "VMware", "Hyper-V", "Networking", "DevOps"],
    "languages": ["Bosnian (Native)", "English (C1)", "German (Basic)"]
}

# --- HELPER FUNCTIONS ---

def detect_language(text):
    text = text.lower()
    # Simple heuristic
    de_words = ["hallo", "wie", "arbeit", "jahr", "wann", "wo", "danke", "bitte", "lebenslauf", "sprache", "was", "ist", "dein"]
    bs_words = ["zdravo", "kako", "posao", "rad", "godina", "gdje", "hvala", "molim", "iskustvo", "jezik", "šta", "koji", "tvoj"]
    
    score_de = sum(1 for w in de_words if w in text)
    score_bs = sum(1 for w in bs_words if w in text)
    
    if score_de > score_bs:
        return "de"
    elif score_bs > score_de:
        return "bs"
    # Default to English if ambiguous, or if specific english words are present
    return "en"

def get_job_info(query, lang):
    query = query.lower()
    best_match = None
    
    # Normalize query for company names
    companies = {
        "federal": CV_CONTEXT["jobs"][0], "fzzz": CV_CONTEXT["jobs"][0], "employment": CV_CONTEXT["jobs"][0],
        "foreo": CV_CONTEXT["jobs"][1],
        "logosoft": CV_CONTEXT["jobs"][2],
        "cms": CV_CONTEXT["jobs"][3], "capital": CV_CONTEXT["jobs"][3],
        "payten": CV_CONTEXT["jobs"][4],
        "ataco": CV_CONTEXT["jobs"][5],
        "telinvest": CV_CONTEXT["jobs"][6],
        "bh telecom": CV_CONTEXT["jobs"][7], "telecom": CV_CONTEXT["jobs"][7],
        "see contact": CV_CONTEXT["jobs"][8]
    }
    
    for key, job in companies.items():
        if key in query:
            return job
            
    return None

def generate_smart_response(prompt):
    # 1. Detect Language
    lang = detect_language(prompt)
    prompt_lower = prompt.lower()
    
    # 2. Check for "Who are you" / "Name"
    if any(x in prompt_lower for x in ["name", "who are you", "ime", "zoveš", "wer bist du", "heißt"]):
        if lang == "bs": return f"Ja sam {CV_CONTEXT['personal']['name']}, {CV_CONTEXT['personal']['role']}."
        if lang == "de": return f"Ich bin {CV_CONTEXT['personal']['name']}, {CV_CONTEXT['personal']['role']}."
        return f"I am {CV_CONTEXT['personal']['name']}, {CV_CONTEXT['personal']['role']}."

    # 3. Check for "Contact" / "Email"
    if any(x in prompt_lower for x in ["contact", "email", "mail", "kontakt", "reach"]):
        email = CV_CONTEXT['personal']['email']
        if lang == "bs": return f"Možete me kontaktirati putem emaila: {email}."
        if lang == "de": return f"Sie können mich per E-Mail erreichen: {email}."
        return f"You can contact me via email: {email}."

    # 4. Check for Specific Job Queries
    job_match = get_job_info(prompt_lower, lang)
    if job_match:
        # Determine specific question type (When? What? Where?)
        is_time = any(x in prompt_lower for x in ["when", "year", "period", "kada", "godin", "vrijeme", "wann", "jahr", "zeit"])
        is_role = any(x in prompt_lower for x in ["what", "role", "position", "šta", "pozicija", "was", "tätigkeit"])
        
        company = job_match['company']
        period = job_match['period']
        
        if lang == "bs":
            role = job_match['role_bs']
            desc = job_match['details_bs']
            if is_time:
                return f"U kompaniji **{company}** sam radio u periodu: **{period}**."
            return f"U **{company}** ({period}) sam radio kao **{role}**. {desc}"
            
        elif lang == "de":
            role = job_match['role_de']
            desc = job_match['details_de']
            if is_time:
                return f"Ich habe bei **{company}** im Zeitraum **{period}** gearbeitet."
            return f"Bei **{company}** ({period}) war ich als **{role}** tätig. {desc}"
            
        else: # English
            role = job_match['role_en']
            desc = job_match['details_en']
            if is_time:
                return f"I worked at **{company}** during the period: **{period}**."
            return f"At **{company}** ({period}), I worked as a **{role}**. {desc}"

    # 5. Check for "Skills"
    if any(x in prompt_lower for x in ["skill", "vještin", "znanj", "tech", "fähigkeit"]):
        skills = ", ".join(CV_CONTEXT["skills"])
        if lang == "bs": return f"Moje tehničke vještine uključuju: {skills}."
        if lang == "de": return f"Meine Fähigkeiten umfassen: {skills}."
        return f"My technical skills include: {skills}."

    # 6. Current Job
    if any(x in prompt_lower for x in ["current", "now", "today", "trenutno", "sada", "jetzt", "aktuell"]):
        if lang == "bs": return f"Trenutno radim u: {CV_CONTEXT['jobs'][0]['company']}."
        if lang == "de": return f"Derzeit arbeite ich bei: {CV_CONTEXT['jobs'][0]['company']}."
        return f"I am currently working at: {CV_CONTEXT['jobs'][0]['company']}."

    # 7. Fallback / Small Talk
    if lang == "bs":
        return "Hvala na pitanju. Kao AI asistent specijaliziran za ovaj CV, mogu vam reći detalje o radnom iskustvu, vještinama ili kako stupiti u kontakt s Amarom. Šta vas zanima?"
    elif lang == "de":
        return "Danke für die Frage. Als auf diesen Lebenslauf spezialisierter KI-Assistent kann ich Ihnen Details zu Berufserfahrung, Fähigkeiten oder Kontaktmöglichkeiten geben. Woran sind Sie interessiert?"
    else:
        return "Thanks for asking. As an AI assistant specialized for this CV, I can tell you about work experience, skills, or how to contact Amar. What would you like to know?"

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
    # Initial greeting
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I am Amar's virtual assistant. How can I help you today? / Zdravo! Ja sam Amarov virtualni asistent. Kako vam mogu pomoći?"})

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