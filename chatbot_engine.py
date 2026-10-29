# --- OFFLINE CHATBOT ENGINE ---
# Radi potpuno bez interneta i bez API-ja. Koristi samo standardnu Python biblioteku.
#
# Kako radi:
#   1. Tekst se normalizuje (mala slova, bez kvačica, "c#" -> "csharp" ...).
#   2. Prepoznaje se jezik pitanja (bs / en / de).
#   3. Prepoznaju se entiteti: firma, vještina/oblast, projekat, godina.
#   4. Svaka namjera (intent) dobija bodove po ključnim riječima (tačno, prefiks ili
#      "fuzzy" poklapanje za greške u kucanju) i pobjeđuje najjača.
#   5. Ako ništa ne odgovara, pretražuje se cijeli tekst CV-a i vraćaju se najrelevantnije stavke.
#   6. Kontekst razgovora (zadnja firma, zadnja tema) omogućava pitanja tipa "A koliko dugo?".

import difflib
import os
import random
import re
from datetime import date

import cv_data as cv
from cv_data import tr, format_period, job_role

LANGS = ("bs", "en", "de")


# =============================================================================
# 1. NORMALIZACIJA I TOKENIZACIJA
# =============================================================================

_CHAR_MAP = str.maketrans({
    "č": "c", "ć": "c", "š": "s", "ž": "z", "ä": "a", "ö": "o", "ü": "u",
    "é": "e", "è": "e", "á": "a", "à": "a", "ó": "o", "í": "i", "ú": "u",
    "’": "'", "`": "'",
})

# Tehnički nazivi sa specijalnim znakovima -> jedna "riječ"
_TECH_SUBSTITUTIONS = [
    (r"c\s*#", " csharp "), (r"c\+\+", " cpp "), (r"\.net\b", " dotnet "), (r"asp\.net", " aspnet "),
    (r"node\.?js", " nodejs "), (r"vue\.?js", " vue "), (r"react\.?js", " react "), (r"next\.?js", " nextjs "),
    (r"ci\s*/\s*cd", " cicd "), (r"ci-cd", " cicd "), (r"hyper\s*-\s*v", " hyperv "), (r"\.glb\b", " glb "),
    (r"rodin\s*-?\s*3d", " rodin3d "), (r"e\s*-\s*mail", " email "), (r"g\s*suite", " gsuite "),
    (r"k8s", " kubernetes "), (r"\bms\s+office", " msoffice "), (r"office\s*365", " office365 "),
    (r"microsoft\s*365", " office365 "), (r"\bm365\b", " office365 "), (r"java\s*script", " javascript "),
    (r"type\s*script", " typescript "), (r"power\s*shell", " powershell "), (r"active\s*directory", " activedirectory "),
    (r"home\s*-?\s*office", " homeoffice "), (r"wie geht'?s", " wie geht es "), (r"what'?s up", " whats up "),
]


def normalize(text):
    text = text.lower().replace("đ", "dj").replace("ß", "ss").translate(_CHAR_MAP)
    for pattern, replacement in _TECH_SUBSTITUTIONS:
        text = re.sub(pattern, replacement, text)
    return text


def tokenize(normalized):
    return re.findall(r"[a-z0-9]+", normalized)


# Riječi bez značenja (za pretragu i da fuzzy poklapanje ne "pogađa" veznike)
STOPWORDS = set("""
a i u o na za je su se da li ili ne sa s od do po iz uz pa te ti ja mi vi on ona oni to taj ta
koji koja koje sta sto sto kako kad kada gdje ko cu ces ce smo ste bi bih bio bila bilo biti
imas ima imam mi me mene tebe te tvoj tvoja tvoje moj moja moje sve svi jos samo vec
the a an and or of to in on at for with by is are was were be been am i you he she it we they
me my your his her our their this that these those do does did have has had what who whom
which how when where why can could would should will shall may might must there here about
from as into than then so if but not no yes please tell show give
der die das ein eine einen einem und oder zu im in am an auf fur mit von bei ist sind war
waren bin bist sein ich du er sie es wir ihr mich dich mir dir mein dein was wer wie wann wo
warum welche welcher welches hast hat haben kannst kann bitte sag mal auch noch schon
""".split())


# =============================================================================
# 2. PREPOZNAVANJE JEZIKA
# =============================================================================

_LANG_WORDS = {
    "bs": set("""
        zdravo pozdrav cao hej kako si sta sto gdje kada zasto koliko koji koja koje ko jesi li
        imas ima radis radio radila posao poslu iskustvo vjestine znas mozes reci mi molim hvala
        fala jezik jezike govoris pricas zivis firma firmi kompanija skola obrazovanje plata
        dobar dan jutro vece ime zoves tvoj tvoja tvoje svoj sebi tebi mene nesto nisi jesam
        nemam imam treba trebam zanima zanimaju projekti projekte vjestinama dugo godina godine
        trenutno sada sad prije onda a i u na za od do sa iz bih bi ces cu biti bio bila kod
        jezici jezika iskustva vjestina programski programiranje znanje obrazovanje skola fakultet
        plata posla poslove firme firmama projekat projekti mrezama mreze sigurnost certifikate kontakt
        broj telefona zivis zivim zasto zaposliti tebe tvoje imas li jesi radio radila koliko
        """.split()),
    "en": set("""
        hello hi hey how are you what where when why who which is the a an do does did have has
        your you me my tell about experience skills work worked job jobs company companies
        school education salary languages speak live thanks thank please can could would should
        know long years year current currently now before after with and or of to in at for
        good morning evening name contact email phone projects project there their they
        """.split()),
    "de": set("""
        hallo guten tag morgen abend wie geht es was wo wann warum wer welche welcher ist bist
        sind hast hat haben du dich dir dein deine ich mich mir mein meine erfahrung arbeit
        arbeitest gearbeitet firma unternehmen schule ausbildung gehalt sprachen sprichst
        sprechen wohnst danke bitte kannst konnen lange jahre jahr derzeit jetzt vorher und oder
        der die das ein eine einen mit von bei fur auf uber erzahl erzahlen kenntnisse
        fahigkeiten projekte kontakt nummer telefon lebenslauf heisst name tschuss
        """.split()),
}


def detect_language(text, fallback="en"):
    """Vraća (jezik, sigurnost). Kvačice i umlauti su jak signal."""
    lowered = text.lower()
    tokens = tokenize(normalize(text))
    scores = {lang: sum(1 for t in tokens if t in words) for lang, words in _LANG_WORDS.items()}
    if re.search(r"[čćšđž]", lowered):
        scores["bs"] += 3
    if re.search(r"[äöüß]", lowered):
        scores["de"] += 3
    best = max(scores, key=scores.get)
    ordered = sorted(scores.values(), reverse=True)
    if ordered[0] == 0 or ordered[0] == ordered[1]:
        return fallback, 0
    return best, ordered[0] - ordered[1]


# =============================================================================
# 3. POKLAPANJE KLJUČNIH RIJEČI
# =============================================================================
# Format ključne riječi:
#   "rijec"          -> tačno poklapanje riječi (ili fuzzy za duže riječi sa greškom u kucanju)
#   "prefiks*"       -> riječ počinje sa prefiksom (pokriva padeže: iskustvo, iskustva, iskustvom...)
#   "vise rijeci"    -> fraza (riječi jedna do druge), nosi više bodova
#   "rijec:2"        -> posebna težina

class KeywordMatcher:
    def __init__(self, table, fuzzy_cutoff=0.84):
        self.exact = {}      # rijec -> [(kljuc, tezina)]
        self.prefixes = []   # (prefiks, kljuc, tezina)
        self.phrases = []    # (fraza, kljuc, tezina)
        self.fuzzy_cutoff = fuzzy_cutoff
        for key, specs in table.items():
            for spec in specs:
                spec, _, weight = spec.partition(":")
                spec = normalize(spec).strip()
                if " " in spec:
                    # Svaka riječ fraze može imati "*" (npr. "programsk* jezi*")
                    words = [re.escape(w[:-1]) + "[a-z0-9]*" if w.endswith("*") else re.escape(w) for w in spec.split()]
                    pattern = re.compile(r"(?<![a-z0-9])" + " ".join(words) + r"(?![a-z0-9])")
                    self.phrases.append((pattern, key, float(weight or 2.5)))
                elif spec.endswith("*"):
                    self.prefixes.append((spec[:-1], key, float(weight or 1)))
                else:
                    self.exact.setdefault(spec, []).append((key, float(weight or 1)))
        self._vocab = [w for w in self.exact if len(w) >= 5]

    def match(self, tokens):
        """Vraća {kljuc: bodovi}."""
        scores = {}

        def add(key, weight):
            scores[key] = scores.get(key, 0) + weight

        joined = " ".join(tokens)
        for pattern, key, weight in self.phrases:
            if pattern.search(joined):
                add(key, weight)

        for token in tokens:
            hits = self.exact.get(token)
            if hits:
                for key, weight in hits:
                    add(key, weight)
                continue
            prefix_hit = False
            for prefix, key, weight in self.prefixes:
                if token.startswith(prefix):
                    add(key, weight)
                    prefix_hit = True
            if prefix_hit or token in STOPWORDS or len(token) < 5:
                continue
            # Greška u kucanju: "expirience" -> "experience"
            for close in difflib.get_close_matches(token, self._vocab, n=2, cutoff=self.fuzzy_cutoff):
                for key, weight in self.exact[close]:
                    add(key, weight * 0.8)
        return scores


# =============================================================================
# 4. ZNANJE: VJEŠTINE I OBLASTI (sa dokazima iz CV-a)
# =============================================================================
# evidence = riječi koje se traže u engleskim opisima poslova; pronađene stavke se
# prikazuju na jeziku korisnika (liste su paralelne na sva tri jezika).

