# --- CV DATA (JEDINI IZVOR PODATAKA) ---
# Sve stranice (O meni, Iskustvo, Chat Bot) čitaju podatke odavde.
# Tekstovi su na tri jezika: "bs" (Bosanski), "en" (English), "de" (Deutsch).
# Liste "duties" moraju imati isti broj stavki i isti redoslijed na sva tri jezika.

LANGUAGE_CODES = {"Bosanski": "bs", "English": "en", "Deutsch": "de"}


def lang_code(language_name):
    """'Bosanski' -> 'bs', 'English' -> 'en', 'Deutsch' -> 'de'."""
    return LANGUAGE_CODES.get(language_name, "en")


def tr(value, lang):
    """Vraća prevod ako je vrijednost rječnik po jezicima, inače samu vrijednost."""
    if isinstance(value, dict):
        return value.get(lang) or value.get("en") or next(iter(value.values()))
    return value


PRESENT = {"bs": "Danas", "en": "Present", "de": "Heute"}


def format_period(job, lang):
    """(2024, 2) / None -> '02/2024 - Present'"""
    start = f"{job['start'][1]:02d}/{job['start'][0]}"
    end = f"{job['end'][1]:02d}/{job['end'][0]}" if job["end"] else PRESENT[lang]
    return f"{start} - {end}"


# --- LIČNI PODACI ---
PERSONAL = {
    "name": "Amar Helać",
    "email": "hela3292@hotmail.com",
    "location": {
        "bs": "Sarajevo, Bosna i Hercegovina",
        "en": "Sarajevo, Bosnia and Herzegovina",
        "de": "Sarajevo, Bosnien und Herzegowina",
    },
    "role": {
        "bs": "IT Specijalista | Podrška i automatizacija",
        "en": "IT Specialist | Support & Automation",
        "de": "IT-Spezialist | Support & Automatisierung",
    },
    "description": {
        "bs": "IT profesionalac sa preko 10 godina iskustva u sistemskoj administraciji i tehničkoj podršci. Trenutno fokusiran na unapređenje IT procesa kroz DevOps prakse i AI automatizaciju u svrhu poboljšanja efikasnosti rada.",
        "en": "IT professional with over 10 years of experience in system administration and technical support. Currently focused on improving IT workflows through DevOps practices and AI-driven automation to enhance workplace efficiency.",
        "de": "IT-Experte mit über 10 Jahren Erfahrung in der Systemadministration und technischem Support. Derzeit fokussiert auf die Optimierung von IT-Abläufen durch DevOps-Praktiken und KI-Automatisierung zur Steigerung der Arbeitseffizienz.",
    },
}

SOFT_SKILLS = {
    "bs": ["Komunikacija", "Timski rad", "Rješavanje problema", "Pregovaranje", "Organizacija", "Prilagodljivost"],
    "en": ["Communication", "Teamwork", "Problem solving", "Negotiation", "Organization", "Adaptability"],
    "de": ["Kommunikation", "Teamarbeit", "Problemlösung", "Verhandlung", "Organisation", "Anpassungsfähigkeit"],
}

