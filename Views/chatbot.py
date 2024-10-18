import streamlit as st


# --- BACKGROUND IMAGE ---
page_bg_img = """
<style>
body, html {
    margin: 0;
    padding: 0;
    height: 100%;
}

body {
    background-image: url("https://t3.ftcdn.net/jpg/07/66/87/68/360_F_766876856_XDPvm1sg90Ar5Hwf1jRRIHM4FNCXmhKj.jpg");
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



# Definiši funkciju za generisanje odgovora
def generate_response(messages):
    # Definiši ključne reči za različite jezike
    bosnian_keywords = [
        "radno iskustvo", "See Contact", "2014", "koje godine si radio u BH Telecom", "telecom", "Telinvest",
        "koje godine si radio u Telinvest", "2015", "koje godine si radio u logosoftu", "koje godine si radio u ataco",
        "ataco", "logosoft", "koje godine si radio u foreo", "koje godine si radio u logosoftu", "logosoft", "payten",
        "koje godine si radio u capital market solutions", "koje godine si radio u payten", "CMS",  "poslovi",
        "koji su tvoji budući planovi", "planovi", "gdje si radio", "radio", "sada", "kako da te kontaktiram", "kontakt",
        "kako se zoves", "ime", "Kako si?", "kako si ti?", "šta ima?", "šta radiš?", "gdje trenutno radiš"
    ]
    german_keywords = [
        "arbeitsplätze", "See Contact", "2014", "in welchem jahr haben sie bei BH Telecom gearbeitet", "telecom",
        "Telinvest", "in welchem jahr haben sie bei telinvest gearbeitet", "in welchem jahr haben sie bei payten gearbeitet",
        "in welchem jahr haben sie bei ataco gearbeitet", "ataco", "in welchem jahr haben sie bei capital markt solutions gearbeitet",
        "CMS", "payten", "logosoft", "in welchem jahr haben sie bei foreo gearbeitet", "in welchem jahr haben sie bei logosoft gearbeitet",
        "logosoft", "in welchem jahr haben sie bei capital market solutions gearbeitet", "CMS", "arbeitserfahrung",
        "was sind deine zukunftspläne", "pläne", "arbeiten", "im augenblick", "wo hast du gearbeitet", "wie kann ich dich kontaktieren",
        "kontakt", "wie heißt du", "name", "Wie geht es dir?", "Was geht?", "was machst du gerade?", "wo sie derzeit arbeiten"
    ]
    english_keywords = [
        "where have you worked", "See Contact", "2014", "Telinvest", "what year did you work at BH Telecom", "telecom",
        "2015", "what year did you work at telinvest", "what year did you work at Ataco", "ataco", "what year did you work at payten",
        "payten", "what year did you work at foreo", "what year did you work at Logosoft", "what year did you work at capital market solutions",
        "logosoft", "foreo", "capital market solutions", "CMS", "right now", "what are your future plans", "plans",
        "where did you work", "how can i contact you", "contact", "what is your name", "name", "How are you?", "What's up?", "What are you doing?",
        "where are you currently working"
    ]

    # Definiši odgovore za različite pozicije
    job_positions = {
        "foreo": ("U kompaniji Foreo sam radio u periodu od 11/2021 do 02/2024 gdje sam bio na poziciji IT support specialist te kasnije Sys admin. Detaljnije o navednoj poziciji možete pronaći na stranici about me",
                  "Ich habe im Zeitraum von 11/2021 bis 02/2024 bei der Firma Foreo gearbeitet, wo ich als IT-Supportspezialist und später als Systemadministrator tätig war. Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich.",
                  "I worked at the company Foreo in the period from 11/2021 to 02/2024 where I was in the position of IT support specialist and later Sys admin. You can find more details about this position on the about me page"),
        "logosoft": ("U kompaniji Logosoft sam radio u periodu od 10/2020 do 11/2021 gdje sam bio na poziciji tehničke podrške za rezidencijalne korisnike te dodatne poslove. Detaljnije o navednoj poziciji možete pronaći na stranici about me",
                     "Ich habe im Zeitraum von 10/2020 bis 11/2021 bei Logosoft gearbeitet, wo ich die Position des technischen Supports für Privatanwender und zusätzlicher Aufgaben innehatte. Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich.",
                     "I worked at Logosoft in the period from 10/2020 to 11/2021 where I was in the position of technical support for residential users and additional tasks. You can find more details about this position on the about me page"),
        "capital market solutions": ("U kompaniji Capital Market Solutions sam radio u periodu od 06/2020 do 10/2020 gdje sam bio na poziciji IT Scientist. Detaljnije o navednoj poziciji možete pronaći na stranici about me",
                                     "Ich habe im Zeitraum von 06/2020 bis 10/2020 bei Capital Market Solutions gearbeitet, wo ich die Position des IT-Wissenschaftlers innehatte. Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich.",
                                     "I worked at Capital Market Solutions in the period from 06/2020 to 10/2020 where I was in the position of IT Scientist. You can find more details about this position on the about me page"),
        "payten": ("U kompaniji Payten sam radio u periodu od 03/2019 do 02/2020 gdje sam bio na poziciji Tehnička podrška za POS terminale i ATM uređaje. Detaljnije o navednoj poziciji možete pronaći na stranici about me",
                   "Ich habe im Zeitraum von 03/2019 bis 02/2020 bei Payten gearbeitet, wo ich die Position des technischen Supports für POS-Terminals und Geldautomatengeräte innehatte. Weitere Details zu dieser Position finden Sie auf der Seite Über mich.",
                   "I worked at Payten in the period from 03/2019 to 02/2020, where I held the position of Technical support for POS terminals and ATM devices. You can find more details about this position on the about me page"),
        "ataco": ("U kompaniji Ataco sam radio u periodu od 09/2017 do 03/2018 gdje sam bio na poziciji Dostavljača i komercijaliste. Detaljnije o navednoj poziciji možete pronaći na stranici about me",
                  "Ich habe im Zeitraum von 09/2017 bis 03/2018 bei Ataco gearbeitet, wo ich die Position des Liefer- und Kaufmanns innehatte. Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich.",
                  "I worked at Ataco in the period from 09/2017 to 03/2018, where I was in the position of Delivery and Commercialist. You can find more details about this position on the about me page"),
        "telinvest": ("U kompaniji Telinvest sam radio u periodu od 07/2015 do 09/2017 gdje sam bio na poziciji tehničke podrške za business korisnike, o navednoj poziciji možete pronaći na stranici about me",
                      "Ich habe im Zeitraum von 07/2015 bis 09/2017 bei Telinvest gearbeitet, wo ich die Position des technischen Supports für Geschäftsanwender innehatte. Informationen zu dieser Position finden Sie auf der Seite Über mich.",
                      "I worked at Telinvest in the period from 07/2015 to 09/2017, where I held the position of Technical support for business users. Information about this position can be found on the about me page")
    }

    # Prolazi kroz sve poruke
     # Prolazi kroz sve poruke
    for msg in messages:
        content = msg["content"].lower()

        # Ako se pitanje odnosi na ime na bilo kojem jeziku
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["kako se zoves", "ime"]):
            return "Moje ime je Amar Helac"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["wie heißt du", "name"]):
            return "Mein Name ist Amar Helac"
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what is your name", "name"]):
            return "My name is Amar Helac"

        # Ako se pitanje odnosi na buduće planove
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koji su tvoji budući planovi", "planovi", "cilje"]):
            return "Imam veliki interes da se bavim konkretnije Devops dijelom te svi moji planovi vode ka tom cilju"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["was sind deine zukunftspläne", "pläne", "Ziel"]):
            return "Ich habe ein großes Interesse daran, mich konkreter mit dem Devops-Teil auseinanderzusetzen, und alle meine Pläne führen auf dieses Ziel hin"
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what are your future plans", "plans", "goal"]):
            return "I have a great interest in dealing more specifically with the Devops part, and all my plans lead to that goal"

        # Ako se pitanje odnosi na određeno radno mesto 1
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koje godine si radio u foreo", "foreo"]):
            return "U kompaniji Foreo sam radio u periodu od 11/2021 do 02/2024 gdje sam bio na poziciji IT support specialist te kasnije Sys admin.Detaljnije o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["in welchem jahr haben sie bei foreo gearbeitet", "foreo"]):
            return "Ich habe im Zeitraum von 11/2021 bis 02/2024 bei der Firma Foreo gearbeitet, wo ich als IT-Supportspezialist und später als Systemadministrator tätig war.Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what year did you work at foreo", "foreo"]):
            return "I worked at the company Foreo in the period from 11/2021 to 02/2024 where I was in the position of IT support specialist and later Sys admin.You can find more details about this position on the about me page"

        # Ako se pitanje odnosi na određeno radno mesto 2
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koje godine si radio u logosoftu", "logosoft"]):
            return "U kompaniji Logosoft sam radio u periodu od 10/2020 do 11/2021 gdje sam bio na poziciji tehničke podrške za rezidencijalne korisnike te dodatne poslove.Detaljnije o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["in welchem jahr haben sie bei logosoft gearbeitet", "logosoft"]):
            return "Ich habe im Zeitraum von 10/2020 bis 11/2021 bei Logosoft gearbeitet, wo ich die Position des technischen Supports für Privatanwender und zusätzlicher Aufgaben innehatte.Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what year did you work at logosoft", "logosoft"]):
            return "I worked at Logosoft in the period from 10/2020 to 11/2021 where I was in the position of technical support for residential users and additional tasks.You can find more details about this position on the about me page"

        # Ako se pitanje odnosi na određeno radno mesto 3
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koje godine si radio u capital market solutions", "capital market solutions", "CMS"]):
            return "U kompaniji Capital Market Solutions sam radio u periodu od 06/2020 do 10/2020 gdje sam bio na poziciji IT Scientist.Detaljnije o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["in welchem jahr haben sie bei capital market solutions gearbeitet", "capital market solutions", "CMS"]):
            return "Ich habe im Zeitraum von 06/2020 bis 10/2020 bei Capital Market Solutions gearbeitet, wo ich die Position des IT-Wissenschaftlers innehatte.Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what year did you work at capital market solutions", "capital market solutions", "CMS"]):
            return "I worked at Capital Market Solutions in the period from 06/2020 to 10/2020 where I was in the position of IT Scientist.You can find more details about this position on the about me page"

        # Ako se pitanje odnosi na određeno radno mesto 4
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koje godine si radio u payten", "payten"]):
            return "U kompaniji Payten sam radio u periodu od 03/2019 do 02/2020 gdje sam bio na poziciji Tehnička podrška za POS terminale i ATM uređaje.Detaljnije o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["in welchem jahr haben sie bei payten gearbeitet", "payten"]):
            return "Ich habe im Zeitraum von 03/2019 bis 02/2020 bei Payten gearbeitet, wo ich die Position des technischen Supports für POS-Terminals und Geldautomatengeräte innehatte. Weitere Details zu dieser Position finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what year did you work at payten", "payten"]):
            return "I worked at Payten in the period from 03/2019 to 02/2020, where I held the position of Technical support for POS terminals and ATM devices. You can find more details about this position on the about me page"

        # Ako se pitanje odnosi na određeno radno mesto 5
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koje godine si radio u Ataco", "Ataco"]):
            return "U kompaniji Payten sam radio u periodu od 09/2017 do 03/2018 gdje sam bio na poziciji Dostavljača i komercijaliste.Detaljnije o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["in welchem jahr haben sie bei Ataco gearbeitet", "Ataco"]):
            return "Ich habe im Zeitraum von 09/2017 bis 03/2018 bei Payten gearbeitet, wo ich die Position des Liefer- und Kaufmanns innehatte. Weitere Details zu dieser Position finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what year did you work at Ataco","2017", "2018", "Ataco"]):
            return "I worked at Payten in the period from 09/2017 to 03/2018, where I was in the position of Delivery and Commercialist. You can find more details about this position on the about me page"


        # Ako se pitanje odnosi na određeno radno mesto 6
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koje godine si radio u Telinvest", "Telinvest"]):
            return "U kompaniji Telinvest sam radio u periodu od 07/2015 do 09/2017 gdje sam bio na poziciji tehničke podrške za business korisnike, o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["in welchem jahr haben sie bei Telinvest gearbeitet", "Telinvest"]):
            return "Ich habe im Zeitraum von 07/2015 bis 09/2017 bei Telinvest gearbeitet, wo ich die Position des technischen Supports für Geschäftsanwender innehatte. Informationen zu dieser Position finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what year did you work at Telinvest","2015", "Telinvest"]):
            return "I worked at Telinvest in the period from 07/2015 to 09/2017 where I was in the position of technical support for business users, you can find about this position on the about me page"


        # Ako se pitanje odnosi na određeno radno mesto 7
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koje godine si radio u BH Telecom", "telecom"]):
            return "U kompaniji BH Telecom sam radio u periodu od 08/2014 do 12/2014 gdje sam bio na poziciji Technical Support za Residential korisnike, o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["in welchem jahr haben sie bei BH Telecom gearbeitet", "telecom"]):
            return "Ich habe im Zeitraum von 01/2015 bis 07/2015 bei der Firma BH Telecom gearbeitet, wo ich die Position des technischen Supports für Privatanwender innehatte. Informationen zu dieser Position finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what year did you work at BH Telecom", "telecom"]):
            return "I worked in the BH Telecom company in the period from 01/2015 to 07/2015 where I was in the position of Technical Support for Residential users, you can find about this position on the about me page."


        # Ako se pitanje odnosi na određeno radno mesto 8
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koje godine si radio u See Contact", "2014", "See Contact"]):
            return "U kompaniji See Contact sam radio u periodu od 01/2015 do 07/2015 gdje sam bio na poziciji Technical Support za Residential korisnike, o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["in welchem jahr haben sie bei See Contact gearbeitet", "2014", "See Contact"]):
            return "Ich habe im Zeitraum von 01/2015 bis 07/2015 bei See Contact gearbeitet, wo ich die Position des technischen Supports für Privatanwender innehatte. Informationen zu dieser Position finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what year did you work at See Contact","2014", "See Contact"]):
            return "I worked at See Contact in the period from 01/2015 to 07/2015 where I was in the position of Technical Support for Residential users, you can find about the said position on the about me page."

        # Ako se pitanje odnosi na pitanje kako si?
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["Kako si?", "kako si ti?"]):
            return "Dobro sam hvala na pitanju. Nažalost trenutno nisam podešen za neku napredniju konverzaciju već samo vezano za moj CV."
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["Wie geht es dir?", "Wie geht es dir"]):
            return "Mir geht es gut, danke der Nachfrage. Leider bin ich derzeit nicht auf ein weiterführendes Gespräch eingestellt, sondern nur auf meinen Lebenslauf bezogen."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["How are you?", "how are you"]):
            return "I'm good thanks for asking. Unfortunately, I am not currently set up for a more advanced conversation, but only related to my CV."

        # Ako se pitanje odnosi na pitanje šta ima?
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["šta ima?", "šta radiš?"]):
            return "Nažalost trenutno nisam podešen za neku napredniju konverzaciju već samo vezano za moj CV."
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["Was geht?", "was machst du gerade?"]):
            return "Leider bin ich derzeit nicht auf ein weiterführendes Gespräch eingestellt, sondern nur auf meinen Lebenslauf bezogen."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["What's up? ", "What are you doing?"]):
            return "I am not currently set up for a more advanced conversation, but only related to my CV."


        # Ako se pitanje odnosi gdje sada radis
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["gdje trenutno radiš", "sada"]):
            return "Trenutno radim u Federalnom zavodu za zapošljavanje kao referent IT podrške.Detaljnije o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["wo sie derzeit arbeiten", "im augenblick"]):
            return "Derzeit arbeite ich bei der Bundesagentur für Arbeit als IT-Betreuer.Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["where are you currently working", "right now"]):
            return "I currently work at the Federal Employment Agency as an IT support officer.You can find more details about this position on the about me page"

        # Ako se pitanje odnosi na radno iskustvo na bosanskom jeziku
        if any(keyword in content for keyword in bosnian_keywords):
            if any(keyword in content for keyword in ["kako da te kontaktiram", "kontakt"]):
                return "Možete me kontaktirati na stranici About Me u sekciji Contact Me ili direktno na mail: amar.helac@outlook.com"
            return (
                "Moje radno iskustvo u nastavku:\n"
                "- **Foreo**: IT Support Specialist (11/2021 - Present)\n"
                "- **Logosoft**: Technical Support Provider for Residential Users (10/2020 - 11/2021)\n"
                "- **Capital Market Solutions**: IT Scientist (06/2020 - 10/2020)\n"
                "- **Payten**: Help Desk POS Support Associate (03/2019 - 02/2020)\n"
                "- **Ataco Commerce**: Commercialist (09/2017 - 03/2018)\n"
                "- **Telinvest**: Technical Support for Business Users (07/2015 - 09/2017)\n"
                "- **BH Telecom Sarajevo**: Technical Support for Residential Users (01/2015 - 07/2015)\n"
                "- **See Contact**: Technical Support for Residential Users (08/2014 - 12/2014)"
            )

        # Ako se pitanje odnosi na radno iskustvo na nemačkom jeziku
        if any(keyword in content for keyword in german_keywords):
            if any(keyword in content for keyword in ["wie kann ich dich kontaktieren", "kontakt"]):
                return "Sie können mich über die Seite About Me im Bereich Contact Me oder direkt per E-Mail kontaktieren: amar.helac@outlook.com"
            return (
                "Hier ist eine Zusammenfassung meiner Berufserfahrung:\n"
                "- **Foreo**: IT-Support-Spezialist (11/2021 – heute)\n"
                "- **Logosoft**: Technischer Support-Anbieter für Privatanwender (10/2020 – 11/2021)\n"
                "- **Capital Market Solutions**: Informatiker (06/2020 – 10/2020)\n"
                "- **Payten**: Helpdesk-POS-Supportmitarbeiter (03/2019 – 02/2020)\n"
                "- **Ataco Commerce**: Kaufmann (09/2017 – 03/2018)\n"
                "- **Telinvest**: Technischer Support für Geschäftsanwender (07/2015 – 09/2017)\n"
                "- **BH Telecom Sarajevo**: Technischer Support für Privatanwender (01/2015 – 07/2015)\n"
                "- **See Contact**: Technischer Support für Privatanwender (08/2014 – 12/2014)"
            )

        # Ako se pitanje odnosi na radno iskustvo na engleskom jeziku
        if any(keyword in content for keyword in english_keywords):
            if any(keyword in content for keyword in ["how can i contact you", "contact"]):
                return "You can contact me via the About Me page in the Contact Me section or directly via email: amar.helac@outlook.com"
            return (
                "Here is a summary of my work experience:\n"
                "- **Foreo**: IT Support Specialist (11/2021 - Present)\n"
                "- **Logosoft**: Technical Support Provider for Residential Users (10/2020 - 11/2021)\n"
                "- **Capital Market Solutions**: IT Scientist (06/2020 - 10/2020)\n"
                "- **Payten**: Help Desk POS Support Associate (03/2019 - 02/2020)\n"
                "- **Ataco Commerce**: Commercialist (09/2017 - 03/2018)\n"
                "- **Telinvest**: Technical Support for Business Users (07/2015 - 09/2017)\n"
                "- **BH Telecom Sarajevo**: Technical Support for Residential Users (01/2015 - 07/2015)\n"
                "- **See Contact**: Technical Support for Residential Users (08/2014 - 12/2014)"
            )

    # Ako nijedna ključna reč nije pronađena, možeš vratiti neku generičku poruku na sve tri jezike
    return (
        "Nisam pronašao relevantne ključne reči u porukama.Nažalost trenutno nisam podešen za neku napredniju konverzaciju već samo vezano za moj CV.Pokušatje kao npr: Koje godine si radio u Foreo.\n"  # Bosanski
        "I could not find relevant keywords in the messages.I am not currently set up for a more advanced conversation, but only related to my CV.Attempts such as: What year did you work at Foreo.\n"  # Engleski
        "Ich konnte keine relevanten Schlüsselwörter in den Nachrichten finden.Leider bin ich derzeit nicht auf ein weiterführendes Gespräch eingestellt, sondern nur auf meinen Lebenslauf bezogen.Versuche wie: In welchem ​​Jahr haben Sie bei Foreo gearbeitet?"  # Nemački
    )

# Postavi HTML i CSS za stilizaciju
st.markdown(
    """
    <style>
    .chatbot-title {
        color: #d33682; /* Promijeni ovu boju po želji */
        font-size: 36px; /* Promijeni veličinu fonta po želji */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Naslov sa primjenjenim stilom
st.markdown('<h1 class="chatbot-title">Chatbot</h1>', unsafe_allow_html=True)

# Polje za unos pitanja
user_input = st.text_input("Unesite vaše pitanje:")

# Dugme za slanje pitanja
if st.button("Pošalji"):
    if user_input:
        # Pozovi funkciju za generisanje odgovora
        response = generate_response([{"content": user_input}])
        st.write("Odgovor: ", response)
    else:
        st.write("Molimo unesite pitanje.")