KNOWLEDGE = [
    # --- Programiranje ---
    {"id": "python", "name": "Python", "aliases": ["python", "pajton", "piton", "py"], "category": "programming",
     "level": {"bs": "napredni nivo (Advanced)", "en": "advanced level", "de": "fortgeschrittenes Niveau (Advanced)"},
     "evidence": ["script"], "projects": ["helpdesk"]},
    {"id": "typescript", "name": "TypeScript", "aliases": ["typescript", "ts"], "category": "programming", "projects": ["webdev"]},
    {"id": "javascript", "name": "JavaScript / jQuery", "aliases": ["javascript", "js", "jquery", "ecmascript"], "category": "programming", "projects": ["webdev"]},
    {"id": "react", "name": "React", "aliases": ["react", "reactjs"], "category": "programming", "projects": ["webdev"]},
    {"id": "vite", "name": "Vite", "aliases": ["vite"], "category": "programming", "projects": ["webdev"]},
    {"id": "tailwind", "name": "Tailwind CSS", "aliases": ["tailwind", "css", "html", "frontend", "front end", "web dizajn", "web design", "webdesign"],
     "category": "programming", "projects": ["webdev"]},
    {"id": "csharp", "name": "C#", "aliases": ["csharp", "dotnet", "aspnet"], "category": "programming"},
    {"id": "webdev", "name": {"bs": "Web razvoj", "en": "Web development", "de": "Webentwicklung"},
     "aliases": ["web development", "web razvoj", "webentwicklung", "web stranic*", "websit*", "webseite*", "web aplikacij*", "web app*", "sajt*", "internet stranic*"],
     "category": "programming", "evidence": ["web portal"], "projects": ["webdev", "3d"]},

    # --- AI i automatizacija ---
    {"id": "ai", "name": {"bs": "Umjetna inteligencija (AI / LLM)", "en": "Artificial intelligence (AI / LLM)", "de": "Künstliche Intelligenz (KI / LLM)"},
     "aliases": ["ai", "ki", "llm", "llms", "umjetn* inteligencij*", "vjestack* inteligencij*", "artificial intelligence", "kunstliche intelligenz",
                 "machine learning", "masinsko ucenje", "masinskog ucenja", "generativ*", "genai", "gpt", "chatgpt", "openai", "langchain",
                 "neural*", "neuronsk*", "prompt*", "rag"],
     "category": "ai", "projects": ["helpdesk", "ailab", "3d"]},
    {"id": "gemini", "name": "Gemini API", "aliases": ["gemini", "google ai", "bard"], "category": "ai", "projects": ["helpdesk"]},
    {"id": "ollama", "name": "Ollama", "aliases": ["ollama", "lokaln* llm*", "local llm*", "lokalni model*", "llama"], "category": "ai", "projects": ["ailab"]},
    {"id": "agents", "name": {"bs": "AI agenti i automatizacija (Claude Code, Aider, AutoGen)", "en": "AI agents & automation (Claude Code, Aider, AutoGen)",
                              "de": "KI-Agenten & Automatisierung (Claude Code, Aider, AutoGen)"},
     "aliases": ["claude code:3", "claude:2", "anthropic", "autogen", "aider", "agent*", "agenat*", "agenata", "agentic", "multi agent*", "multiagent*",
                 "coding agent*", "ai agent*", "ki agent*"],
     "category": "ai", "projects": ["cvsite"]},
    {"id": "appsscript", "name": "Google Apps Script", "aliases": ["apps script:3", "google apps script:4", "appsscript", "gas"], "category": "ai", "projects": ["cvsite"]},
    {"id": "streamlit", "name": "Streamlit", "aliases": ["streamlit:2"], "category": "programming", "projects": ["cvsite"]},
    {"id": "cloudflare", "name": "Cloudflare (Turnstile)", "aliases": ["cloudflare", "turnstile", "captcha", "recaptcha"], "category": "devops", "projects": ["cvsite"]},
    {"id": "gcloud", "name": "Google Cloud API", "aliases": ["google cloud", "gcp", "gcloud"], "category": "ai"},
    {"id": "vba", "name": "PowerPoint VBA", "aliases": ["vba", "makro*", "macro*", "powerpoint", "visual basic"], "category": "ai"},
    {"id": "automation", "name": {"bs": "Automatizacija", "en": "Automation", "de": "Automatisierung"},
     "aliases": ["automatiz*", "automat*", "skript*", "script*", "scripting", "skriptir*", "powershell", "bash", "shell"],
     "category": "ai", "evidence": ["automation"], "projects": ["helpdesk"]},

    # --- DevOps ---
    {"id": "docker", "name": "Docker", "aliases": ["docker", "dokr", "kontejner*", "container*", "containeriz*"], "category": "devops", "projects": ["ailab"]},
    {"id": "linux", "name": "Linux (Ubuntu / Debian)", "aliases": ["linux", "ubuntu", "debian", "unix", "linuks"], "category": "devops", "projects": ["helpdesk", "ailab"]},
    {"id": "cicd", "name": "CI/CD, Git / GitHub", "aliases": ["cicd", "pipeline*", "continuous integration", "deployment", "deploy*", "git", "github", "github actions",
                                                    "github pages:2", "gitlab ci", "jenkins", "devops"],
     "category": "devops", "projects": ["cvsite"]},
    {"id": "hosting", "name": {"bs": "Web hosting", "en": "Web hosting", "de": "Webhosting"}, "aliases": ["hosting", "hostinga", "webhosting", "cpanel", "domen*", "domain*"],
     "category": "devops", "evidence": ["hosting", "web portal"]},
    {"id": "macos", "name": "Mac OS", "aliases": ["mac", "macos", "apple", "osx", "macbook"], "category": "devops"},
    {"id": "cloud", "name": "Cloud", "aliases": ["cloud", "oblak*", "azure", "aws", "amazon web services"], "category": "devops",
     "note": {"bs": "Na CV-u je Google Cloud API i web hosting administracija; AWS i Azure nisu posebno navedeni.",
              "en": "My CV lists Google Cloud API and web hosting administration; AWS and Azure are not listed specifically.",
              "de": "Im Lebenslauf stehen Google Cloud API und Webhosting-Administration; AWS und Azure sind nicht ausdrücklich aufgeführt."}},

    # --- Virtualizacija ---
    {"id": "virtualization", "name": {"bs": "Virtualizacija (VMware, Hyper-V, VirtualBox)", "en": "Virtualization (VMware, Hyper-V, VirtualBox)", "de": "Virtualisierung (VMware, Hyper-V, VirtualBox)"},
     "aliases": ["vmware", "hyperv", "virtualbox", "virtualiz*", "virtualis*", "vm", "vms", "virtueln* masin*", "virtual machine*", "esxi", "vsphere", "proxmox", "hypervisor*"],
     "category": "virtualization", "projects": ["ailab"]},

    # --- Sistemska administracija ---
    {"id": "ad", "name": "Active Directory", "aliases": ["activedirectory", "ad", "domenski", "ldap", "group policy", "gpo", "korisnick* racun*", "user account*", "benutzerkont*"],
     "category": "sysadmin", "evidence": ["active directory", "user accounts"]},
    {"id": "gsuite", "name": "G Suite / Google Workspace", "aliases": ["gsuite", "google workspace", "google suite", "gmail admin"], "category": "sysadmin"},
    {"id": "windows", "name": "Windows / Windows Server", "aliases": ["windows", "win", "windows server", "os administr*", "operativn* sistem*", "operating system*", "betriebssystem*"],
     "category": "sysadmin", "evidence": ["workstations", "computers"]},
    {"id": "network", "name": {"bs": "Mreže (networking)", "en": "Networking", "de": "Netzwerke"},
     "aliases": ["mrez*", "network*", "netzwerk*", "networking", "lan", "wan", "wifi", "wlan", "router*", "switch*", "firewall*", "vlan*", "tcp", "dns", "dhcp",
                 "cisco", "mikrotik", "ccna", "port*", "internet konekcij*", "internet connection", "isp",
                 "optick*", "optik*", "optic*", "fiber*", "fibre*", "glasfaser*", "ftth", "gpon"],
     "category": "sysadmin", "evidence": ["network", "ports", "internet connection", "isp"]},
    {"id": "security", "name": {"bs": "IT sigurnost", "en": "IT security", "de": "IT-Sicherheit"},
     "aliases": ["sigurnos*", "security", "cyber*", "sicherheit*", "cybersecurity", "zastit*", "antivirus*", "hakiranj*", "hacking", "penetration", "infosec"],
     "category": "sysadmin", "evidence": ["security", "surveillance"]},
    {"id": "hardware", "name": {"bs": "Hardver i održavanje opreme", "en": "Hardware & equipment maintenance", "de": "Hardware & Gerätewartung"},
     "aliases": ["hardver*", "hardware", "oprem*", "equipment", "printer*", "stampac*", "drucker*", "racunar*", "computer*", "workstation*", "radn* stanic*",
                 "odrzavanj*", "maintenance", "wartung", "servisir*", "repair*", "popravk*", "multifunkcijsk*"],
     "category": "sysadmin", "evidence": ["equipment", "workstations", "printers", "terminals"]},
    {"id": "servers", "name": {"bs": "Serveri", "en": "Servers", "de": "Server"}, "aliases": ["server*", "serveri", "servera", "serverima", "data center", "datacenter"],
     "category": "sysadmin", "evidence": ["server"]},
    {"id": "databases", "name": {"bs": "Baze podataka", "en": "Databases", "de": "Datenbanken"},
     "aliases": ["baz* podatak*", "database*", "datenbank*", "sql", "mysql", "postgres*", "mssql", "oracle", "db", "dba", "mongodb"],
     "category": "sysadmin", "evidence": ["database"],
     "note": {"bs": "Konkretni sistemi baza (npr. MySQL, MSSQL) nisu navedeni u CV-u – za detalje me kontaktirajte.",
              "en": "Specific database engines (e.g. MySQL, MSSQL) are not listed in my CV – feel free to ask me directly.",
              "de": "Konkrete Datenbanksysteme (z. B. MySQL, MSSQL) sind im Lebenslauf nicht aufgeführt – fragen Sie mich gerne direkt."}},
    {"id": "monitoring", "name": {"bs": "Monitoring sistema i mreže", "en": "System & network monitoring", "de": "System- und Netzwerküberwachung"},
     "aliases": ["monitoring", "nadzor*", "pracenj*", "uberwach*", "zabbix", "nagios", "grafana", "prtg"],
     "category": "sysadmin", "evidence": ["monitoring"]},
    {"id": "voip", "name": {"bs": "VoIP / telefonija", "en": "VoIP / telephony", "de": "VoIP / Telefonie"}, "aliases": ["voip", "telefonij*", "telephony", "pots", "pbx", "centrala", "sip"],
     "category": "sysadmin", "evidence": ["voip"]},

    # --- Alati ---
    {"id": "office", "name": "MS Office / Google Suite", "aliases": ["msoffice", "office", "office365", "excel", "word", "outlook", "teams", "sharepoint", "google docs", "google sheets"],
     "category": "tools"},
    {"id": "photoshop", "name": "Photoshop", "aliases": ["photoshop", "fotosop", "grafick* dizajn*", "graphic design", "adobe", "gimp"], "category": "tools"},
    {"id": "joomla", "name": "Joomla (K2)", "aliases": ["joomla", "k2", "cms sistem*", "wordpress", "content management"], "category": "tools", "evidence": ["web portal"]},
    {"id": "3dmodel", "name": {"bs": "3D modelovanje (Rodin-3D, ComfyUI, .glb)", "en": "3D modeling (Rodin-3D, ComfyUI, .glb)", "de": "3D-Modellierung (Rodin-3D, ComfyUI, .glb)"},
     "aliases": ["3d", "rodin3d", "rodin", "comfyui", "glb", "dinov3", "blender", "cad", "modelovanj*", "modeling", "modellierung"],
     "category": "tools", "projects": ["3d"]},
    {"id": "qa", "name": {"bs": "Testiranje softvera (QA)", "en": "Software testing (QA)", "de": "Softwaretests (QA)"},
     "aliases": ["qa", "testiranj*", "testing", "tester*", "test*", "quality assurance", "istqb", "bug*"],
     "category": "tools", "evidence": ["testing"]},

    # --- Oblasti rada (domene) ---
    {"id": "support", "name": {"bs": "Tehnička podrška / Help Desk", "en": "Technical support / Help Desk", "de": "Technischer Support / Help Desk"},
     "aliases": ["podrsk*", "support*", "helpdesk", "help desk", "service desk", "servicedesk", "troubleshoot*", "rjesavanj* problem*", "problem solving",
                 "fehlerbehebung", "korisnick* podrsk*", "customer support", "customer service", "kundensupport", "kundenbetreuung", "it podrsk*", "it support",
                 "first level", "second level", "1st level", "2nd level", "l1", "l2", "tiket*", "ticket*"],
     "category": "sysadmin", "evidence": ["support", "troubleshooting", "problems", "inquiries"]},
    {"id": "telecom", "name": {"bs": "Telekomunikacije", "en": "Telecommunications", "de": "Telekommunikation"},
     "aliases": ["telekomunikacij*", "telecommunication*", "telekommunikation", "telco", "adsl", "dsl", "iptv", "mobiln* mrez*", "mobile network*", "provajder*", "provider*"],
     "category": "sysadmin", "evidence": ["adsl", "iptv", "isp", "tv content"]},
    {"id": "banking", "name": {"bs": "Bankarstvo i platni promet (POS / ATM)", "en": "Banking & payments (POS / ATM)", "de": "Banken & Zahlungsverkehr (POS / ATM)"},
     "aliases": ["bank*", "pos", "atm", "bankomat*", "geldautomat*", "payment*", "placanj*", "platn* promet*", "fintech", "finansij*", "financ*", "kartic*", "terminal*"],
     "category": "sysadmin", "evidence": ["banks", "pos", "atm", "terminals"]},
    {"id": "erp", "name": "ERP", "aliases": ["erp", "sap", "navision", "dynamics"], "category": "sysadmin", "evidence": ["erp"]},
    {"id": "cctv", "name": {"bs": "Video nadzor", "en": "Video surveillance (CCTV)", "de": "Videoüberwachung"},
     "aliases": ["video nadzor*", "videonadzor*", "cctv", "kamer*", "camera*", "surveillance", "videouberwachung"], "category": "sysadmin", "evidence": ["surveillance"]},
    {"id": "remote", "name": {"bs": "Sistemi za rad na daljinu", "en": "Remote work systems", "de": "Systeme für Remote-Arbeit"},
     "aliases": ["vpn", "remote desktop", "rdp", "teamviewer", "anydesk", "remote access", "udaljen* pristup*"], "category": "sysadmin", "evidence": ["remote work"]},
    {"id": "documentation", "name": {"bs": "Dokumentacija i procedure", "en": "Documentation & procedures", "de": "Dokumentation & Verfahren"},
     "aliases": ["dokumentacij*", "documentation", "dokumentation", "procedur*", "procedure*", "verfahren", "uputstv*", "manual*", "wiki", "knowledge base"],
     "category": "sysadmin", "evidence": ["documentation"]},
    {"id": "management", "name": {"bs": "Budžet, nabavka i organizacija", "en": "Budgeting, procurement & organization", "de": "Budget, Beschaffung & Organisation"},
     "aliases": ["budzet*", "budget*", "nabavk*", "procurement", "beschaffung", "troskov*", "cost*", "kosten*", "menadzment*", "management", "manage*", "upravlj*",
                 "rukovod*", "lead*", "leader*", "vodj*", "team lead", "teamleiter*", "fuhrung*", "leitung", "organizac*", "organiz*", "koordin*", "coordinat*"],
     "category": "sysadmin", "evidence": ["budget", "purchasing", "costs"]},
    {"id": "sales", "name": {"bs": "Prodaja i pregovaranje", "en": "Sales & negotiation", "de": "Vertrieb & Verhandlung"},
     "aliases": ["prodaj*", "sales", "sale", "selling", "verkauf*", "vertrieb*", "pregovar*", "negotiat*", "verhandl*", "kupc*", "customers", "komercijal*", "commercial*", "b2b"],
     "category": "tools", "evidence": ["sale of services", "selling", "negotiat", "orders"]},
    {"id": "logistics", "name": {"bs": "Logistika i skladište", "en": "Logistics & warehouse", "de": "Logistik & Lager"},
     "aliases": ["logistik*", "logistic*", "skladist*", "warehouse*", "lager*", "dostav*", "delivery", "lieferung*", "vozac*", "driver*", "vozack*", "dispecer*", "dispatcher*"],
     "category": "tools", "evidence": ["delivery", "warehouse", "dispatcher"]},
    {"id": "oncall", "name": {"bs": "Dežurstva i rad u smjenama", "en": "On-call duty & shifts", "de": "Bereitschaftsdienst & Schichtarbeit"},
     "aliases": ["dezur*", "on call", "oncall", "on duty", "bereitschaft*", "smjen*", "shift*", "schicht*", "24/7", "nocn* smjen*", "night shift*", "vikend*", "weekend*"],
     "category": "sysadmin", "evidence": ["on duty", "outages"]},
    {"id": "av", "name": {"bs": "Konferencijska / AV oprema", "en": "Meeting room / AV equipment", "de": "Konferenz- / AV-Technik"},
     "aliases": ["sala za sastanke", "meeting room", "konferencij*", "conference", "projektor*", "projector*", "audio", "video konferencij*", "zoom", "besprechungsraum"],
     "category": "sysadmin", "evidence": ["meeting room"]},
]
KNOWLEDGE_BY_ID = {item["id"]: item for item in KNOWLEDGE}