# --- TEHNIČKE VJEŠTINE (prikaz na stranici "O meni") ---
SKILL_CATEGORIES = [
    {
        "id": "programming",
        "name": {"bs": "Programiranje i Frameworks", "en": "Programming & Frameworks", "de": "Programmierung & Frameworks"},
        "items": {
            "bs": ["Python (Advanced)", "TypeScript", "React", "Vite", "Tailwind CSS", "C#", "JavaScript/jQuery", "Osnove programiranja"],
            "en": ["Python (Advanced)", "TypeScript", "React", "Vite", "Tailwind CSS", "C#", "JavaScript/jQuery", "Basic programming"],
            "de": ["Python (Advanced)", "TypeScript", "React", "Vite", "Tailwind CSS", "C#", "JavaScript/jQuery", "Grundlegende Programmierung"],
        },
    },
    {
        "id": "ai",
        "name": {"bs": "AI i Automatizacija", "en": "AI & Automation", "de": "KI & Automatisierung"},
        "items": {
            "bs": ["LLM integracija (Gemini API, Ollama)", "Multi-agent sistemi (AutoGen, Aider)", "Google Cloud API", "PowerPoint VBA automatizacija"],
            "en": ["LLM integration (Gemini API, Ollama)", "Multi-agent systems (AutoGen, Aider)", "Google Cloud API", "PowerPoint VBA automation"],
            "de": ["LLM-Integration (Gemini API, Ollama)", "Multi-Agenten-Systeme (AutoGen, Aider)", "Google Cloud API", "PowerPoint VBA-Automatisierung"],
        },
    },
    {
        "id": "devops",
        "name": {"bs": "DevOps i Cloud", "en": "DevOps & Cloud", "de": "DevOps & Cloud"},
        "items": {
            "bs": ["Docker", "Linux (Ubuntu/Debian)", "CI/CD pipelines", "Web Hosting administracija", "Mac OS"],
            "en": ["Docker", "Linux (Ubuntu/Debian)", "CI/CD pipelines", "Web Hosting administration", "Mac OS"],
            "de": ["Docker", "Linux (Ubuntu/Debian)", "CI-CD-Pipelines", "Web-Hosting-Administration", "Mac OS"],
        },
    },
    {
        "id": "virtualization",
        "name": {"bs": "Virtualizacija i Infrastruktura", "en": "Virtualization & Infrastructure", "de": "Virtualisierung & Infrastruktur"},
        "items": {
            "bs": ["VMware", "Hyper-V", "VirtualBox (Multi-OS okruženja)"],
            "en": ["VMware", "Hyper-V", "VirtualBox (Multi-OS environments)"],
            "de": ["VMware", "Hyper-V", "VirtualBox (Multi-OS-Umgebungen)"],
        },
    },
    {
        "id": "sysadmin",
        "name": {"bs": "Sistemska Administracija", "en": "System Admin", "de": "Systemadministration"},
        "items": {
            "bs": ["Active Directory", "G Suite Admin", "Administracija OS", "Konfiguracija mrežne i sigurnosne opreme", "Održavanje hardvera i softvera", "Network monitoring"],
            "en": ["Active Directory", "G Suite Admin", "OS Administration", "Network & Security equipment configuration", "Hardware & Software maintenance", "Network Monitoring"],
            "de": ["Active Directory", "G Suite Admin", "Betriebssystemadministration", "Konfiguration von Netzwerk- und Sicherheitsgeräten", "Hardware- und Softwarewartung", "Netzwerküberwachung"],
        },
    },
    {
        "id": "tools",
        "name": {"bs": "Specijalizovani Alati", "en": "Specialized Tools", "de": "Spezialisierte Tools"},
        "items": {
            "bs": ["MS Office", "Google Suite", "Photoshop", "Joomla (K2)", "3D modelovanje (Rodin-3D, ComfyUI, .glb)", "QA Manual kurs"],
            "en": ["MS Office", "Google Suite", "Photoshop", "Joomla (K2)", "3D modeling (Rodin-3D, ComfyUI, .glb)", "QA Manual course"],
            "de": ["MS Office", "Google Suite", "Photoshop", "Joomla (K2)", "3D-Modellierung (Rodin-3D, ComfyUI, .glb)", "QA-Handbuchkurs"],
        },
    },
]


def skill_category_line(category, lang):
    """'● **Naziv:** stavka1, stavka2.' - format koji koristi stranica 'O meni'."""
    return f"● **{tr(category['name'], lang)}:** {', '.join(category['items'][lang])}."


