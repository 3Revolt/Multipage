import streamlit as st
from transformers import pipeline

# Učitaj model za prepoznavanje jezika
language_detector = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def detect_language(content):
    labels = ["bosnian", "german", "english"]
    result = language_detector(content, candidate_labels=labels)
    return result['labels'][0]

def generate_response(content, language):
    job_positions = {
        "foreo": {
            "bosnian": "U kompaniji Foreo sam radio u periodu od 11/2021 do 02/2024 gdje sam bio na poziciji IT support specialist te kasnije Sys admin. Detaljnije o navednoj poziciji možete pronaći na stranici about me",
            "german": "Ich habe im Zeitraum von 11/2021 bis 02/2024 bei der Firma Foreo gearbeitet, wo ich als IT-Supportspezialist und später als Systemadministrator tätig war. Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich.",
            "english": "I worked at the company Foreo in the period from 11/2021 to 02/2024 where I was in the position of IT support specialist and later Sys admin. You can find more details about this position on the about me page"},
        "logosoft": {
            "bosnian": "U kompaniji Logosoft sam radio u periodu od 10/2020 do 11/2021 gdje sam bio na poziciji tehničke podrške za rezidencijalne korisnike te dodatne poslove. Detaljnije o navednoj poziciji možete pronaći na stranici about me",
            "german": "Ich habe im Zeitraum von 10/2020 bis 11/2021 bei Logosoft gearbeitet, wo ich die Position des technischen Supports für Privatanwender und zusätzlicher Aufgaben innehatte. Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich.",
            "english": "I worked at Logosoft in the period from 10/2020 to 11/2021 where I was in the position of technical support for residential users and additional tasks. You can find more details about this position on the about me page"},
            "capital market solutions": ("U kompaniji Capital Market Solutions sam radio u periodu od 06/2020 do 10/2020 gdje sam bio na poziciji IT Scientist. Detaljnije o navednoj poziciji možete pronaći na stranici about me",
                                         "Ich habe im Zeitraum von 06/2020 bis 10/2020 bei Capital Market Solutions gearbeitet, wo ich die Position des IT-Wissenschaftlers innehatte. Weitere Details zu dieser Stelle finden Sie auf der Seite Über mich.",
                                         "I worked at Capital Market Solutions in the period from 06/2020 to 10/2020 where I was in the position of IT Scientist. You can find more details about this position on the about me page"),
            "payten": ("U kompaniji Payten sam radio u periodu od 03/2019 do 02/2020 gdje sam bio na poziciji Tehnička podrška za POS terminale i ATM uređaje. Detaljnije o navednoj poziciji možete pronaći na stranici about me",
                       "Ich habe im Zeitraum von 03/2019 bis 02/2020 bei Payten gearbeitet, wo ich die Position des technischen Supports für POS-Terminals und Geldautomatengeräte innehatte. Weitere Details zu dieser Position finden Sie auf der Seite Über mich.",
                       "I worked at Payten in the period from 03/2019 to 02/2020, where I held the position of Technical support for POS terminals and ATM devices. You can find more details about this position on the about me page"),
            "ataco": ("U kompaniji Ataco sam radio u periodu od 09/2017 do 03/2018 gdje sam bio na poziciji Dostavljača i komercijaliste. Detaljnije o navednoj poziciji možete pronaći na stranici about me",
                      "Ich habe im Zeitraum von 09/2017 bis 03/2018 bei Ataco gearbeitet, wo ich die Position des Liefer- und Kaufmanns innehatte. Weitere Details zu dieser Position finden Sie auf der Seite Über mich.",
                      "I worked at Ataco in the period from 09/2017 to 03/2018, where I was in the position of Delivery and Commercialist. You can find more details about this position on the about me page"),
            "telinvest": ("U kompaniji Telinvest sam radio u periodu od 07/2015 do 09/2017 gdje sam bio na poziciji tehničke podrške za business korisnike, o navednoj poziciji možete pronaći na stranici about me",
                          "Ich habe im Zeitraum von 07/2015 bis 09/2017 bei Telinvest gearbeitet, wo ich die Position des technischen Supports für Geschäftsanwender innehatte. Informationen zu dieser Position finden Sie auf der Seite Über mich.",
                          "I worked at Telinvest in the period from 07/2015 to 09/2017, where I held the position of Technical support for business users. Information about this position can be found on the about me page")
        }

    for position, responses in job_positions.items():
        if position in content.lower():
            return responses.get(language, "Sorry, I don't understand your request.")
    
    return "Sorry, I don't understand your request."

# Example Streamlit app
st.title("Chat Bot")
st.write("Ask me anything about my work experience!")

user_input = st.text_input("Your question:")
if st.button("Submit"):
    with st.spinner("Generating response..."):
        language = detect_language(user_input)
        response = generate_response(user_input, language)
        st.write(response)