# Tehnologije koje NISU na CV-u -> iskren odgovor + najbliže srodno iskustvo
UNLISTED_TECH = {
    "kubernetes": ("Kubernetes", ["docker", "cicd"]), "openshift": ("OpenShift", ["docker"]),
    "terraform": ("Terraform", ["automation", "cicd"]), "ansible": ("Ansible", ["automation"]),
    "puppet": ("Puppet", ["automation"]), "chef": ("Chef", ["automation"]),
    "java": ("Java", ["programming"]), "php": ("PHP", ["joomla", "webdev"]), "golang": ("Go", ["programming"]),
    "rust": ("Rust", ["programming"]), "kotlin": ("Kotlin", ["programming"]), "swift": ("Swift", ["programming"]),
    "ruby": ("Ruby", ["programming"]), "perl": ("Perl", ["automation"]), "cpp": ("C++", ["csharp"]),
    "angular": ("Angular", ["react"]), "vue": ("Vue.js", ["react"]), "svelte": ("Svelte", ["react"]), "nextjs": ("Next.js", ["react"]),
    "django": ("Django", ["python"]), "flask": ("Flask", ["python"]), "fastapi": ("FastAPI", ["python"]),
    "nodejs": ("Node.js", ["javascript"]), "tensorflow": ("TensorFlow", ["ai", "python"]), "pytorch": ("PyTorch", ["ai", "python"]),
    "intune": ("Microsoft Intune", ["automation", "windows"]), "sccm": ("SCCM / MECM", ["automation", "windows"]),
    "exchange": ("Microsoft Exchange", ["office", "windows"]), "citrix": ("Citrix", ["virtualization", "remote"]),
    "veeam": ("Veeam", ["servers"]), "backup": ("Backup", ["servers"]), "splunk": ("Splunk", ["monitoring", "security"]),
    "prometheus": ("Prometheus", ["monitoring"]), "elk": ("ELK stack", ["monitoring"]), "jira": ("Jira", ["support"]),
    "servicenow": ("ServiceNow", ["support"]), "salesforce": ("Salesforce", ["sales"]), "figma": ("Figma", ["photoshop", "webdev"]),
    "unity": ("Unity", ["3dmodel"]), "unreal": ("Unreal Engine", ["3dmodel"]), "fortinet": ("Fortinet", ["network", "security"]),
    "fortigate": ("FortiGate", ["network", "security"]), "paloalto": ("Palo Alto", ["network", "security"]),
}


# =============================================================================
# 5. NAMJERE (INTENTS)
# =============================================================================

INTENTS = {
    "greeting": ["zdravo", "pozdrav*", "cao", "ciao", "hej", "hey", "hi", "hello", "hallo", "hallochen", "servus", "moin", "selam", "merhaba",
                 "dobar dan", "dobro jutro", "dobro vece", "dobra vecer", "good morning", "good afternoon", "good evening", "guten tag",
                 "guten morgen", "guten abend", "gruss gott", "grus gott", "howdy", "es selamu alejkum", "selamu alejkum", "zdrao", "hejj"],
    "farewell": ["dovidjenja", "do vidjenja", "vidimo se", "prijatno", "laku noc", "bye", "goodbye", "good bye", "see you", "see ya", "good night",
                 "tschuss", "tschus", "auf wiedersehen", "gute nacht", "bis bald", "pozz"],
    "thanks": ["hvala", "fala", "hvala ti", "hvala vam", "thanks", "thank you", "thx", "ty", "danke", "danke schon", "vielen dank", "zahvaljujem",
               "super", "odlicno", "great", "perfect", "perfekt", "awesome", "cool", "nice", "bravo", "top", "sjajno", "toll", "prima", "klasa"],
    "how_are_you": ["kako si", "kako ste", "sta ima", "kako ide", "sta radis", "how are you", "how is it going", "how are things", "whats up",
                    "wie geht es", "wie gehts", "alles gut", "jesi dobro"],
    "bot": ["bot:2", "robot*", "chatbot:2", "jesi li bot", "jesi li covjek", "jesi li stvaran", "are you a bot", "are you human", "are you real",
            "bist du ein bot", "bist du echt", "ko te napravio", "ko te je napravio", "who made you", "who built you", "who created you",
            "wer hat dich", "kako radis", "how do you work", "wie funktionierst du", "offline", "api", "asistent*", "assistant"],
    "intro": ["ko si", "ko ste", "ko je amar", "ko je on", "who are you", "who is amar", "who is he", "wer bist du", "wer ist amar",
              "predstavi se", "predstavi", "nesto o sebi", "o sebi", "o tebi", "o amaru", "about yourself", "about you", "about amar",
              "uber dich", "uber amar", "erzahl", "introduce", "introduction", "summary", "rezime", "sazetak", "sazmi", "profil", "profile",
              "zusammenfassung", "background", "bio", "biografij*", "opis", "describe yourself", "opisi se", "beschreib*", "amar:0.5", "helac:0.5"],
    "name": ["kako se zoves", "ime", "imena", "zoves", "your name", "name:1.5", "heisst", "wie heisst", "puno ime", "prezime", "full name", "surname"],
    "age": ["koliko imas godina", "koliko ti je godina", "koliko godina imas", "how old", "your age", "age", "godiste", "rodjen*", "born",
            "wie alt", "alter", "geboren", "datum rodjenja", "birthday", "rodjendan", "geburtstag", "star si"],
    "personal": ["ozenjen", "ozenjeni", "married", "verheiratet", "djeca", "djece", "dijete", "kids", "children", "kinder", "vjer*", "religion*",
                 "religij*", "porodic*", "family", "familie", "djevojk*", "girlfriend", "wife", "zena", "supruga", "partner*", "politik*", "politic*"],
    "hobbies": ["hobi*", "hobby", "hobbies", "slobodno vrijeme", "slobodnom vremenu", "free time", "spare time", "freizeit", "interesuje te",
                "sta volis", "what do you like", "was magst du", "sport*", "fudbal*", "football", "soccer", "muzik*", "music", "gaming",
                "igric*", "putovanj*", "travel*", "reisen", "citanj*", "reading", "knjig*", "books", "film*", "movies"],
    "contact": ["kontakt*", "contact*", "email:2", "mail", "mejl*", "reach", "javi*", "pisi", "pisati", "napisati", "kako da te", "kako mogu da te",
                "how can i reach", "get in touch", "erreich*", "schreib*", "kontaktier*", "adresa e", "email adres*", "poruk*", "message"],
    "phone": ["telefon*", "phone", "broj telefona", "broj mobitela", "nummer", "mobitel*", "mobile number", "handy", "viber", "whatsapp",
              "nazvati", "nazovem", "pozvati", "call you", "anruf*", "anrufen"],
    "social": ["linkedin", "github", "gitlab", "twitter", "instagram", "facebook", "drustven* mrez*", "social media", "social network*",
               "xing", "profil na", "link*"],
    "location": ["gdje zivis", "gdje si", "gdje se nalazis", "odakle si", "odakle", "where do you live", "where are you", "where are you from",
                 "wo wohnst du", "woher", "wo lebst du", "lokacij*", "location", "located", "grad", "city", "stadt", "adres*", "address",
                 "drzav*", "country", "zemlj*", "sarajev*", "bosn*", "bih", "zivis", "live:1.5", "wohn*", "where:0.5", "gdje:0.5", "wo:0.5"],
    "relocation": ["preseli*", "preselj*", "relocat*", "move to", "moving", "umzieh*", "umzug", "inostranstv*", "abroad", "ausland",
                   "remote:3", "rad od kuce", "od kuce", "na daljinu", "homeoffice:2", "work from home", "wfh", "hybrid*", "hibrid*",
                   "njemackoj", "njemacku", "germany", "deutschland", "austrij*", "austria", "osterreich", "svicarsk*", "switzerland",
                   "schweiz", "evrop*", "europe", "europa", "eu", "inostran*", "vani"],
    "current": ["trenutn*", "sada", "sad", "current*", "right now", "now", "today", "jetzt", "derzeit", "aktuell*", "gegenwart*",
                "gdje radis", "gdje sada radis", "where do you work", "where are you working", "wo arbeitest du", "zaposlen*",
                "employed", "beschaftigt", "radis li", "do you work", "present"],
    "experience": ["iskust*:1.5", "experience:1.5", "erfahrung*:1.5", "berufserfahrung:2", "radno", "radn* iskust*", "karijer*", "career",
                   "karriere", "work history", "historij*", "posao", "poslovi", "poslova", "poslu", "poslom", "rad", "radio", "radila",
                   "work", "worked", "working", "jobs", "job", "arbeit", "gearbeitet", "beruf*", "firm*", "kompanij*", "compan*",
                   "unternehmen", "employer*", "poslodav*", "arbeitgeber*", "stelle*", "positions", "pozicij*", "radna mjesta",
                   "gdje si radio", "gdje si sve radio", "where have you worked", "where did you work", "wo hast du gearbeitet",
                   "sve firme", "all companies", "nabroj", "spisak", "lista", "list", "alle firmen", "cv:0.5", "lebenslauf:0.5", "resume:0.5"],
    "total_years": ["koliko godina iskustva", "godina iskustva", "godine iskustva", "years of experience", "how many years", "how much experience",
                    "koliko iskustva", "koliko dugo radis", "koliko dugo si u", "wie viele jahre", "jahre erfahrung", "wie lange arbeitest du",
                    "wie viel erfahrung", "ukupno:1.5", "total:1.5", "insgesamt:1.5", "ukupn*"],
    "longest": ["najduz*:3", "longest:3", "am langsten:4", "langste*:3", "najvise vremena", "most time"],
    "first_job": ["prvi posao", "prvo zaposlenje", "first job", "first company", "first employer", "erster job", "erste stelle", "erste arbeit",
                  "ersten job", "prva firma", "pocetak karijere", "start of career", "career start", "karrierebeginn", "kako si poceo", "how did you start"],
    "previous": ["prethodn*", "previous", "prije toga", "before that", "prior", "davor", "vorherig*", "zuvor", "bivs*", "former", "ehemalig*"],
    "job_change": ["pauz*", "rupa", "rupe", "gap", "gaps", "lucke*", "nisi radio", "niste radili", "between jobs", "izmedju poslova",
                   "zasto si otisao", "zasto si napustio", "zasto si mijenjao", "zasto mijenjas", "why did you leave", "why did you quit",
                   "why did you change", "why so many", "warum hast du", "warum gewechselt", "otkaz*", "dao otkaz", "quit", "left", "verlassen",
                   "promjen* posl*:2", "promjen* posa*:2", "mijenja*:2.5", "promijeni*:2", "wechsel*:2", "gewechselt:2.5", "changed:1.5", "switch* jobs:2", "change jobs:2", "changed jobs:2", "job changes:2", "jobwechsel:2",
                   "cesto mijenjas", "mnogo firmi", "many companies", "viele firmen", "viele stellen"],
    "skills": ["vjestin*:1.5", "skill*:1.5", "znanj*", "tech stack", "stack", "tehnolog*", "technolog*", "technik*", "fahigkeit*:1.5",
               "kenntnis*:1.5", "kompetenc*", "kompetenz*", "competenc*", "sta znas", "what do you know", "was kannst du", "sta umijes",
               "alat*", "tools", "werkzeug*", "softver*", "software", "programe", "know how", "expertise", "strucnost", "hard skills",
               "tehnick*", "technical", "technisch*"],
    "programming": ["programir*:1.5", "programming:1.5", "programmier*:1.5", "kodir*", "coding", "code", "kod", "programer*", "developer*",
                    "entwickler*", "programsk* jezi*:2", "programming languages:3", "programmiersprache*:3", "development", "razvoj*", "entwicklung"],
    "ai_cat": ["ai i automatizacij*", "ai and automation", "ki und automatisierung"],
    "devops_cat": ["devops:1.5", "devops i cloud", "devops and cloud"],
    "virt_cat": ["virtualizacij* i infrastruktur*", "virtualization and infrastructure", "infrastruktur*", "infrastructure"],
    "sysadmin_cat": ["sistemsk* administr*:2", "system admin*:2", "sysadmin:2", "systemadministration:2", "administrator*", "admin", "administracij*"],
    "tools_cat": ["specijalizovan* alat*", "specialized tools", "spezialisierte tools"],
    "projects": ["projek*:2", "project*:2", "projekt*:2", "sta si napravio", "sta si izradio", "what have you built", "what did you build",
                 "was hast du gebaut", "portfolio:1.5", "radovi", "side project*", "hobby project*", "privatn* projek*", "personal project*", "demo"],
    "education": ["obrazovanj*", "edukacij*", "skol*", "school", "schule", "ausbildung", "studij*", "studirao", "studium", "studiert",
                  "fakultet*", "university", "univerzitet*", "uni", "degree", "diplom*", "srednj*", "high school", "college", "bildung",
                  "abschluss", "kvalifikacij*", "qualification*", "zvanje", "titula", "masinsk*", "cnc", "konstruktor*", "bachelor", "master"],
    "courses": ["certifikat*", "certificat*", "certificate*", "zertifik*", "kurs*", "course*", "training*", "obuk*", "seminar*", "edukacije",
                "weiterbildung", "fortbildung", "udemy", "coursera", "licenc*", "license*", "istqb", "ccna:0.5", "mcsa", "comptia", "itil"],
    "languages": ["jezik*:1.5", "jezic*:1.5", "language*:1.5", "sprach*:1.5", "govoris", "pricas", "speak", "spoken", "sprichst", "sprechen", "english",
                  "engleski", "engleskog", "englisch", "german", "njemacki", "njemackog", "njemackom", "deutsch", "deutschkenntnisse",
                  "bosanski", "bosanskog", "bosnisch", "bosnian", "hrvatski", "srpski", "croatian", "serbian", "c1", "b1", "b2", "a1", "a2",
                  "nivo", "niveau", "fluent", "tecno", "fliessend", "maternji", "native", "muttersprache"],
    "soft_skills": ["soft skill*:2", "meke vjestine:3", "soft vjestine:3", "komunikac*", "communicat*", "kommunikation*", "timsk*", "team*",
                    "teamwork", "teamarbeit", "osobin*", "personality", "personlichkeit", "kakav si", "kakva si", "what kind of person",
                    "was fur ein mensch", "karakter*", "character", "charakter", "licnost", "interpersonal*", "prilagodljiv*", "adaptab*", "stres*", "stress*", "pritis*", "pressure"],
    "strengths": ["zasto bi", "zasto tebe", "zasto vas", "why should", "why hire", "why you", "warum sollten", "warum dich", "warum sie",
                  "prednost*", "jake strane", "jaka strana", "snag*", "strength*", "starke*", "najbolj*", "best at", "sta te izdvaja",
                  "what makes you", "was macht dich", "vrijednost", "value", "doprinos*", "contribut*", "hire", "hiring", "zaposliti",
                  "zaposlimo", "einstell*", "mehrwert", "unique", "posebn*", "dobar u", "good at", "gut in"],
    "salary": ["plata", "platu", "plate", "placa", "placu", "visina plate", "salary", "salaries", "pay", "paid", "compensation", "money",
               "novac", "novca", "pare", "para", "gehalt*", "lohn", "bezahl*", "koliko trazis", "koliko zelis", "how much do you want",
               "wie viel verdien*", "verdienst", "satnic*", "hourly rate", "rate", "eur", "euro", "km", "netto", "brutto", "gross", "net",
               "primanj*", "zarad*", "earn*", "ocekivanj*", "expectation*", "vorstellung*"],
    "availability": ["dostup*", "available", "availability", "verfugbar*", "kada mozes poceti", "kad mozes poceti", "when can you start",
                     "start date", "wann kannst du", "otkazn* rok*", "notice period", "kundigungsfrist", "poceti", "pocet", "pocnes", "start:1.5",
                     "beginnen", "anfangen", "zapoceti", "ab wann"],
    "job_search": ["trazis li posao", "trazis posao", "looking for a job", "looking for work", "job search", "open to", "otvoren za",
                   "suchst du", "auf jobsuche", "nove prilike", "new opportunit*", "opportunit*", "prilik*", "zainteresovan*", "interested",
                   "interessiert", "freelanc*", "honorar*", "part time", "parttime", "pola radnog", "teilzeit", "full time", "fulltime",
                   "puno radno", "vollzeit", "contract*", "ugovor*", "vertrag", "ponud*", "offer", "angebot", "intervju*", "interview*",
                   "vorstellungsgesprach", "razgovor za posao", "zaposlenje", "employment", "anstellung", "saradnj*", "collaborat*", "zusammenarbeit"],
    "goals": ["cilj*", "goal*", "ziel*", "planov*", "plans", "plane", "buducnost*", "buducnosti", "future", "zukunft", "za 5 godina", "pet godina",
              "five years", "funf jahren", "ambicij*", "ambition*", "motivac*", "motivation", "motiviert", "sta zelis", "what do you want",
              "was willst du", "vision", "vizij*", "fokus*", "focus*", "dream", "san", "strast*", "passion*", "leidenschaft", "zelja", "zelje"],
    "cv_download": ["download:2", "preuzmi*:2", "preuzet*:2", "skini:2", "skinuti:2", "herunterlad*:2", "pdf:2", "posalji cv:3", "send cv:3",
                    "send me your cv", "cv:1", "resume:1", "zivotopis:1.5", "lebenslauf:1", "curriculum vitae"],
    "website": ["ovaj sajt", "ova stranica", "ovu stranicu", "ovaj web", "this site", "this website", "this page", "diese seite",
                "diese webseite", "streamlit:2", "kako je napravljen", "napravljen", "built with", "how was this made", "how is this made",
                "source code", "izvorni kod", "quellcode", "kod sajta"],
    "help": ["pomoc", "pomozi", "help", "hilfe", "sta mogu pitati", "sta da pitam", "what can i ask", "was kann ich fragen", "sta znas raditi",
             "what can you do", "primjer*", "example*", "beispiel*", "menu", "meni", "opcij*", "options", "optionen", "uputstv*", "instructions"],
    "joke": ["vic", "vica", "viceve", "joke*", "witz*", "nasmij*", "funny", "smijesn*", "lustig", "zabav*", "fun"],
    "insult": ["glup*", "stupid", "dumb", "idiot*", "dumm", "los si", "losi", "useless", "beskorist*", "nutzlos", "sucks", "smece", "trash"],
    "datetime": ["koliko je sati", "koji je dan", "koji je datum", "what time is it", "what day is it", "todays date", "wie spat", "welcher tag",
                 "datum danas"],
}