# --- PROJEKTI ---
PROJECTS = [
    {
        "id": "helpdesk",
        "emoji": "🚀",
        "name": {
            "bs": "Help Desk sistem za tikete sa AI integracijom",
            "en": "Help Desk Ticketing System with AI Integration",
            "de": "Help-Desk-Ticketsystem mit KI-Integration",
        },
        "description": {
            "bs": "Razvio i implementirao vlastiti Help Desk sistem za upravljanje tiketima u Linux okruženju, u koji sam integrisao AI funkciju (Gemini API) za automatske prijedloge odgovora na zahtjeve korisnika.",
            "en": "Designed and implemented a custom Linux-based help desk ticketing system and integrated an AI feature (Gemini API) that automatically drafts responses to user requests.",
            "de": "Konzeption und Implementierung eines eigenen Linux-basierten Help-Desk-Ticketsystems mit integrierter KI-Funktion (Gemini API), die automatisch Antwortvorschläge auf Benutzeranfragen erstellt.",
        },
        "tech": ["Linux", "Gemini API", "Python"],
    },
    {
        "id": "ailab",
        "emoji": "🛠️",
        "name": {
            "bs": "Lokalna AI razvojna laboratorija",
            "en": "Local AI Development Lab",
            "de": "Lokales KI-Entwicklungslabor",
        },
        "description": {
            "bs": "Postavio i optimizovao lokalno razvojno okruženje visokih performansi (Ubuntu VM, Docker, Ollama) za pokretanje i testiranje jezičkih modela (LLM) bez oslanjanja na cloud servise.",
            "en": "Set up and optimized a high-performance local development environment (Ubuntu VMs, Docker, Ollama) for running and testing large language models (LLMs) without relying on cloud services.",
            "de": "Aufbau und Optimierung einer leistungsstarken lokalen Entwicklungsumgebung (Ubuntu-VMs, Docker, Ollama) zum Betrieb und Testen von Sprachmodellen (LLMs) ohne Abhängigkeit von Cloud-Diensten.",
        },
        "tech": ["Ubuntu", "Docker", "Ollama", "VMs"],
    },
    {
        "id": "webdev",
        "emoji": "🌐",
        "name": {
            "bs": "Web razvoj za klijente",
            "en": "Client Web Development",
            "de": "Webentwicklung für Kunden",
        },
        "description": {
            "bs": "Dizajnirao i implementirao moderne web interfejse za kompanije poput INTESECO koristeći React i Tailwind CSS.",
            "en": "Designed and built modern web interfaces for companies such as INTESECO using React and Tailwind CSS.",
            "de": "Konzeption und Umsetzung moderner Weboberflächen für Unternehmen wie INTESECO mit React und Tailwind CSS.",
        },
        "tech": ["React", "Tailwind CSS", "TypeScript", "Vite"],
    },
    {
        "id": "3d",
        "emoji": "🤖",
        "name": {
            "bs": "3D pipeline uz generativnu AI",
            "en": "AI-Assisted 3D Asset Pipeline",
            "de": "KI-gestützte 3D-Asset-Pipeline",
        },
        "description": {
            "bs": "Razvio tok rada za kreiranje 3D modela pomoću generativnih AI alata (Rodin-3D, DINOv3) i njihovu integraciju u web aplikacije kao .glb fajlove.",
            "en": "Developed a workflow for creating 3D models with generative AI tools (Rodin-3D, DINOv3) and integrating them into web applications as .glb files.",
            "de": "Entwicklung eines Workflows zur Erstellung von 3D-Modellen mit generativen KI-Tools (Rodin-3D, DINOv3) und deren Integration in Webanwendungen als .glb-Dateien.",
        },
        "tech": ["Rodin-3D", "DINOv3", "ComfyUI", ".glb"],
    },
]


def project_line(project, lang):
    return f"{project['emoji']} **{tr(project['name'], lang)}:** {project['description'][lang]}"


# --- EDUKACIJA ---
EDUCATION = {
    "years": "2008 / 2012",
    "school": {
        "bs": "Srednja mašinska tehnička škola: SMTS",
        "en": "Secondary mechanical technical school",
        "de": "Technische Mittelschule für Maschinenbau",
    },
    "profession": {
        "bs": "Konstruktor na računaru i CNC mašinama",
        "en": "Constructor on the computer and CNC machines",
        "de": "Konstrukteur am Computer und an CNC-Maschinen",
    },
    "courses": {
        "bs": ["QA Manual kurs (ručno testiranje softvera)"],
        "en": ["QA Manual course (manual software testing)"],
        "de": ["QA-Handbuchkurs (manuelles Softwaretesten)"],
    },
}


def education_lines(lang):
    sep = " – " if lang == "de" else " - "
    return [f"• {EDUCATION['years']}{sep}{EDUCATION['school'][lang]}", f"• {EDUCATION['profession'][lang]}"]


# --- JEZICI ---
LANGUAGES = [
    {"id": "bs", "label": {"bs": "Bosanski (Maternji)", "en": "Bosnian (Native)", "de": "Bosnisch (Muttersprache)"}},
    {"id": "en", "label": {"bs": "Engleski (Nivo C1)", "en": "English (Level C1)", "de": "Englisch (Niveau C1)"}},
    {"id": "de", "label": {"bs": "Njemački (Osnove)", "en": "German (Basic)", "de": "Deutsch (Grundlagen)"}},
]

