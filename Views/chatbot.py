import requests
import streamlit as st
import time

# Postavi Gemini API ključ i endpoint
gemini_api_key = st.secrets["gemini"]["api_key"]
gemini_endpoint = "https://gemini.googleapis.com/v1beta/chat"

def get_gemini_response(messages):
    print("Sending request to Gemini API...")
    headers = {
        "Authorization": f"Bearer {gemini_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": messages,
        "max_tokens": 150
    }
    try:
        response = requests.post(gemini_endpoint, headers=headers, json=data)
        response.raise_for_status()
        print("Received response from Gemini API.")
        response_data = response.json()
        
        # Proverite strukturu odgovora
        if 'choices' in response_data and len(response_data['choices']) > 0:
            return response_data['choices'][0].get('message', {}).get('content', '').strip()
        else:
            st.error("Unexpected response format.")
            return "Unexpected response format."
    except requests.exceptions.HTTPError as e:
        st.error("HTTP error occurred while contacting Gemini API.")
        print(f"HTTPError: {e}")
        return "An error occurred while contacting the Gemini API."
    except requests.exceptions.RequestException as e:
        st.error("An error occurred while sending the request.")
        print(f"RequestException: {e}")
        return "An unexpected error occurred."
    except ValueError as e:
        st.error("Failed to parse response JSON.")
        print(f"ValueError: {e}")
        return "Failed to parse response JSON."
    except Exception as e:
        st.error("An unexpected error occurred.")
        print(f"Error: {e}")
        return "An unexpected error occurred."
    return None

st.title("Chatbot")

# Inicijalizacija chat istorije
if "messages" not in st.session_state:
    st.session_state.messages = []

# Prikaz chat poruka iz istorije na ponovno učitavanje aplikacije
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Prihvati korisnički unos
if prompt := st.chat_input("What is up?"):
    # Dodaj korisničku poruku u istoriju chat-a
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Prikaz korisničke poruke u chat message kontejneru
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prikaz odgovora asistenta u chat message kontejneru
    with st.chat_message("assistant"):
        # Pripremi sve poruke za API poziv
        response = get_gemini_response(st.session_state.messages)
        st.markdown(response)  # Prikaz konačnog odgovora
        # Dodaj odgovor asistenta u istoriju chat-a
        st.session_state.messages.append({"role": "assistant", "content": response})