# Aspekti pitanja o konkretnoj firmi
JOB_ASPECTS = {
    "duration": ["koliko:0.8", "koliko si radio", "koliko si bio", "how long were you", "koliko dugo", "koliko si dugo", "koliko vremena", "how long", "wie lange", "trajanj*", "duration", "dauer", "koliko godina:1.5",
                 "how many years", "wie viele jahre"],
    "when": ["kada", "kad", "start*", "poceo", "pocela", "pocetak", "began", "begonnen", "angefangen", "ended", "until", "do kada", "when", "wann", "period*", "zeitraum", "which year*", "koje godine", "godin*:0.5", "year*:0.5", "jahr*:0.5", "od kada", "since"],
    "role": ["pozicij*", "position*", "role", "uloga", "ulog*", "title", "titula", "naziv", "funkcij*", "als was", "kao sta", "as what",
             "which position", "koja pozicija", "radno mjesto"],
    "duties": ["sta si radio", "sta si tamo radio", "sta si radila", "what did you do", "was hast du", "odgovornost*", "responsibilit*",
               "duties", "dutie*", "zadu*", "zadac*", "zadat*", "tasks", "aufgaben", "verantwortung*", "opis posla", "job description",
               "detalj*", "details", "radio si", "posao u", "work at", "arbeit bei", "kakav posao", "what kind of work"],
    "tech": ["tehnolog*", "technolog*", "alat*", "tools", "koristio", "used", "verwendet", "benutzt", "stack"],
    "website": ["web", "website", "sajt", "link", "url", "stranica", "webseite", "homepage"],
    "why_left": ["zasto si otisao", "zasto si napustio", "why did you leave", "why did you quit", "warum hast du", "otisao", "napustio", "left", "quit", "verlassen", "gekundigt"],
}

# Riječi koje znače "nastavak" prethodne teme
FOLLOW_UP = ["a", "and", "und", "i", "tamo", "there", "dort", "onda", "then", "dann", "a tamo", "what about", "how about", "und bei",
             "a u", "a kod", "sta je sa", "a sta", "isto", "also", "same", "jos", "more", "mehr", "detaljnije", "more details", "genauer",
             "nastavi", "continue", "weiter", "o tome", "about that", "daruber", "koliko", "how", "wie"]

INTENT_MATCHER = KeywordMatcher(INTENTS)
ASPECT_MATCHER = KeywordMatcher(JOB_ASPECTS)
COMPANY_MATCHER = KeywordMatcher({job["id"]: job["aliases"] for job in cv.JOBS}, fuzzy_cutoff=0.8)
KNOWLEDGE_MATCHER = KeywordMatcher({item["id"]: item["aliases"] for item in KNOWLEDGE}, fuzzy_cutoff=0.88)
PROJECT_ALIASES = {
    "cvsite": ["ovaj sajt:3", "this site:3", "this website:3", "digital* cv:3", "interaktivn* cv:3", "interactive cv:3", "cv sajt:3", "cv website:3"],
    "helpdesk": ["ticketing:2", "ticket system*:3", "ticketsystem*:3", "tiket*:2", "help desk ticketing:4", "ai help desk:4", "help desk sistem*:3",
                 "helpdesk sistem*:3", "helpdesk system*:3", "help desk system*:3", "ai integracij*:3", "ai integration:3", "ki integration:3"],
    "ailab": ["ai lab:3", "local ai:3", "lokaln* ai:3", "development lab:3", "lab:1.5", "laboratorij*:1.5", "lokaln* okruzenj*:2"],
    "webdev": ["web development portfolio:4", "inteseco:3", "web portfolio:3", "web interfejs*:2", "web interface*:2"],
    "3d": ["3d asset*:3", "asset pipeline:3", "3d pipeline:3", "3d model*:3", "image to 3d:4", "slik* u 3d:4", "iz slik*:2", "rodin3d:2", "dinov3:2", "comfyui:2", "glb:2", "3d:1"],
}
PROJECT_MATCHER = KeywordMatcher(PROJECT_ALIASES, fuzzy_cutoff=0.88)
FOLLOW_UP_SET = set(FOLLOW_UP)


# =============================================================================
# 6. POMOĆNE FUNKCIJE ZA ODGOVORE
# =============================================================================

def L(lang, bs, en, de):
    """Bira tekst na jeziku odgovora."""
    return {"bs": bs, "en": en, "de": de}[lang]


def _months_between(start, end):
    return (end[0] - start[0]) * 12 + (end[1] - start[1])


def _today():
    today = date.today()
    return (today.year, today.month)


def job_months(job):
    # +1 jer se računaju i početni i završni mjesec
    return _months_between(job["start"], job["end"] or _today()) + 1


def format_duration(months, lang):
    years, rest = divmod(months, 12)
    parts = []
    if years:
        parts.append(L(lang,
                       f"{years} {'godina' if years % 10 == 1 and years != 11 else 'godine' if 2 <= years % 10 <= 4 and not 12 <= years <= 14 else 'godina'}",
                       f"{years} year{'s' if years != 1 else ''}",
                       f"{years} Jahr{'e' if years != 1 else ''}"))
    if rest:
        parts.append(L(lang,
                       f"{rest} {'mjesec' if rest == 1 else 'mjeseca' if 2 <= rest <= 4 else 'mjeseci'}",
                       f"{rest} month{'s' if rest != 1 else ''}",
                       f"{rest} Monat{'e' if rest != 1 else ''}"))
    return L(lang, " i ", " and ", " und ").join(parts) if parts else L(lang, "manje od mjesec dana", "less than a month", "weniger als einen Monat")


def total_experience_months(it_only=False):
    """Ukupno iskustvo bez preklapanja perioda."""
    covered = set()
    for job in cv.JOBS:
        if it_only and job["id"] == "ataco":
            continue
        y, m = job["start"]
        end = job["end"] or _today()
        while (y, m) <= end:
            covered.add((y, m))
            m += 1
            if m > 12:
                y, m = y + 1, 1
    return len(covered)


def company_label(job, lang):
    return tr(job["company_name"], lang)


def contact_hint(lang, short=False):
    email = cv.PERSONAL["email"]
    if short:
        return L(lang, f"**{email}** ili **[kontakt forma](/#contact-me)**.", f"**{email}** or the **[contact form](/#contact-me)**.",
                 f"**{email}** oder das **[Kontaktformular](/#contact-me)**.")
    return L(lang,
             f"Za to me najbolje kontaktirajte direktno: **{email}** ili putem **[kontakt forme](/#contact-me)**.",
             f"For that, it's best to contact me directly: **{email}** or via the **[contact form](/#contact-me)**.",
             f"Dafür kontaktieren Sie mich am besten direkt: **{email}** oder über das **[Kontaktformular](/#contact-me)**.")


def knowledge_name(item, lang):
    return tr(item["name"], lang)


def find_evidence(item, max_items=4, query_tokens=None):
    """
    Pronalazi stavke iz opisa poslova koje dokazuju vještinu: [(job, [indeksi])].
    Stavke koje sadrže riječi iz pitanja (npr. "printer") idu prve.
    """
    terms = [t.lower() for t in item.get("evidence", [])]
    if not terms:
        return []
    query = [t for t in (query_tokens or []) if t not in STOPWORDS and len(t) >= 4]

    def relevance(job, i):
        words = {w for lg in LANGS for w in tokenize(normalize(job["duties"][lg][i]))}
        return sum(1 for q in query if any(_token_match(q, w) for w in words))

    results = []
    for job in cv.JOBS:
        idx = [i for i, duty in enumerate(job["duties"]["en"]) if any(re.search(r"\b" + re.escape(t), duty.lower()) for t in terms)]
        if idx:
            idx.sort(key=lambda i: -relevance(job, i))
            results.append((job, idx[:2], relevance(job, idx[0])))
    results.sort(key=lambda r: -r[2])  # stabilno sortiranje čuva hronologiju unutar iste relevantnosti
    return [(job, idx) for job, idx, _ in results[:max_items]]


def job_summary(job, lang, full=True):
    period = format_period(job, lang)
    duration = format_duration(job_months(job), lang)
    role = job_role(job, lang)
    company = company_label(job, lang)
    current = job["end"] is None
    header = L(lang,
               f"U **{company}** {'radim' if current else 'sam radio'} kao **{role}** ({period}, {duration}).",
               f"At **{company}** I {'work' if current else 'worked'} as **{role}** ({period}, {duration}).",
               f"Bei **{company}** {'arbeite' if current else 'arbeitete'} ich als **{role}** ({period}, {duration}).")
    if not full:
        return header
    duties = job["duties"][lang]
    title = L(lang, "Ključne odgovornosti:", "Key responsibilities:", "Hauptaufgaben:")
    lines = "\n".join(f"- {d}" for d in duties)
    return f"{header}\n\n{title}\n{lines}"