# --- RADNO ISKUSTVO (od najnovijeg prema najstarijem) ---
# header / subheader = dva reda koja se prikazuju pored logotipa na stranici "Iskustvo".
JOBS = [
    {
        "id": "fzzz",
        "company": "Federalni zavod za zapošljavanje",
        "company_name": {
            "bs": "Federalni zavod za zapošljavanje",
            "en": "Federal Employment Institute (Federalni zavod za zapošljavanje)",
            "de": "Föderales Arbeitsamt (Federalni zavod za zapošljavanje)",
        },
        "logo": "fzzz.png",
        "logo_caption": "[Federalni zavod za zapošljavanje](https://fzzz.ba/)",
        "url": "https://fzzz.ba/",
        "start": (2024, 2),
        "end": None,
        "header": {
            "bs": "Federalni zavod za zapošljavanje",
            "en": "Federal Employment Institute",
            "de": "Föderales Arbeitsamt (FZZZ)",
        },
        "subheader": {
            "bs": "Referent za tehničku podršku",
            "en": "Technical Support Officer",
            "de": "Mitarbeiter für Technischen Support",
        },
        "sector": {"bs": "javni sektor", "en": "public sector", "de": "öffentlicher Sektor"},
        "aliases": ["fzzz", "zavod*", "federaln*", "federal", "employment institute", "arbeitsamt", "zzz"],
        "duties": {
            "bs": [
                "Odgovornost za blagovremeno zakonito pravilno i kvalitetno obavljanje poslova",
                "Administracija baze podataka i informacijskih tehnologija",
                "Administracija korisnika u Active Directory-u",
                "Konfiguracija mrežne i sigurnosne opreme",
                "Implementiranje programskih rješenja za potrebe Zavoda",
                "Ažuriranje podataka i dokumenata na web portalu",
                "Nadgledanje ispravnosti radnih stanica (printera i ostalih multifunkcijskih uređaja)",
                "IT podrška korisnicima za rad u poslovnom sustavu uključujući nadogradnje sustava ovisno o potrebama korisnika",
                "Pisanje dokumentacije i procedura IT sistema",
                "Pisanje skripti za automatizaciju",
                "Identificiranje zahtjeva korisnika i zaprimanje različitih upita kao i pružanje pomoći i otklanjanje kvarova",
                "Implementiranje sigurnosnih mjera na računarima",
                "Pripremanje i instalacija opreme u sali za održavanje sastanaka",
                "Druge aktivnosti u skladu sa zahtjevima nadležne osobe i zahtjevima radnog mjesta",
                "Dnevno kontroliranje internet konekcije u zavodu",
                "Obavljanje i drugih poslova po nalogu rukovoditelja jedinice",
            ],
            "en": [
                "Responsibility for timely, lawful, proper, and quality performance of tasks",
                "Administration of database and information technologies",
                "Administration of users in Active Directory",
                "Configuration of network and security equipment",
                "Implementation of software solutions for the needs of the Institute",
                "Updating data and documents on the web portal",
                "Monitoring the functionality of workstations (printers and other multifunction devices)",
                "IT support for users working within the business system, including system upgrades based on user needs",
                "Writing documentation and procedures for the IT system",
                "Writing scripts for automation",
                "Identifying user requirements, receiving various inquiries, providing assistance, and troubleshooting",
                "Implementing security measures on computers",
                "Preparing and installing equipment in the meeting room",
                "Other activities in accordance with the requirements of the supervisor and the job position",
                "Daily monitoring of the internet connection at the Institute",
                "Performing other tasks as directed by the unit manager",
            ],
            "de": [
                "Verantwortung für die rechtzeitige, gesetzmäßige, ordnungsgemäße und qualitativ hochwertige Erledigung der Aufgaben",
                "Verwaltung von Datenbanken und Informationstechnologien",
                "Benutzerverwaltung im Active Directory",
                "Konfiguration von Netzwerk- und Sicherheitsgeräten",
                "Implementierung von Softwarelösungen für die Bedürfnisse des Instituts",
                "Aktualisierung von Daten und Dokumenten auf dem Webportal",
                "Überwachung der Funktionsfähigkeit von Arbeitsstationen (Druckern und anderen Multifunktionsgeräten)",
                "IT-Support für Benutzer im Geschäftssystem, einschließlich System-Upgrades je nach Benutzeranforderungen",
                "Erstellung von Dokumentationen und Verfahren für das IT-System",
                "Schreiben von Skripten zur Automatisierung",
                "Identifizierung der Benutzeranforderungen, Entgegennahme verschiedener Anfragen, Bereitstellung von Unterstützung und Fehlerbehebung",
                "Implementierung von Sicherheitsmaßnahmen auf Computern",
                "Vorbereitung und Installation von Geräten im Besprechungsraum",
                "Weitere Aktivitäten gemäß den Anforderungen des Vorgesetzten und des Arbeitsplatzes",
                "Tägliche Überprüfung der Internetverbindung im Institut",
                "Ausführung weiterer Aufgaben auf Anweisung des Abteilungsleiters",
            ],
        },
    },
    {
        "id": "foreo",
        "company": "FOREO",
        "company_name": "FOREO",
        "logo": "foreo.png",
        "logo_caption": "[F O R E O](http://www.foreo.com)",
        "url": "http://www.foreo.com",
        "start": (2021, 11),
        "end": (2024, 2),
        "header": "F O R E O",
        "subheader": "IT support specialist",
        "sector": {"bs": "međunarodna tehnološka kompanija", "en": "international tech company", "de": "internationales Technologieunternehmen"},
        "aliases": ["foreo", "forio", "foreoa", "foreu"],
        "duties": {
            "bs": [
                "Odgovornost za osnovnu podršku korisnicima",
                "Instalacija i konfiguracija različitih IT softvera i mrežne opreme",
                "Instalacija i konfiguracija servera",
                "Upravljanje korisničkim računima, upravljanje IT opremom",
                "Konfiguracija i korištenje alata za automatizaciju instalacije i konfiguracije IT softvera",
                "Pisanje dokumentacije i procedura IT sistema",
                "Pisanje skripti za automatizaciju",
                "Pružanje pomoći i tehničke podrške korisnicima ERP sistema i razvojnog tima",
                "Odgovaranje na upite odjela",
                "E-mail korespondencija",
                "Druge aktivnosti u skladu sa zahtjevima nadležne osobe i zahtjevima radnog mjesta",
            ],
            "en": [
                "Responsibility for basic customer support",
                "Installation and configuration of various IT software and network equipment",
                "Installation and configuration of servers",
                "Management of user accounts, management of IT equipment",
                "Configuration and use of automation tools for installation and configuration of IT software",
                "Writing documentation and procedures of IT systems",
                "Writing automation scripts",
                "Providing assistance and technical support to ERP system users and development team",
                "Answering department inquiries",
                "E-mail correspondence",
                "Other activities in accordance with the request of the competent person, and in accordance with the requirements of the workplace",
            ],
            "de": [
                "Verantwortung für grundlegende Kundenbetreuung",
                "Installation und Konfiguration verschiedener IT-Software und Netzwerkgeräte",
                "Installation und Konfiguration von Servern",
                "Verwaltung von Benutzerkonten, Verwaltung von IT-Geräten",
                "Konfiguration und Nutzung von Automatisierungswerkzeugen für die Installation und Konfiguration von IT-Software",
                "Verfassen von Dokumentationen und Verfahren für IT-Systeme",
                "Schreiben von Automatisierungsskripten",
                "Bereitstellung von Unterstützung und technischem Support für ERP-Systembenutzer und Entwicklungsteam",
                "Beantwortung von Anfragen der Abteilung",
                "E-Mail-Korrespondenz",
                "Andere Aktivitäten gemäß dem Wunsch der zuständigen Person und den Anforderungen des Arbeitsplatzes",
            ],
        },
    },
    {
        "id": "logosoft",
        "company": "Logosoft",
        "company_name": "Logosoft",
        "logo": "logosoft.png",
        "logo_caption": "[LOGOSOFT](https://www.logosoft.ba)",
        "url": "https://www.logosoft.ba",
        "start": (2020, 10),
        "end": (2021, 11),
        "header": "LOGOSOFT",
        "subheader": "TECHNICAL SUPPORT PROVIDER FOR RESIDENTIAL SUBJECTS",
        "role": {
            "bs": "Tehnička podrška za rezidencijalne korisnike",
            "en": "Technical Support Provider for Residential Users",
            "de": "Technischer Support für Privatkunden",
        },
        "sector": {"bs": "internet provajder (ISP)", "en": "internet service provider (ISP)", "de": "Internetdienstanbieter (ISP)"},
        "aliases": ["logosoft", "logo soft", "logosofta", "logosoftu"],
        "duties": {
            "bs": [
                "Pružanje osnovne tehničke podrške korisnicima usluga (rješavanje problema) s eskalacijom problema na viši nivo",
                "Konfigurisanje portova na mrežnim otocima za nove korisnike",
                "Pozivanje korisnika, posebno u slučaju većih prekida i tehničkih problema",
                "Unos svih relevantnih podataka korisnika u odgovarajuće baze podataka i aplikacije",
                "Prodaja usluga stambenim korisnicima i drugih ponuda pružatelja usluga",
                "Praćenje ispravnog funkcionisanja usluge pružatelja internet usluga",
                "Praćenje i sprovođenje obaveznog gašenja TV sadržaja",
                "Pružanje potrebne podrške tehničarima za eksploataciju",
                "Predlaganje budžeta i praćenje implementacije budžeta",
            ],
            "en": [
                "Providing primary technical support to service users (problem solving) with problem escalation to higher levels",
                "Configuring ports on network islands for new users",
                "Calling users, especially in case of major outages and technical problems",
                "Entering all relevant user data into the appropriate databases and applications",
                "Sale of services for residential users and other offers of providers",
                "Monitoring the correct functioning of the ISP service",
                "Monitoring and implementation of mandatory blackout of TV content",
                "Providing necessary support to field technicians",
                "Proposing the budget and monitoring the implementation of the budget",
            ],
            "de": [
                "Bereitstellung primärer technischer Unterstützung für Servicenutzer (Problembehebung) mit Eskalation von Problemen auf höhere Ebenen",
                "Konfiguration von Ports auf Netzwerkinseln für neue Benutzer",
                "Anrufen von Benutzern, besonders im Falle größerer Ausfälle und technischer Probleme",
                "Eingabe aller relevanten Benutzerdaten in die entsprechenden Datenbanken und Anwendungen",
                "Verkauf von Dienstleistungen für Privatnutzer und anderen Angeboten von Anbietern",
                "Überwachung der korrekten Funktion des Internetdienstleisters (ISP)",
                "Überwachung und Umsetzung der obligatorischen Abschaltung von TV-Inhalten",
                "Bereitstellung notwendiger Unterstützung für Außendiensttechniker",
                "Vorschlag des Budgets und Überwachung der Umsetzung des Budgets",
            ],
        },
    },
    {
        "id": "cms",
        "company": "Capital Market Solutions (CMS)",
        "company_name": "Capital Market Solutions (CMS)",
        "logo": "cms.png",
        "logo_caption": "CMS",
        "url": None,
        "start": (2020, 6),
        "end": (2020, 10),
        "header": "CAPITAL MARKET SOLUTIONS",
        "subheader": "IT SCIENTIST",
        "role": {"bs": "IT Scientist (IT stručnjak)", "en": "IT Scientist", "de": "IT Scientist (Informatiker)"},
        "sector": {"bs": "finansijska tehnologija (tržište kapitala)", "en": "financial technology (capital markets)", "de": "Finanztechnologie (Kapitalmarkt)"},
        "aliases": ["cms", "capital market*", "market solutions"],
        "duties": {
            "bs": [
                "Održavanje IT opreme, video nadzora i mrežne infrastrukture",
                "Tehnička podrška za zaposlene",
                "Konfigurisanje internih sistema i VoIP uređaja",
                "Praćenje cyber sigurnosti",
                "Uspostavljanje sistema za rad na daljinu",
                "Kreiranje budžeta, upravljanje troškovima i nabavka opreme",
            ],
            "en": [
                "Maintenance of IT equipment, video surveillance and network infrastructure",
                "Technical support for employees",
                "Configuring internal systems and VoIP devices",
                "Cyber Security Monitoring",
                "Establishing a system for remote work",
                "Creating a budget, managing costs and purchasing equipment",
            ],
            "de": [
                "Wartung von IT-Geräten, Videoüberwachung und Netzwerkinfrastruktur",
                "Technische Unterstützung für Mitarbeiter",
                "Konfiguration interner Systeme und VoIP-Geräte",
                "Überwachung der Cybersicherheit",
                "Einrichtung eines Systems für die Arbeit im Homeoffice",
                "Erstellung eines Budgets, Kostenmanagement und Beschaffung von Ausrüstung",
            ],
        },
    },
    {
        "id": "payten",
        "company": "Payten",
        "company_name": "Payten",
        "logo": "payten.png",
        "logo_caption": "[PAYTEN](https://www.payten.com/en/)",
        "url": "https://www.payten.com/en/",
        "start": (2019, 3),
        "end": (2020, 2),
        "header": "PAYTEN",
        "subheader": "HELP DESK POS SUPPORT ASSOCIATE",
        "role": {
            "bs": "Help Desk podrška za POS i ATM",
            "en": "Help Desk POS Support Associate",
            "de": "Help-Desk-Mitarbeiter für POS-Support",
        },
        "sector": {"bs": "platni promet (POS i bankomati)", "en": "payments (POS and ATMs)", "de": "Zahlungsverkehr (POS und Geldautomaten)"},
        "aliases": ["payten", "pejten", "paytenu", "paytena"],
        "duties": {
            "bs": [
                "Korespondencija s bankama",
                "Testiranje",
                "Podrška za POS uređaje (rješavanje problema vezanih za rad POS terminala)",
                "Rješavanje prijavljenih problema",
                "Priprema terminala u vezi s instalacijom i intervencijom",
                "Podrška za bankomate (ATM)",
            ],
            "en": [
                "Correspondence with Banks",
                "Testing",
                "POS Support (resolving problems related to the operation of POS terminals)",
                "Solving reported problems",
                "Preparation of terminals regarding installation and intervention",
                "ATM Support",
            ],
            "de": [
                "Korrespondenz mit Banken",
                "Testen",
                "POS-Unterstützung (Lösung von Problemen im Zusammenhang mit dem Betrieb von POS-Terminals)",
                "Lösung gemeldeter Probleme",
                "Vorbereitung von Terminals in Bezug auf Installation und Intervention",
                "Unterstützung für Geldautomaten (ATM)",
            ],
        },
    },
    {
        "id": "ataco",
        "company": "Ataco Commerce",
        "company_name": "Ataco Commerce",
        "logo": "ataco.png",
        "logo_caption": "[A T A C O](https://ataco-bih.com/)",
        "url": "https://ataco-bih.com/",
        "start": (2017, 9),
        "end": (2018, 3),
        "header": "COMMERCIALIST",
        "subheader": "ATACO COMMERCE",
        "role": {"bs": "Komercijalista", "en": "Commercialist", "de": "Kaufmann (Außendienst)"},
        "sector": {"bs": "trgovina i distribucija", "en": "trade and distribution", "de": "Handel und Vertrieb"},
        "aliases": ["ataco", "atako", "ataca", "atacu"],
        "duties": {
            "bs": [
                "Primanje dnevnog plana dostave i ostalih dnevnih zadataka od dispečera",
                "Dostava vraćenih proizvoda u skladište u skladu s internim postupkom",
                "Kontrola, brojanje, prikupljanje i utovar robe iz skladišta",
                "Pregovaranje o novim narudžbama s kupcima",
            ],
            "en": [
                "Receiving the daily delivery plan and other daily tasks from the dispatcher",
                "Delivery of returned goods to the warehouse in accordance with the internal procedure",
                "Checking, counting, picking up, and loading goods from the warehouse",
                "Negotiating new orders with customers",
            ],
            "de": [
                "Empfang des täglichen Lieferplans und anderer täglicher Aufgaben vom Disponenten",
                "Rücklieferung der Waren gemäß dem internen Verfahren ins Lager",
                "Kontrolle, Zählung, Aufnahme und Beladung von Waren aus dem Lager",
                "Verhandlung neuer Bestellungen mit Kunden",
            ],
        },
    },
    {
        "id": "telinvest",
        "company": "Telinvest",
        "company_name": "Telinvest",
        "logo": "telinvest.png",
        "logo_caption": "[TELINVEST](https://www.telinvest.ba/)",
        "url": "https://www.telinvest.ba/",
        "start": (2015, 7),
        "end": (2017, 9),
        "header": "TECHNICAL SUPPORT FOR BUSINESS USERS",
        "subheader": "TELINVEST",
        "role": {
            "bs": "Tehnička podrška za poslovne korisnike",
            "en": "Technical Support for Business Users",
            "de": "Technischer Support für Geschäftskunden",
        },
        "sector": {"bs": "telekomunikacije", "en": "telecommunications", "de": "Telekommunikation"},
        "aliases": ["telinvest", "tel invest", "telinvestu", "telinvesta"],
        "duties": {
            "bs": [
                "Angažiran kao izvršilac tehničkih podrški u prostorijama BH TELECOM-a",
                "Pružanje osnovne tehničke podrške poslovnim korisnicima",
                "Pružanje tehničke podrške poslovnim korisnicima za ADSL, IPTV, mobilne mreže, POTS, VOIP, HOSTING, Web email usluge",
                "Praćenje i prijavljivanje općih problema, eskalacija problema na viši nivo drugim servisima",
                "Obavljanje dužnosti operatera dežurnog tima",
                "Pružanje potrebne podrške tehničarima za eksploataciju",
                "Unos svih relevantnih podataka korisnika u odgovarajuće baze podataka i aplikacije",
            ],
            "en": [
                "Engaged as an executor for technical support tasks in the premises of BH TELECOM",
                "Providing primary technical support to business users",
                "Providing technical support to business users for ADSL, IPTV, mobile networks, POTS, VOIP, HOSTING, Web email services",
                "Monitoring and reporting of general problems, escalation of problems to a higher level to other services",
                "Performing the duties of an operator on duty",
                "Providing necessary support to field technicians",
                "Entering all relevant user data into the appropriate databases and applications",
            ],
            "de": [
                "Engagiert als Ausführender für technische Supportaufgaben in den Räumlichkeiten von BH TELECOM",
                "Bereitstellung von grundlegender technischer Unterstützung für Geschäftskunden",
                "Bereitstellung von technischem Support für Geschäftskunden für ADSL, IPTV, Mobilfunknetze, POTS, VOIP, HOSTING, Web-E-Mail-Dienste",
                "Überwachung und Meldung allgemeiner Probleme, Eskalation von Problemen auf eine höhere Ebene zu anderen Diensten",
                "Ausführung der Aufgaben eines diensthabenden Operators",
                "Bereitstellung notwendiger Unterstützung für Außendiensttechniker",
                "Eingabe aller relevanten Benutzerdaten in die entsprechenden Datenbanken und Anwendungen",
            ],
        },
    },
    {
        "id": "bhtelecom",
        "company": "BH Telecom",
        "company_name": "BH Telecom",
        "logo": "bhtelecom.png",
        "logo_caption": "[BH Telecom](https://www.bhtelecom.ba)",
        "url": "https://www.bhtelecom.ba",
        "start": (2015, 1),
        "end": (2015, 7),
        "header": "TECHNICAL SUPPORT FOR RESIDENTIAL USERS",
        "subheader": "BH TELECOM SARAJEVO",
        "role": {
            "bs": "Tehnička podrška za rezidencijalne korisnike",
            "en": "Technical Support for Residential Users",
            "de": "Technischer Support für Privatkunden",
        },
        "sector": {"bs": "telekomunikacije", "en": "telecommunications", "de": "Telekommunikation"},
        "aliases": ["bh telecom", "bhtelecom", "bh telekom", "bhtelekom", "telecom", "telekom", "bht", "bh telecomu", "bh telecoma"],
        "duties": {
            "bs": [
                "Pružanje osnovne tehničke podrške korisnicima stambenih objekata",
                "Pružanje tehničke podrške poslovnim korisnicima za ADSL, IPTV, POTS, VOIP",
                "Pružanje potrebne podrške tehničarima za eksploataciju",
                "Unos svih relevantnih podataka korisnika u odgovarajuće baze podataka i aplikacije",
            ],
            "en": [
                "Providing primary technical support for Residential users",
                "Providing technical support to business users for ADSL, IPTV, POTS, VOIP",
                "Providing necessary support to field technicians",
                "Entering all relevant user data into the appropriate databases and applications",
            ],
            "de": [
                "Bereitstellung von primärer technischer Unterstützung für Privatkunden",
                "Bereitstellung von technischem Support für Geschäftskunden für ADSL, IPTV, POTS, VOIP",
                "Bereitstellung notwendiger Unterstützung für Außendiensttechniker",
                "Eingabe aller relevanten Benutzerdaten in die entsprechenden Datenbanken und Anwendungen",
            ],
        },
    },
    {
        "id": "seecontact",
        "company": "SEE Contact",
        "company_name": "SEE Contact",
        "logo": "see.png",
        "logo_caption": "SEE Contact",
        "url": None,
        "start": (2014, 8),
        "end": (2014, 12),
        "header": "TECHNICAL SUPPORT FOR RESIDENTIAL USERS",
        "subheader": "SEE CONTACT",
        "role": {
            "bs": "Tehnička podrška za rezidencijalne korisnike",
            "en": "Technical Support for Residential Users",
            "de": "Technischer Support für Privatkunden",
        },
        "sector": {"bs": "kontakt centar (telekomunikacije)", "en": "contact center (telecommunications)", "de": "Contact Center (Telekommunikation)"},
        "aliases": ["see contact", "seecontact", "see contactu", "see kontakt"],
        "duties": {
            "bs": [
                "Angažovan kao izvršitelj za tehničke podrške u prostorijama BH TELECOM-a",
                "Pružanje osnovne tehničke podrške korisnicima stambenih objekata",
                "Pružanje tehničke podrške poslovnim korisnicima za ADSL, IPTV, POTS, VOIP",
                "Pružanje potrebne podrške tehničarima za eksploataciju",
                "Unos svih relevantnih podataka korisnika u odgovarajuće baze podataka i aplikacije",
            ],
            "en": [
                "Engaged as an executor for technical support tasks in the premises of BH TELECOM",
                "Providing primary technical support for Residential users",
                "Providing technical support to business users for ADSL, IPTV, POTS, VOIP",
                "Providing necessary support to field technicians",
                "Entering all relevant user data into the appropriate databases and applications",
            ],
            "de": [
                "Tätig als Ausführender für technische Supportaufgaben in den Räumlichkeiten von BH TELECOM",
                "Bereitstellung primärer technischer Unterstützung für Privatkunden",
                "Bereitstellung von technischem Support für Geschäftskunden für ADSL, IPTV, POTS, VOIP",
                "Bereitstellung notwendiger Unterstützung für Außendiensttechniker",
                "Eingabe aller relevanten Benutzerdaten in die entsprechenden Datenbanken und Anwendungen",
            ],
        },
    },
]


def job_role(job, lang):
    """Naziv pozicije za chatbot (ako nije posebno naveden, koristi subheader)."""
    return tr(job.get("role") or job["subheader"], lang)


JOBS_BY_ID = {job["id"]: job for job in JOBS}
PROJECTS_BY_ID = {project["id"]: project for project in PROJECTS}
