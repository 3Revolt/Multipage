import random
import time
import streamlit as st

def generate_response(messages):
    bosnian_keywords = [
        "radno iskustvo", "gdje si radio", "See Contact", "2014", "koje godine si radio u BH Telecom",
        "telecom", "Telinvest", "koje godine si radio u Telinvest", "2015",
        "koje godine si radio u logosoftu", "koje godine si radio u ataco",
        "ataco", "logosoft", "koje godine si radio u foreo",
        "koje godine si radio u logosoftu", "logosoft", "payten",
        "koje godine si radio u capital market solutions", "koje godine si radio u payten",
        "CMS", "foreo", "poslovi", "koji su tvoji budući planovi",
        "planovi", "sada", "kako da te kontaktiram", "kontakt",
        "kako se zoves", "ime"
    ]
    german_keywords = [
        "arbeitsplätze", "wo hast du gearbeitet", "See Contact", "2014",
        "in welchem jahr haben sie bei BH Telecom gearbeitet", "telecom",
        "Telinvest", "in welchem jahr haben sie bei telinvest gearbeitet",
        "in welchem jahr haben sie bei payten gearbeitet", "in welchem jahr haben sie bei ataco gearbeitet",
        "ataco", "in welchem jahr haben sie bei logosoft gearbeitet", "logosoft",
        "in welchem jahr haben sie bei foreo gearbeitet", "foreo",
        "in welchem jahr haben sie bei capital markt solutions gearbeitet", "CMS",
        "was sind deine zukunftspläne", "pläne", "sada", "wie kann ich dich kontaktieren", "kontakt",
        "wie heißt du", "name"
    ]
    english_keywords = [
        "where have you worked", "See Contact", "2014",
        "what year did you work at BH Telecom", "telecom", "Telinvest",
        "what year did you work at telinvest", "what year did you work at Ataco",
        "ataco", "what year did you work at payten", "payten",
        "what year did you work at foreo", "what year did you work at Logosoft",
        "logosoft", "foreo", "capital market solutions", "CMS", "right now",
        "what are your future plans", "plans", "how can i contact you",
        "contact", "what is your name", "name"
    ]

    for msg in messages:
        content = msg["content"].lower()

        # Prepoznaj ime
        if any(keyword in content for keyword in ["kako se zoves", "ime"]) and any(keyword in content for keyword in bosnian_keywords):
            return "Moje ime je Amar Helac"
        if any(keyword in content for keyword in ["wie heißt du", "name"]) and any(keyword in content for keyword in german_keywords):
            return "Mein Name ist Amar Helac"
        if any(keyword in content for keyword in ["what is your name", "name"]) and any(keyword in content for keyword in english_keywords):
            return "My name is Amar Helac"

        # Prepoznaj buduće planove
        if any(keyword in content for keyword in ["koji su tvoji budući planovi", "planovi", "cilje"]) and any(keyword in content for keyword in bosnian_keywords):
            return "Imam veliki interes da se bavim konkretnije Devops dijelom te svi moji planovi vode ka tom cilju"
        if any(keyword in content for keyword in ["was sind deine zukunftspläne", "pläne", "Ziel"]) and any(keyword in content for keyword in german_keywords):
            return "Ich habe ein großes Interesse daran, mich konkreter mit dem Devops-Teil auseinanderzusetzen, und alle meine Pläne führen auf dieses Ziel hin"
        if any(keyword in content for keyword in ["what are your future plans", "plans", "goal"]) and any(keyword in content for keyword in english_keywords):
            return "I have a great interest in dealing more specifically with the Devops part, and all my plans lead to that goal"

        # Prepoznaj radno mesto
        if any(keyword in content for keyword in ["koje godine si radio u BH Telecom", "telecom"]) and any(keyword in content for keyword in bosnian_keywords):
            return "U kompaniji BH Telecom sam radio u periodu od 08/2014 do 12/2014 gdje sam bio na poziciji Technical Support za Residential korisnike, o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in ["in welchem jahr haben sie bei BH Telecom gearbeitet", "telecom"]) and any(keyword in content for keyword in german_keywords):
            return "Ich habe im Zeitraum von 01/2015 bis 07/2015 bei der Firma BH Telecom gearbeitet, wo ich die Position des technischen Supports für Privatanwender innehatte. Informationen zu dieser Position finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in ["what year did you work at BH Telecom", "telecom"]) and any(keyword in content for keyword in english_keywords):
            return "I worked in the BH Telecom company in the period from 01/2015 to 07/2015 where I was in the position of Technical Support for Residential users, you can find about this position on the about me page."


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

        # Ako se pitanje odnosi na radno mesto 1
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koje godine si radio u foreo", "foreo"]):
            return "U kompaniji Foreo sam radio u periodu od 11/2021 do 02/2024 gdje sam bio na poziciji IT support specialist te kasnije Sys admin. Detaljnije o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["in welchem jahr haben sie bei foreo gearbeitet", "foreo"]):
            return "Ich habe im Zeitraum von 11/2021 bis 02/2024 bei der Firma Foreo gearbeitet, wo ich als IT-Supportspezialist und später als Systemadministrator tätig war. Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what year did you work at foreo", "foreo"]):
            return "I worked at the company Foreo in the period from 11/2021 to 02/2024 where I was in the position of IT support specialist and later Sys admin. You can find more details about this position on the about me page"

        # Ako se pitanje odnosi na radno mesto 2
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koje godine si radio u logosoftu", "logosoft"]):
            return "U kompaniji Logosoft sam radio u periodu od 10/2020 do 11/2021 gdje sam bio na poziciji tehničke podrške za rezidencijalne korisnike te dodatne poslove. Detaljnije o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["in welchem jahr haben sie bei logosoft gearbeitet", "logosoft"]):
            return "Ich habe im Zeitraum von 10/2020 bis 11/2021 bei Logosoft gearbeitet, wo ich die Position des technischen Supports für Privatanwender und zusätzlicher Aufgaben innehatte. Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what year did you work at logosoft", "logosoft"]):
            return "I worked at Logosoft in the period from 10/2020 to 11/2021 where I was in the position of technical support for residential users and additional tasks. You can find more details about this position on the about me page"

        # Ako se pitanje odnosi na radno mesto 3
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koje godine si radio u capital market solutions", "capital market solutions", "CMS"]):
            return "U kompaniji Capital Market Solutions sam radio u periodu od 06/2020 do 10/2020 gdje sam bio na poziciji IT Scientist. Detaljnije o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["in welchem jahr haben sie bei capital market solutions gearbeitet", "capital market solutions", "CMS"]):
            return "Ich habe im Zeitraum von 06/2020 bis 10/2020 bei Capital Market Solutions gearbeitet, wo ich die Position des IT-Wissenschaftlers innehatte. Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what year did you work at capital market solutions", "capital market solutions", "CMS"]):
            return "I worked at Capital Market Solutions in the period from 06/2020 to 10/2020 where I was in the position of IT Scientist. You can find more details about this position on the about me page"

        # Ako se pitanje odnosi na radno mesto 4
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koje godine si radio u payten", "payten"]):
            return "U kompaniji Payten sam radio u periodu od 03/2019 do 02/2020 gdje sam bio na poziciji Tehnička podrška za POS terminale i ATM uređaje. Detaljnije o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["in welchem jahr haben sie bei payten gearbeitet", "payten"]):
            return "Ich habe im Zeitraum von 03/2019 bis 02/2020 bei Payten gearbeitet, wo ich die Position des technischen Supports für POS-Terminals und Geldautomaten innehatte. Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what year did you work at payten", "payten"]):
            return "I worked at Payten in the period from 03/2019 to 02/2020 where I was in the position of Technical Support for POS terminals and ATM devices. You can find more details about this position on the about me page"
        # Ako se pitanje odnosi na radno mesto 5
        if any(keyword in content for keyword in bosnian_keywords) and any(keyword in content for keyword in ["koje godine si radio u ataco", "ataco"]):
            return "U kompaniji Ataco sam radio u periodu od 09/2018 do 03/2019 gdje sam bio na poziciji Tehnička podrška. Detaljnije o navednoj poziciji možete pronaći na stranici about me"
        if any(keyword in content for keyword in german_keywords) and any(keyword in content for keyword in ["in welchem jahr haben sie bei ataco gearbeitet", "ataco"]):
            return "Ich habe im Zeitraum von 09/2018 bis 03/2019 bei Ataco gearbeitet, wo ich die Position des technischen Supports innehatte. Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich."
        if any(keyword in content for keyword in english_keywords) and any(keyword in content for keyword in ["what year did you work at ataco", "ataco"]):
            return "I worked at Ataco in the period from 09/2018 to 03/2019 where I was in the position of Technical Support. You can find more details about this position on the about me page"
        
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
        
            # Ako nijedna ključna reč nije pronađena, možeš vratiti neku generičku poruku na sve tri jezike
    return (
        "Nisam pronašao relevantne ključne reči u porukama.Nažalost trenutno nisam podešen za neku napredniju konverzaciju već samo vezano za moj CV.Pokušatje kao npr: Koje godine si radio u Foreo.\n"  # Bosanski
        "I could not find relevant keywords in the messages.I am not currently set up for a more advanced conversation, but only related to my CV.Attempts such as: What year did you work at Foreo.\n"  # Engleski
        "Ich konnte keine relevanten Schlüsselwörter in den Nachrichten finden.Leider bin ich derzeit nicht auf ein weiterführendes Gespräch eingestellt, sondern nur auf meinen Lebenslauf bezogen.Versuche wie: In welchem ​​Jahr haben Sie bei Foreo gearbeitet?"  # Nemački
    )

# Streamlit aplikacija
st.title("Chat Bot")

user_input = st.text_input("Unesite svoje pitanje:")
if st.button("Pošalji"):
    if user_input:
        with st.spinner("Bot odgovara..."):
            response = generate_response([{"content": user_input}])
            st.write(response)
    else:
        st.warning("Molimo unesite pitanje.")