# =============================================================================
# 7. ODGOVORI PO NAMJERAMA
# =============================================================================

def answer_greeting(lang, state):
    return random.choice(L(lang,
        ["Zdravo! 👋 Drago mi je. Pitajte me o mom iskustvu, vještinama, projektima ili kako me kontaktirati.",
         "Pozdrav! 😊 Šta vas zanima – radno iskustvo, tehničke vještine ili projekti?"],
        ["Hello! 👋 Nice to meet you. Ask me about my experience, skills, projects or how to contact me.",
         "Hi there! 😊 What would you like to know – work experience, technical skills or projects?"],
        ["Hallo! 👋 Schön, dass Sie da sind. Fragen Sie mich nach meiner Erfahrung, meinen Fähigkeiten, Projekten oder Kontaktdaten.",
         "Guten Tag! 😊 Was interessiert Sie – Berufserfahrung, technische Fähigkeiten oder Projekte?"]))


def answer_farewell(lang, state):
    return L(lang,
             f"Hvala na posjeti! 👋 Ako vas nešto zanima kasnije, tu sam. Možete me kontaktirati i na **{cv.PERSONAL['email']}**.",
             f"Thanks for stopping by! 👋 I'm here if you have more questions. You can also reach me at **{cv.PERSONAL['email']}**.",
             f"Danke für Ihren Besuch! 👋 Bei weiteren Fragen bin ich da. Sie erreichen mich auch unter **{cv.PERSONAL['email']}**.")


def answer_thanks(lang, state):
    return random.choice(L(lang,
        ["Nema na čemu! 😊 Želite li znati još nešto?", "Drago mi je da sam pomogao! Ima li još pitanja?"],
        ["You're welcome! 😊 Anything else you'd like to know?", "Glad I could help! Any other questions?"],
        ["Gern geschehen! 😊 Möchten Sie noch etwas wissen?", "Freut mich, dass ich helfen konnte! Noch weitere Fragen?"]))


def answer_how_are_you(lang, state):
    return L(lang,
             "Odlično, hvala na pitanju! 😊 Spreman sam odgovoriti na sve o mom iskustvu i vještinama. Šta vas zanima?",
             "Great, thanks for asking! 😊 I'm ready to answer anything about my experience and skills. What would you like to know?",
             "Sehr gut, danke der Nachfrage! 😊 Ich beantworte gerne alles zu meiner Erfahrung und meinen Fähigkeiten. Was möchten Sie wissen?")


def answer_bot(lang, state):
    return L(lang,
             "Ja sam Amarov virtualni asistent 🤖. Radim **potpuno offline** – bez interneta i bez vanjskih AI servisa. "
             "Odgovaram u Amarovo ime isključivo na osnovu podataka iz njegovog CV-a, na bosanskom, engleskom i njemačkom.",
             "I'm Amar's virtual assistant 🤖. I run **completely offline** – no internet and no external AI services. "
             "I answer on Amar's behalf strictly based on his CV, in Bosnian, English and German.",
             "Ich bin Amars virtueller Assistent 🤖. Ich arbeite **komplett offline** – ohne Internet und ohne externe KI-Dienste. "
             "Ich antworte in Amars Namen ausschließlich auf Basis seines Lebenslaufs, auf Bosnisch, Englisch und Deutsch.")


def answer_intro(lang, state):
    current = cv.JOBS[0]
    years = total_experience_months() // 12
    return L(lang,
             f"Ja sam **{cv.PERSONAL['name']}**, {cv.PERSONAL['role'][lang]}, iz grada {cv.PERSONAL['location'][lang]}.\n\n"
             f"{cv.PERSONAL['description'][lang]}\n\n"
             f"Trenutno radim u **{company_label(current, lang)}** kao **{job_role(current, lang)}**, a ukupno imam oko **{years} godina** radnog iskustva u {len(cv.JOBS)} firmi.",
             f"I'm **{cv.PERSONAL['name']}**, {cv.PERSONAL['role'][lang]}, based in {cv.PERSONAL['location'][lang]}.\n\n"
             f"{cv.PERSONAL['description'][lang]}\n\n"
             f"I currently work at **{company_label(current, lang)}** as **{job_role(current, lang)}**, with around **{years} years** of work experience across {len(cv.JOBS)} companies.",
             f"Ich bin **{cv.PERSONAL['name']}**, {cv.PERSONAL['role'][lang]}, wohnhaft in {cv.PERSONAL['location'][lang]}.\n\n"
             f"{cv.PERSONAL['description'][lang]}\n\n"
             f"Derzeit arbeite ich bei **{company_label(current, lang)}** als **{job_role(current, lang)}** und habe insgesamt rund **{years} Jahre** Berufserfahrung in {len(cv.JOBS)} Unternehmen.")


def answer_name(lang, state):
    return L(lang,
             f"Zovem se **{cv.PERSONAL['name']}**. 😊",
             f"My name is **{cv.PERSONAL['name']}**. 😊",
             f"Mein Name ist **{cv.PERSONAL['name']}**. 😊")


def bs_years_word(n):
    if n % 10 == 1 and n != 11:
        return "godina"
    if 2 <= n % 10 <= 4 and not 12 <= n <= 14:
        return "godine"
    return "godina"


def current_age():
    day, month, year = (int(x) for x in cv.PERSONAL["birth_date"].split("."))
    today = date.today()
    return today.year - year - ((today.month, today.day) < (month, day))


def answer_age(lang, state):
    birth = cv.PERSONAL["birth_date"]
    age = current_age()
    return L(lang,
             f"Rođen sam **{birth}** ({age} {bs_years_word(age)}). Imam preko 10 godina radnog iskustva, od 2014. godine.",
             f"I was born on **{birth}** ({age} years old). I have over 10 years of work experience, since 2014.",
             f"Ich bin am **{birth}** geboren ({age} Jahre alt). Ich habe über 10 Jahre Berufserfahrung, seit 2014.")


def answer_personal(lang, state):
    return L(lang,
             "To je privatna tema koju ne pokriva moj CV – ovdje se fokusiram na profesionalno iskustvo. 🙂 Pitajte me slobodno o poslu, vještinama ili projektima.",
             "That's a private topic my CV doesn't cover – here I focus on professional experience. 🙂 Feel free to ask about work, skills or projects.",
             "Das ist ein privates Thema, das mein Lebenslauf nicht abdeckt – hier geht es um Berufliches. 🙂 Fragen Sie gerne nach Arbeit, Fähigkeiten oder Projekten.")


def answer_hobbies(lang, state):
    return L(lang,
             "Hobiji nisu posebno navedeni u CV-u, ali u slobodno vrijeme se najviše bavim tehnologijom: "
             "gradio sam **lokalni AI lab** (Ubuntu, Docker, Ollama), eksperimentišem sa **generativnim 3D alatima** (Rodin-3D, DINOv3) "
             "i pravim **web projekte** u Reactu. ",
             "Hobbies aren't listed in my CV, but in my free time I'm mostly into technology: "
             "I built a **local AI lab** (Ubuntu, Docker, Ollama), I experiment with **generative 3D tools** (Rodin-3D, DINOv3) "
             "and build **web projects** with React. ",
             "Hobbys stehen nicht im Lebenslauf, aber in meiner Freizeit beschäftige ich mich vor allem mit Technologie: "
             "Ich habe ein **lokales KI-Labor** aufgebaut (Ubuntu, Docker, Ollama), experimentiere mit **generativen 3D-Tools** (Rodin-3D, DINOv3) "
             "und baue **Webprojekte** mit React. ") + L(lang, "Za ostalo – pitajte me lično. 🙂", "For anything else – just ask me personally. 🙂", "Alles Weitere – fragen Sie mich gerne persönlich. 🙂")


def answer_contact(lang, state):
    email = cv.PERSONAL["email"]
    return L(lang,
             f"Možete me kontaktirati direktno putem emaila: **{email}**.\n\nTakođer, možete popuniti **[kontakt formu na početnoj stranici 'O meni'](/#contact-me)** – poruka mi stiže direktno na mail.",
             f"You can contact me directly via email: **{email}**.\n\nAlternatively, you can fill out the **[contact form on the 'About Me' home page](/#contact-me)** – the message goes straight to my inbox.",
             f"Sie können mich direkt per E-Mail erreichen: **{email}**.\n\nAlternativ können Sie das **[Kontaktformular auf der Startseite 'Über mich'](/#contact-me)** ausfüllen – die Nachricht landet direkt in meinem Postfach.")


def answer_phone(lang, state):
    email = cv.PERSONAL["email"]
    phone = cv.PERSONAL["phone"]
    return L(lang,
             f"Moj broj telefona je **{phone}**. Možete mi pisati i na **{email}** ili putem **[kontakt forme](/#contact-me)**.",
             f"My phone number is **{phone}**. You can also write to **{email}** or use the **[contact form](/#contact-me)**.",
             f"Meine Telefonnummer ist **{phone}**. Sie können mir auch an **{email}** schreiben oder das **[Kontaktformular](/#contact-me)** nutzen.")


def answer_social(lang, state):
    return L(lang,
             "Linkovi na društvene mreže (LinkedIn, GitHub) nisu objavljeni na ovom sajtu. ",
             "Social media links (LinkedIn, GitHub) aren't published on this site. ",
             "Social-Media-Links (LinkedIn, GitHub) sind auf dieser Seite nicht veröffentlicht. ") + contact_hint(lang)


def answer_location(lang, state):
    loc = cv.PERSONAL["location"][lang]
    return L(lang,
             f"Živim u **{loc}**. Za pitanja o preseljenju ili radu na daljinu, slobodno me kontaktirajte na **{cv.PERSONAL['email']}** ili preko **[kontakt forme](/#contact-me)**.",
             f"I live in **{loc}**. For questions about relocation or remote work, feel free to contact me at **{cv.PERSONAL['email']}** or through the **[contact form](/#contact-me)**.",
             f"Ich lebe in **{loc}**. Bei Fragen zu Umzug oder Remote-Arbeit kontaktieren Sie mich gerne unter **{cv.PERSONAL['email']}** oder über das **[Kontaktformular](/#contact-me)**.")


def answer_relocation(lang, state):
    loc = cv.PERSONAL["location"][lang]
    return L(lang,
             f"Trenutno sam u **{loc}**. Imam iskustvo sa uspostavljanjem sistema za **rad na daljinu** (CMS), a engleski govorim na nivou C1. "
             f"O preseljenju, remote ili hibridnom radu najradije razgovaram direktno – **{cv.PERSONAL['email']}** ili **[kontakt forma](/#contact-me)**.",
             f"I'm currently based in **{loc}**. I have experience setting up **remote work systems** (CMS) and speak English at C1 level. "
             f"I'm happy to discuss relocation, remote or hybrid work directly – **{cv.PERSONAL['email']}** or the **[contact form](/#contact-me)**.",
             f"Ich lebe derzeit in **{loc}**. Ich habe Erfahrung mit der Einrichtung von **Remote-Arbeitssystemen** (CMS) und spreche Englisch auf C1-Niveau. "
             f"Über Umzug, Remote- oder Hybridarbeit spreche ich gerne direkt – **{cv.PERSONAL['email']}** oder das **[Kontaktformular](/#contact-me)**.")


def answer_current(lang, state):
    job = cv.JOBS[0]
    state["company"] = job["id"]
    return job_summary(job, lang)


def answer_experience(lang, state):
    years = total_experience_months() // 12
    lines = "\n".join(f"- **{company_label(j, lang)}** ({format_period(j, lang)}): {job_role(j, lang)}" for j in cv.JOBS)
    return L(lang,
             f"Imam oko **{years} godina** radnog iskustva u {len(cv.JOBS)} firmi:\n\n{lines}\n\nZa detalje o firmi pitajte npr. *„Šta si radio u Foreo?”* ili *„Koliko dugo si bio u Payten?”*",
             f"I have around **{years} years** of work experience across {len(cv.JOBS)} companies:\n\n{lines}\n\nFor details, ask e.g. *\"What did you do at Foreo?\"* or *\"How long were you at Payten?\"*",
             f"Ich habe rund **{years} Jahre** Berufserfahrung in {len(cv.JOBS)} Unternehmen:\n\n{lines}\n\nFür Details fragen Sie z. B. *„Was hast du bei Foreo gemacht?”* oder *„Wie lange warst du bei Payten?”*")


def answer_total_years(lang, state):
    total = total_experience_months()
    it_total = total_experience_months(it_only=True)
    first = min(cv.JOBS, key=lambda j: j["start"])
    return L(lang,
             f"Ukupno imam **{format_duration(total, lang)}** radnog iskustva (od {first['start'][1]:02d}/{first['start'][0]}), od čega **{format_duration(it_total, lang)}** u IT-u i tehničkoj podršci.",
             f"In total I have **{format_duration(total, lang)}** of work experience (since {first['start'][1]:02d}/{first['start'][0]}), of which **{format_duration(it_total, lang)}** in IT and technical support.",
             f"Insgesamt habe ich **{format_duration(total, lang)}** Berufserfahrung (seit {first['start'][1]:02d}/{first['start'][0]}), davon **{format_duration(it_total, lang)}** in IT und technischem Support.")


def answer_longest(lang, state):
    job = max(cv.JOBS, key=job_months)
    state["company"] = job["id"]
    return L(lang, "Najduže sam radio u ovoj firmi:\n\n", "The company where I worked the longest:\n\n", "Am längsten habe ich hier gearbeitet:\n\n") + job_summary(job, lang)


def answer_first_job(lang, state):
    job = min(cv.JOBS, key=lambda j: j["start"])
    state["company"] = job["id"]
    return L(lang, "Karijeru sam počeo ovdje:\n\n", "I started my career here:\n\n", "Meine Karriere begann hier:\n\n") + job_summary(job, lang)


def answer_previous(lang, state):
    ids = [j["id"] for j in cv.JOBS]
    current = state.get("company") or ids[0]
    idx = ids.index(current) + 1 if current in ids else 1
    if idx >= len(ids):
        return L(lang, "To je bio moj prvi posao – prije toga sam završio srednju školu (2008–2012).",
                 "That was my first job – before that I finished secondary school (2008–2012).",
                 "Das war meine erste Stelle – davor habe ich die Mittelschule abgeschlossen (2008–2012).")
    job = cv.JOBS[idx]
    state["company"] = job["id"]
    return L(lang, "Prije toga:\n\n", "Before that:\n\n", "Davor:\n\n") + job_summary(job, lang)


def answer_job_change(lang, state):
    return L(lang,
             "Svaka promjena posla bila je dio mog **ličnog i profesionalnog razvoja**. Svjesno sam tražio nova okruženja u kojima mogu učiti, "
             "rasti i graditi sebe kao IT stručnjaka – od korisničke podrške u telekomu i platnom prometu, preko mreža i servera, "
             "do sistemske administracije, DevOps-a i AI automatizacije.\n\n"
             "Svaka firma mi je donijela nova znanja i iskustva koja danas svakodnevno koristim. 🚀",
             "Every job change was part of my **personal and professional growth**. I deliberately looked for new environments where I could learn, "
             "grow and build myself as an IT professional – from customer support in telecom and payments, through networks and servers, "
             "to system administration, DevOps and AI automation.\n\n"
             "Each company gave me new knowledge and experience that I use every day. 🚀",
             "Jeder Jobwechsel war Teil meiner **persönlichen und beruflichen Weiterentwicklung**. Ich habe bewusst neue Umfelder gesucht, in denen ich lernen, "
             "wachsen und mich als IT-Fachmann weiterentwickeln konnte – vom Kundensupport in Telekommunikation und Zahlungsverkehr über Netzwerke und Server "
             "bis hin zu Systemadministration, DevOps und KI-Automatisierung.\n\n"
             "Jedes Unternehmen hat mir neues Wissen und Erfahrungen gebracht, die ich heute täglich nutze. 🚀")


def answer_skills(lang, state):
    lines = "\n".join(cv.skill_category_line(c, lang) for c in cv.SKILL_CATEGORIES)
    soft = ", ".join(cv.SOFT_SKILLS[lang])
    return L(lang,
             f"**Tehničke vještine:**\n\n{lines}\n\n**Soft skills:** {soft}.\n\nPitajte me i za konkretnu tehnologiju, npr. *„Znaš li Docker?”*",
             f"**Technical skills:**\n\n{lines}\n\n**Soft skills:** {soft}.\n\nYou can also ask about a specific technology, e.g. *\"Do you know Docker?\"*",
             f"**Technische Fähigkeiten:**\n\n{lines}\n\n**Soft Skills:** {soft}.\n\nSie können auch nach einer konkreten Technologie fragen, z. B. *„Kennst du Docker?”*")


def answer_skill_category(category_id, lang, state):
    category = next(c for c in cv.SKILL_CATEGORIES if c["id"] == category_id)
    related = [i for i in KNOWLEDGE if i.get("category") == category_id and i.get("projects")]
    projects = sorted({p for i in related for p in i["projects"]}, key=list(cv.PROJECTS_BY_ID).index)
    text = cv.skill_category_line(category, lang)
    if projects:
        text += "\n\n" + L(lang, "Primijenjeno u projektima:", "Applied in projects:", "Angewendet in Projekten:") + "\n" + \
            "\n".join(f"- {cv.project_line(cv.PROJECTS_BY_ID[p], lang)}" for p in projects)
    return text


def answer_knowledge(item, lang, state, query_tokens=None):
    """Odgovor na pitanje o konkretnoj vještini ili oblasti, sa dokazima iz CV-a."""
    state["topic"] = item["id"]
    name = knowledge_name(item, lang)
    category = next((c for c in cv.SKILL_CATEGORIES if c["id"] == item.get("category")), None)
    parts = []

    if item.get("level"):
        parts.append(L(lang, f"Da, **{name}** – {item['level'][lang]}.", f"Yes, **{name}** – {item['level'][lang]}.", f"Ja, **{name}** – {item['level'][lang]}."))
    else:
        parts.append(L(lang, f"Da, imam iskustva sa: **{name}**.", f"Yes, I have experience with **{name}**.", f"Ja, ich habe Erfahrung mit **{name}**."))

    evidence = find_evidence(item, query_tokens=query_tokens)
    if evidence:
        lines = []
        for job, idx in evidence:
            for i in idx:
                lines.append(f"- **{company_label(job, lang)}** ({format_period(job, lang)}): {job['duties'][lang][i]}")
        parts.append(L(lang, "Iz radnog iskustva:", "From my work experience:", "Aus meiner Berufserfahrung:") + "\n" + "\n".join(lines))

    if item.get("projects"):
        lines = "\n".join(f"- {cv.project_line(cv.PROJECTS_BY_ID[p], lang)}" for p in item["projects"])
        parts.append(L(lang, "U projektima:", "In projects:", "In Projekten:") + "\n" + lines)

    if not evidence and not item.get("projects") and category:
        parts.append(L(lang, f"Navedeno u kategoriji **{tr(category['name'], lang)}** mojih vještina.",
                       f"Listed under **{tr(category['name'], lang)}** in my skills.",
                       f"Aufgeführt unter **{tr(category['name'], lang)}** in meinen Fähigkeiten."))

    if item.get("note"):
        parts.append(f"ℹ️ {item['note'][lang]}")
    return "\n\n".join(parts)


def answer_unlisted(tech_name, related_ids, lang, state):
    related = []
    for rid in related_ids:
        if rid in KNOWLEDGE_BY_ID:
            related.append(knowledge_name(KNOWLEDGE_BY_ID[rid], lang))
        else:
            category = next((c for c in cv.SKILL_CATEGORIES if c["id"] == rid), None)
            if category:
                related.append(", ".join(category["items"][lang][:4]))
    related_text = "; ".join(related)
    return L(lang,
             f"**{tech_name}** nije posebno naveden u mom CV-u. Najbliže srodno iskustvo: **{related_text}**. Brzo učim nove tehnologije – za detalje me slobodno kontaktirajte na **{cv.PERSONAL['email']}**.",
             f"**{tech_name}** isn't specifically listed in my CV. The closest related experience: **{related_text}**. I pick up new technologies quickly – feel free to contact me at **{cv.PERSONAL['email']}** for details.",
             f"**{tech_name}** ist in meinem Lebenslauf nicht ausdrücklich aufgeführt. Am nächsten verwandte Erfahrung: **{related_text}**. Ich lerne neue Technologien schnell – kontaktieren Sie mich gerne unter **{cv.PERSONAL['email']}**.")


def answer_projects(lang, state):
    lines = "\n".join(f"- {cv.project_line(p, lang)}" for p in cv.PROJECTS)
    return L(lang, f"Moji ključni projekti:\n\n{lines}", f"My key projects:\n\n{lines}", f"Meine wichtigsten Projekte:\n\n{lines}")


def answer_project(project, lang, state):
    state["project"] = project["id"]
    tech = ", ".join(project["tech"])
    return f"{cv.project_line(project, lang)}\n\n" + L(lang, f"**Tehnologije:** {tech}", f"**Technologies:** {tech}", f"**Technologien:** {tech}")


def answer_education(lang, state, asks_university=False):
    ed = cv.EDUCATION
    text = L(lang,
             f"🎓 **{ed['school'][lang]}** ({ed['years']})\nZvanje: {ed['profession'][lang]}.\n\nDodatno: {', '.join(ed['courses'][lang])}.",
             f"🎓 **{ed['school'][lang]}** ({ed['years']})\nQualification: {ed['profession'][lang]}.\n\nAdditionally: {', '.join(ed['courses'][lang])}.",
             f"🎓 **{ed['school'][lang]}** ({ed['years']})\nAbschluss: {ed['profession'][lang]}.\n\nZusätzlich: {', '.join(ed['courses'][lang])}.")
    if asks_university:
        text += "\n\n" + L(lang,
                           "Fakultet nije naveden u CV-u – moje IT znanje dolazi iz preko 10 godina prakse, samostalnog učenja i projekata.",
                           "A university degree isn't listed in my CV – my IT knowledge comes from over 10 years of hands-on work, self-study and projects.",
                           "Ein Hochschulabschluss ist nicht im Lebenslauf aufgeführt – mein IT-Wissen stammt aus über 10 Jahren Praxis, Selbststudium und Projekten.")
    return text


def answer_courses(lang, state):
    courses = ", ".join(cv.EDUCATION["courses"][lang])
    return L(lang,
             f"Završio sam **{courses}**. Ostali certifikati nisu navedeni u CV-u – većinu znanja sam stekao kroz praksu i projekte. ",
             f"I completed a **{courses}**. Other certifications aren't listed in my CV – most of my knowledge comes from hands-on work and projects. ",
             f"Ich habe einen **{courses}** absolviert. Weitere Zertifikate sind im Lebenslauf nicht aufgeführt – mein Wissen stammt vor allem aus der Praxis und Projekten. ") + contact_hint(lang)


def answer_languages(lang, state):
    langs = "\n".join(f"- {language['label'][lang]}" for language in cv.LANGUAGES)
    return L(lang, f"Govorim sljedeće jezike:\n\n{langs}", f"I speak the following languages:\n\n{langs}", f"Ich spreche folgende Sprachen:\n\n{langs}")


def answer_soft_skills(lang, state):
    soft = ", ".join(cv.SOFT_SKILLS[lang])
    return L(lang,
             f"**Soft skills:** {soft}.\n\nKroz godine rada u korisničkoj podršci (telekom, bankarski POS/ATM, ISP) navikao sam na rad pod pritiskom, jasnu komunikaciju sa korisnicima i timski rad sa tehničarima i razvojnim timovima.",
             f"**Soft skills:** {soft}.\n\nYears of customer-facing support (telecom, banking POS/ATM, ISP) taught me to work under pressure, communicate clearly with users and collaborate with technicians and development teams.",
             f"**Soft Skills:** {soft}.\n\nJahre im Kundensupport (Telekom, Bank-POS/ATM, ISP) haben mich gelehrt, unter Druck zu arbeiten, klar mit Benutzern zu kommunizieren und mit Technikern und Entwicklungsteams zusammenzuarbeiten.")


def answer_strengths(lang, state):
    years = total_experience_months() // 12
    return L(lang,
             f"Šta donosim timu:\n\n"
             f"- **{years}+ godina prakse** – od podrške korisnicima do sistemske administracije (Active Directory, mreže, serveri, sigurnost)\n"
             f"- **Automatizacija** – pišem skripte i koristim alate za automatizaciju, plus AI integracije i AI agente (Gemini API, Ollama, Claude Code)\n"
             f"- **Širina** – telekom, bankarski POS/ATM, ERP, javni sektor, web razvoj (React)\n"
             f"- **Komunikacija** – godine rada direktno sa korisnicima, pisanje dokumentacije i procedura\n"
             f"- **Brzo učenje** – samostalno sam razvio Help Desk sistem sa AI integracijom i lokalnu AI laboratoriju",
             f"What I bring to a team:\n\n"
             f"- **{years}+ years of hands-on work** – from user support to system administration (Active Directory, networks, servers, security)\n"
             f"- **Automation** – I write scripts and use automation tools, plus AI integrations and AI agents (Gemini API, Ollama, Claude Code)\n"
             f"- **Breadth** – telecom, banking POS/ATM, ERP, public sector, web development (React)\n"
             f"- **Communication** – years of working directly with users, writing documentation and procedures\n"
             f"- **Fast learner** – I independently developed a help desk system with AI integration and a local AI lab",
             f"Was ich einem Team biete:\n\n"
             f"- **{years}+ Jahre Praxis** – vom Benutzersupport bis zur Systemadministration (Active Directory, Netzwerke, Server, Sicherheit)\n"
             f"- **Automatisierung** – ich schreibe Skripte und nutze Automatisierungstools, dazu KI-Integrationen und KI-Agenten (Gemini API, Ollama, Claude Code)\n"
             f"- **Bandbreite** – Telekom, Bank-POS/ATM, ERP, öffentlicher Sektor, Webentwicklung (React)\n"
             f"- **Kommunikation** – jahrelange direkte Arbeit mit Benutzern, Erstellung von Dokumentationen und Verfahren\n"
             f"- **Schnelle Auffassungsgabe** – ich habe selbstständig ein Help-Desk-System mit KI-Integration und ein lokales KI-Labor entwickelt")


def answer_salary(lang, state):
    return L(lang, "Plata i uslovi su stvar dogovora i zavise od pozicije. ", "Salary and conditions are negotiable and depend on the position. ",
             "Gehalt und Konditionen sind Verhandlungssache und hängen von der Position ab. ") + contact_hint(lang)


def answer_availability(lang, state):
    return L(lang,
             f"Trenutno sam zaposlen u **{company_label(cv.JOBS[0], lang)}**, pa početak zavisi od otkaznog roka i dogovora. ",
             f"I'm currently employed at **{company_label(cv.JOBS[0], lang)}**, so a start date depends on the notice period and agreement. ",
             f"Ich bin derzeit bei **{company_label(cv.JOBS[0], lang)}** angestellt, daher hängt der Beginn von der Kündigungsfrist und Absprache ab. ") + contact_hint(lang)


def answer_job_search(lang, state):
    return L(lang,
             "Otvoren sam za zanimljive prilike, posebno u oblastima **DevOps**, **sistemske administracije** i **AI automatizacije**. "
             "Za ponude, intervju ili saradnju pišite mi: ",
             "I'm open to interesting opportunities, especially in **DevOps**, **system administration** and **AI automation**. "
             "For offers, interviews or collaboration, write to me: ",
             "Ich bin offen für interessante Möglichkeiten, besonders in den Bereichen **DevOps**, **Systemadministration** und **KI-Automatisierung**. "
             "Für Angebote, Interviews oder Zusammenarbeit schreiben Sie mir: ") + contact_hint(lang, short=True)


def answer_goals(lang, state):
    return L(lang,
             "Moj fokus je unapređenje IT procesa kroz **DevOps prakse** i **AI automatizaciju**. Cilj mi je da od klasične podrške i administracije "
             "pređem na poziciju gdje gradim automatizovane sisteme – kao što je moj Help Desk sistem sa integrisanom AI funkcijom (Gemini API) ili lokalna LLM laboratorija sa Ollamom.",
             "My focus is improving IT workflows through **DevOps practices** and **AI automation**. My goal is to move from classic support and administration "
             "to a role where I build automated systems – like my help desk system with integrated AI (Gemini API) or my local LLM lab with Ollama.",
             "Mein Fokus liegt auf der Optimierung von IT-Abläufen durch **DevOps-Praktiken** und **KI-Automatisierung**. Mein Ziel ist es, vom klassischen Support "
             "und der Administration in eine Rolle zu wechseln, in der ich automatisierte Systeme aufbaue – wie mein Help-Desk-System mit integrierter KI (Gemini API) oder mein lokales LLM-Labor mit Ollama.")


def answer_cv_download(lang, state):
    return L(lang,
             "CV možete preuzeti kao PDF klikom na dugme **⬇️ Preuzmite CV** na stranici **[O meni](/)** – dostupan je na bosanskom, engleskom i njemačkom (prema izabranom jeziku).",
             "You can download my CV as a PDF with the **⬇️ Download CV** button on the **[About Me](/)** page – available in Bosnian, English and German (based on the selected language).",
             "Sie können meinen Lebenslauf als PDF über die Schaltfläche **⬇️ CV herunterladen** auf der Seite **[Über mich](/)** herunterladen – verfügbar auf Bosnisch, Englisch und Deutsch (je nach gewählter Sprache).")


def answer_website(lang, state):
    return L(lang,
             "Ovaj sajt sam napravio u **Pythonu** i **Streamlitu**. Ima tri jezika, kontakt formu sa zaštitom od spama (captcha, limit poruka) "
             "i ovog chatbota koji radi **potpuno offline** – vlastiti sistem za prepoznavanje namjera, tolerantan na greške u kucanju, bez vanjskih API-ja.",
             "I built this site with **Python** and **Streamlit**. It has three languages, a contact form with spam protection (captcha, rate limiting) "
             "and this chatbot, which runs **completely offline** – a custom intent recognition system, tolerant of typos, with no external APIs.",
             "Diese Seite habe ich mit **Python** und **Streamlit** gebaut. Sie hat drei Sprachen, ein Kontaktformular mit Spamschutz (Captcha, Nachrichtenlimit) "
             "und diesen Chatbot, der **komplett offline** läuft – ein eigenes Intent-Erkennungssystem, tolerant gegenüber Tippfehlern, ohne externe APIs.")


def answer_help(lang, state):
    return L(lang,
             "Možete me pitati, na primjer:\n\n"
             "- *Ko si ti?* / *Koliko godina iskustva imaš?*\n- *Gdje trenutno radiš?* / *Šta si radio u Foreo?*\n"
             "- *Koliko dugo si bio u Payten?* / *Šta si radio 2019?*\n- *Znaš li Docker / Python / Active Directory?*\n"
             "- *Imaš li iskustva sa mrežama / sigurnošću / bankarstvom?*\n- *Koji su tvoji projekti?*\n"
             "- *Koje jezike govoriš?* / *Koje je tvoje obrazovanje?*\n- *Zašto bismo te zaposlili?*\n- *Kako te mogu kontaktirati?*",
             "You can ask me, for example:\n\n"
             "- *Who are you?* / *How many years of experience do you have?*\n- *Where do you work now?* / *What did you do at Foreo?*\n"
             "- *How long were you at Payten?* / *What did you do in 2019?*\n- *Do you know Docker / Python / Active Directory?*\n"
             "- *Do you have networking / security / banking experience?*\n- *What are your projects?*\n"
             "- *Which languages do you speak?* / *What is your education?*\n- *Why should we hire you?*\n- *How can I contact you?*",
             "Sie können mich zum Beispiel fragen:\n\n"
             "- *Wer bist du?* / *Wie viele Jahre Erfahrung hast du?*\n- *Wo arbeitest du jetzt?* / *Was hast du bei Foreo gemacht?*\n"
             "- *Wie lange warst du bei Payten?* / *Was hast du 2019 gemacht?*\n- *Kennst du Docker / Python / Active Directory?*\n"
             "- *Hast du Erfahrung mit Netzwerken / Sicherheit / Banken?*\n- *Welche Projekte hast du?*\n"
             "- *Welche Sprachen sprichst du?* / *Welche Ausbildung hast du?*\n- *Warum sollten wir dich einstellen?*\n- *Wie kann ich dich kontaktieren?*")


def answer_joke(lang, state):
    return random.choice(L(lang,
        ["Zašto je sistem administrator ostavio djevojku? Imala je previše *bugova* i nije htjela *update*. 😄",
         "Prvo pravilo IT podrške: *Jeste li probali isključiti i ponovo uključiti?* Drugo pravilo: vidi prvo pravilo. 😄",
         "Postoji 10 vrsta ljudi: oni koji razumiju binarni sistem i oni koji ne razumiju. 😄"],
        ["Why do sysadmins never get lost? They always follow the *route*. 😄",
         "First rule of IT support: *Have you tried turning it off and on again?* Second rule: see rule one. 😄",
         "There are 10 types of people: those who understand binary and those who don't. 😄"],
        ["Erste Regel im IT-Support: *Haben Sie es schon aus- und wieder eingeschaltet?* Zweite Regel: siehe erste Regel. 😄",
         "Es gibt 10 Arten von Menschen: die, die Binär verstehen, und die, die es nicht tun. 😄",
         "Warum gehen Admins nie verloren? Sie folgen immer der richtigen *Route*. 😄"]))


def answer_insult(lang, state):
    return L(lang,
             "Žao mi je ako odgovor nije bio od pomoći. 🙏 Pokušajte preformulisati pitanje ili napišite *pomoć* da vidite šta sve mogu odgovoriti.",
             "Sorry if my answer wasn't helpful. 🙏 Try rephrasing the question or type *help* to see what I can answer.",
             "Entschuldigung, wenn die Antwort nicht hilfreich war. 🙏 Formulieren Sie die Frage um oder schreiben Sie *Hilfe*, um zu sehen, was ich beantworten kann.")


def answer_datetime(lang, state):
    today = date.today().strftime("%d.%m.%Y")
    return L(lang, f"Danas je **{today}**. 📅 Mogu li vam pomoći oko nečega iz mog CV-a?",
             f"Today is **{today}**. 📅 Can I help you with anything from my CV?",
             f"Heute ist der **{today}**. 📅 Kann ich Ihnen mit etwas aus meinem Lebenslauf helfen?")


def answer_year(year, lang, state):
    """Šta je Amar radio određene godine."""
    jobs = [j for j in cv.JOBS if j["start"][0] <= year <= (j["end"] or _today())[0]]
    if 2008 <= year <= 2012 and not jobs:
        return L(lang, f"U {year}. sam se školovao – **{cv.EDUCATION['school'][lang]}** ({cv.EDUCATION['years']}).",
                 f"In {year} I was in school – **{cv.EDUCATION['school'][lang]}** ({cv.EDUCATION['years']}).",
                 f"{year} war ich in der Schule – **{cv.EDUCATION['school'][lang]}** ({cv.EDUCATION['years']}).")
    if not jobs:
        return L(lang, f"Za {year}. godinu nemam podataka u CV-u. Moje radno iskustvo počinje 2014. godine.",
                 f"I have no CV data for {year}. My work experience starts in 2014.",
                 f"Für {year} habe ich keine Daten im Lebenslauf. Meine Berufserfahrung beginnt 2014.")
    if len(jobs) == 1:
        state["company"] = jobs[0]["id"]
    lines = "\n\n".join(job_summary(j, lang, full=False) for j in jobs)
    return L(lang, f"U {year}. godini:\n\n{lines}", f"In {year}:\n\n{lines}", f"Im Jahr {year}:\n\n{lines}")


def answer_job(job, aspect, lang, state):
    state["company"] = job["id"]
    state["aspect"] = aspect
    company = company_label(job, lang)
    period = format_period(job, lang)
    current = job["end"] is None
    if aspect == "duration":
        duration = format_duration(job_months(job), lang)
        return L(lang,
                 f"U **{company}** {'radim već' if current else 'sam radio'} **{duration}** ({period}).",
                 f"I {'have been working' if current else 'worked'} at **{company}** for **{duration}** ({period}).",
                 f"Bei **{company}** {'arbeite ich seit' if current else 'habe ich'} **{duration}** {'' if current else 'gearbeitet '}({period}).".replace("  ", " "))
    if aspect == "when":
        return L(lang, f"U **{company}** {'radim od' if current else 'sam radio u periodu'}: **{period}**.",
                 f"I {'have worked' if current else 'worked'} at **{company}** during: **{period}**.",
                 f"Bei **{company}** {'arbeite ich seit' if current else 'war ich im Zeitraum'}: **{period}**.")
    if aspect == "role":
        role = job_role(job, lang)
        return L(lang, f"U **{company}** {'radim' if current else 'sam radio'} kao **{role}** ({period}). Sektor: {tr(job['sector'], lang)}.",
                 f"At **{company}** I {'work' if current else 'worked'} as **{role}** ({period}). Sector: {tr(job['sector'], lang)}.",
                 f"Bei **{company}** {'arbeite' if current else 'arbeitete'} ich als **{role}** ({period}). Branche: {tr(job['sector'], lang)}.")
    if aspect == "website":
        if job.get("url"):
            return L(lang, f"Web stranica firme **{company}**: {job['url']}", f"Website of **{company}**: {job['url']}", f"Webseite von **{company}**: {job['url']}")
        return L(lang, f"Za **{company}** nemam objavljen link.", f"I don't have a published link for **{company}**.", f"Für **{company}** habe ich keinen veröffentlichten Link.")
    if aspect == "tech":
        found = [knowledge_name(item, lang) for item in KNOWLEDGE
                 if any(j["id"] == job["id"] for j, _ in find_evidence(item, max_items=20))]
        if found:
            return L(lang, f"U **{company}** sam radio sa: **{', '.join(found)}**.\n\n", f"At **{company}** I worked with: **{', '.join(found)}**.\n\n",
                     f"Bei **{company}** habe ich gearbeitet mit: **{', '.join(found)}**.\n\n") + job_summary(job, lang)
    if aspect == "why_left":
        if current:
            return L(lang, f"U **{company}** još uvijek radim.", f"I'm still working at **{company}**.", f"Ich arbeite noch bei **{company}**.")
        return L(lang,
                 f"Iz **{company}** sam otišao radi daljeg **ličnog i profesionalnog razvoja** – želio sam novo okruženje u kojem mogu još više učiti "
                 f"i graditi sebe. Iskustvo koje sam stekao u **{company}** ({format_period(job, lang)}) i danas mi je vrijedan temelj.",
                 f"I left **{company}** for further **personal and professional growth** – I wanted a new environment where I could keep learning "
                 f"and building myself. The experience I gained at **{company}** ({format_period(job, lang)}) is still a valuable foundation for me.",
                 f"Ich habe **{company}** für meine weitere **persönliche und berufliche Entwicklung** verlassen – ich wollte ein neues Umfeld, in dem ich "
                 f"weiter lernen und mich weiterentwickeln kann. Die Erfahrung bei **{company}** ({format_period(job, lang)}) ist bis heute eine wertvolle Grundlage.")
    return job_summary(job, lang)


# =============================================================================
# 8. PRETRAGA CIJELOG CV-a (kad nijedna namjera ne odgovara)
# =============================================================================

def _build_documents():
    docs = []  # (tekstovi po jeziku, oznaka izvora)
    for job in cv.JOBS:
        for i in range(len(job["duties"]["en"])):
            docs.append(({lg: job["duties"][lg][i] for lg in LANGS}, ("job", job["id"])))
    for project in cv.PROJECTS:
        docs.append(({lg: f"{tr(project['name'], lg)}: {project['description'][lg]}" for lg in LANGS}, ("project", project["id"])))
    for category in cv.SKILL_CATEGORIES:
        docs.append(({lg: cv.skill_category_line(category, lg) for lg in LANGS}, ("skills", category["id"])))
    docs.append(({lg: cv.PERSONAL["description"][lg] for lg in LANGS}, ("about", None)))
    docs.append(({lg: " ".join(cv.education_lines(lg)) for lg in LANGS}, ("education", None)))
    return docs


_DOCUMENTS = _build_documents()
_DOC_TOKENS = [{lg: {t for t in tokenize(normalize(texts[lg])) if t not in STOPWORDS} for lg in LANGS} for texts, _ in _DOCUMENTS]


def _token_match(query_token, doc_token):
    """Poklapanje uz toleranciju na padeže/nastavke: 'mreza' ~ 'mreznih', 'printer' ~ 'printers'."""
    if query_token == doc_token:
        return True
    if len(query_token) < 4 or len(doc_token) < 4:
        return False
    common = len(os.path.commonprefix([query_token, doc_token]))
    needed = max(4, min(6, min(len(query_token), len(doc_token)) - 2))
    return common >= needed


def search_cv(tokens, lang, limit=4):
    query = [t for t in tokens if t not in STOPWORDS and (len(t) >= 3 or t.isdigit())]
    if not query:
        return []
    n_docs = len(_DOCUMENTS)
    # Rijetke riječi nose više težine (jednostavan IDF)
    doc_freq = {q: sum(1 for d in _DOC_TOKENS if any(_token_match(q, t) for lg in LANGS for t in d[lg])) for q in query}
    scored = []
    for i, doc in enumerate(_DOC_TOKENS):
        score = 0.0
        for q in query:
            if doc_freq[q] and any(_token_match(q, t) for lg in LANGS for t in doc[lg]):
                score += 1.0 + (n_docs / doc_freq[q]) ** 0.5 / 3
        if score:
            scored.append((score, i))
    scored.sort(reverse=True)
    if not scored or scored[0][0] < 1.8:
        return []
    best = scored[0][0]
    return [i for score, i in scored[:limit] if score >= best * 0.6]


def answer_search(doc_indices, lang, state):
    lines = []
    for i in doc_indices:
        texts, (kind, ref) = _DOCUMENTS[i]
        if kind == "job":
            job = cv.JOBS_BY_ID[ref]
            lines.append(f"- **{company_label(job, lang)}** ({format_period(job, lang)}): {texts[lang]}")
            state["company"] = ref
        else:
            lines.append(f"- {texts[lang]}")
    return L(lang, "Evo šta sam pronašao u svom CV-u o tome:\n\n", "Here's what I found in my CV about that:\n\n",
             "Folgendes habe ich dazu in meinem Lebenslauf gefunden:\n\n") + "\n".join(lines)


def answer_fallback(lang, state):
    return L(lang,
             "Hmm, na to pitanje nemam odgovor u svom CV-u. 🤔 Mogu vam reći o mom **radnom iskustvu**, **vještinama**, **projektima**, "
             "**edukaciji**, **jezicima** ili kako me **kontaktirati**. Napišite *pomoć* za primjere pitanja.\n\n" + contact_hint(lang),
             "Hmm, I don't have an answer to that in my CV. 🤔 I can tell you about my **work experience**, **skills**, **projects**, "
             "**education**, **languages** or how to **contact** me. Type *help* for example questions.\n\n" + contact_hint(lang),
             "Hmm, darauf habe ich in meinem Lebenslauf keine Antwort. 🤔 Ich kann Ihnen etwas über meine **Berufserfahrung**, **Fähigkeiten**, **Projekte**, "
             "**Ausbildung**, **Sprachen** oder **Kontaktmöglichkeiten** erzählen. Schreiben Sie *Hilfe* für Beispielfragen.\n\n" + contact_hint(lang))


SIMPLE_HANDLERS = {
    "greeting": answer_greeting, "farewell": answer_farewell, "thanks": answer_thanks, "how_are_you": answer_how_are_you,
    "bot": answer_bot, "intro": answer_intro, "name": answer_name, "age": answer_age, "personal": answer_personal,
    "hobbies": answer_hobbies, "contact": answer_contact, "phone": answer_phone, "social": answer_social,
    "location": answer_location, "relocation": answer_relocation, "current": answer_current, "experience": answer_experience,
    "total_years": answer_total_years, "longest": answer_longest, "first_job": answer_first_job, "previous": answer_previous,
    "job_change": answer_job_change, "skills": answer_skills, "projects": answer_projects, "courses": answer_courses,
    "education": answer_education,
    "languages": answer_languages, "soft_skills": answer_soft_skills, "strengths": answer_strengths,
    "salary": answer_salary, "availability": answer_availability,
    "job_search": answer_job_search, "goals": answer_goals, "cv_download": answer_cv_download, "website": answer_website,
    "help": answer_help, "joke": answer_joke, "insult": answer_insult, "datetime": answer_datetime,
}

CATEGORY_INTENTS = {"programming": "programming", "ai_cat": "ai", "devops_cat": "devops", "virt_cat": "virtualization",
                    "sysadmin_cat": "sysadmin", "tools_cat": "tools"}

# Namjere koje se mogu kombinovati u jednom odgovoru ("vještine i jezici")
COMBINABLE = {"skills", "languages", "education", "projects", "contact", "location", "soft_skills", "courses", "experience",
              "total_years", "current", "salary", "availability", "goals", "strengths", "hobbies"}

SOCIAL_INTENTS = {"greeting", "farewell", "thanks", "how_are_you"}


# =============================================================================
# 9. GLAVNA FUNKCIJA
# =============================================================================

MAX_INPUT_LENGTH = 500


def respond(text, ui_language="English", state=None):
    """
    Generiše odgovor na pitanje.
    text: pitanje korisnika
    ui_language: jezik iz sidebara ("Bosanski" / "English" / "Deutsch")
    state: rječnik za kontekst razgovora (čuvati u st.session_state između poruka)
    """
    if state is None:
        state = {}
    text = (text or "").strip()[:MAX_INPUT_LENGTH]

    fallback_lang = state.get("lang") or cv.lang_code(ui_language)
    lang, confidence = detect_language(text, fallback=fallback_lang)
    if confidence == 0:
        lang = fallback_lang
    state["lang"] = lang

    tokens = tokenize(normalize(text))
    if not tokens:
        return answer_help(lang, state)

    intents = INTENT_MATCHER.match(tokens)
    aspects = ASPECT_MATCHER.match(tokens)
    companies = COMPANY_MATCHER.match(tokens)
    knowledge = KNOWLEDGE_MATCHER.match(tokens)
    projects = PROJECT_MATCHER.match(tokens)
    unlisted = [UNLISTED_TECH[t] for t in tokens if t in UNLISTED_TECH]
    years = [int(t) for t in tokens if t.isdigit() and 2000 <= int(t) <= 2035]

    # "the", "see" itd. ne smiju aktivirati SEE Contact: traži se fraza "see contact"
    company_ids = sorted(companies, key=companies.get, reverse=True)

    # Uljudni prefiks ako poruka počinje pozdravom, a sadrži i pitanje
    greeting_prefix = ""
    content_intents = {k: v for k, v in intents.items() if k not in SOCIAL_INTENTS}
    has_content = bool(content_intents or company_ids or knowledge or projects or unlisted or years)
    social = [k for k in intents if k in SOCIAL_INTENTS]
    if social and not has_content:
        top_social = max(social, key=intents.get)
        return SIMPLE_HANDLERS[top_social](lang, state)
    if "greeting" in intents and has_content:
        greeting_prefix = L(lang, "Zdravo! 👋 ", "Hello! 👋 ", "Hallo! 👋 ")

    def finish(answer, intent=None):
        state["intent"] = intent
        return greeting_prefix + answer

    top_aspect = max(aspects, key=aspects.get) if aspects else None
    is_follow_up = len(tokens) <= 5 and (tokens[0] in FOLLOW_UP_SET or bool(aspects))

    # --- 1. Pitanje o konkretnoj firmi ---
    if company_ids and not (content_intents.get("experience", 0) >= 3 and len(company_ids) > 2):
        answers = []
        for cid in company_ids[:3]:
            aspect = top_aspect
            # "A u Payten?" -> isti aspekt kao prethodno pitanje
            if aspect is None and len(tokens) <= 4 and state.get("aspect"):
                aspect = state["aspect"]
            answers.append(answer_job(cv.JOBS_BY_ID[cid], aspect, lang, state))
        return finish("\n\n---\n\n".join(answers), "job")

    # --- 2. Pitanje o godini ("Šta si radio 2019?") ---
    if years and not knowledge:
        return finish("\n\n".join(answer_year(y, lang, state) for y in years[:2]), "year")

    # --- 3. Nastavak razgovora o firmi ("A koliko dugo?") ---
    strong_intent = max(content_intents.values()) if content_intents else 0
    if state.get("company") and top_aspect and strong_intent < 1.5 and not knowledge and not projects:
        return finish(answer_job(cv.JOBS_BY_ID[state["company"]], top_aspect, lang, state), "job")

    # --- 4. Konkretan projekat ---
    if projects and (max(projects.values()) >= 2 or "projects" in intents):
        project_id = max(projects, key=projects.get)
        return finish(answer_project(cv.PROJECTS_BY_ID[project_id], lang, state), "project")

    # --- 5. Tehnologije koje nisu na CV-u ---
    if unlisted and not knowledge:
        return finish("\n\n".join(answer_unlisted(name, rel, lang, state) for name, rel in unlisted[:2]), "unlisted")

    # --- 6. Kategorija vještina ("programiranje", "devops") ---
    category_hits = {CATEGORY_INTENTS[k]: v for k, v in intents.items() if k in CATEGORY_INTENTS}
    if category_hits and max(category_hits.values()) >= 1.5 and not (knowledge and max(knowledge.values()) >= 1):
        best_category = max(category_hits, key=category_hits.get)
        if best_category != "sysadmin" or "skills" in intents or max(category_hits.values()) >= 2:
            return finish(answer_skill_category(best_category, lang, state), "category")

    # --- 7. Konkretna vještina ili oblast ("Znaš li Docker?", "iskustvo sa mrežama") ---
    if knowledge:
        # Lične/kontakt teme imaju prednost nad slučajnim poklapanjem (npr. "remote" u pitanju o preseljenju)
        priority = {"relocation", "contact", "salary", "availability", "languages", "education", "location", "phone",
                    "website", "bot", "job_search", "goals", "strengths", "cv_download"}
        top_intent = max(content_intents, key=content_intents.get) if content_intents else None
        if not (top_intent in priority and content_intents[top_intent] >= max(knowledge.values()) + 1):
            items = sorted(knowledge, key=knowledge.get, reverse=True)[:3]
            answer = "\n\n---\n\n".join(answer_knowledge(KNOWLEDGE_BY_ID[i], lang, state, tokens) for i in items)
            if unlisted:
                answer += "\n\n---\n\n" + "\n\n".join(answer_unlisted(name, rel, lang, state) for name, rel in unlisted[:2])
            return finish(answer, "knowledge")

    # --- 8. Opšte namjere ---
    if content_intents:
        ranked = sorted(content_intents.items(), key=lambda kv: kv[1], reverse=True)
        top, top_score = ranked[0]

        # Posebni slučajevi
        if top in CATEGORY_INTENTS:
            return finish(answer_skill_category(CATEGORY_INTENTS[top], lang, state), "category")
        if top == "education":
            asks_uni = any(t.startswith(("fakultet", "univerz", "universit", "studij", "studir", "studium", "degree", "bachelor", "master", "uni"))
                           for t in tokens)
            if "courses" in content_intents and content_intents["courses"] >= top_score:
                return finish(answer_courses(lang, state), "courses")
            return finish(answer_education(lang, state, asks_uni), "education")
        if "previous" in content_intents and state.get("company"):
            return finish(answer_previous(lang, state), "previous")
        if top == "experience" and "total_years" in content_intents:
            return finish(answer_total_years(lang, state), "total_years")
        if top == "age" and ("experience" in content_intents or "total_years" in content_intents):
            return finish(answer_total_years(lang, state), "total_years")
        if top in ("location", "current") and content_intents.get("current", 0) and ("experience" in content_intents):
            return finish(answer_current(lang, state), "current")

        if top_score >= 0.5:
            answer = SIMPLE_HANDLERS[top](lang, state)
            # Drugo pitanje u istoj poruci ("vještine i jezici")
            if len(ranked) > 1 and top in COMBINABLE:
                second, second_score = ranked[1]
                if second in COMBINABLE and second_score >= 1.5 and second_score >= top_score * 0.7 \
                        and {top, second} not in ({"experience", "total_years"}, {"experience", "current"}):
                    answer += "\n\n---\n\n" + SIMPLE_HANDLERS[second](lang, state)
            return finish(answer, top)

    # --- 9. Nastavak bez jasne teme ("A detaljnije?") ---
    if is_follow_up and state.get("company"):
        return finish(answer_job(cv.JOBS_BY_ID[state["company"]], top_aspect, lang, state), "job")
    if is_follow_up and state.get("topic") in KNOWLEDGE_BY_ID:
        return finish(answer_knowledge(KNOWLEDGE_BY_ID[state["topic"]], lang, state), "knowledge")

    # --- 10. Pretraga cijelog CV-a ---
    hits = search_cv(tokens, lang)
    if hits:
        return finish(answer_search(hits, lang, state), "search")

    return finish(answer_fallback(lang, state), "fallback")


def greeting_message(ui_language):
    lang = cv.lang_code(ui_language)
    return L(lang,
             "Zdravo! Ja sam Amarov virtualni asistent. Kako vam mogu pomoći? Možete me pitati o mom iskustvu, vještinama ili projektima.",
             "Hello! I am Amar's virtual assistant. How can I help you today? You can ask me about my experience, skills, or projects.",
             "Hallo! Ich bin Amars virtueller Assistent. Wie kann ich Ihnen heute helfen? Sie können mich nach meiner Erfahrung, meinen Fähigkeiten oder Projekten fragen.")
