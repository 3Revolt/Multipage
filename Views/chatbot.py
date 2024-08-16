import openai
import streamlit as st
import time

# Postavi OpenAI API ključ
openai.api_key = st.secrets["openai"]["OPEN_API_KEY"]

def get_chatgpt_response(messages):
    print("Sending request to OpenAI API...")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )
        print("Received response from OpenAI API.")
        return response.choices[0].message['content'].strip()
    except openai.error.RateLimitError as e:
        st.error("Rate limit exceeded. Please wait and try again.")
        print(f"RateLimitError: {e}")
        time.sleep(20)  # Povećano kašnjenje pre nego što ponovo pokušate
        return "Rate limit exceeded. Please try again later."
    except openai.error.OpenAIError as e:
        st.error("An OpenAI error occurred.")
        print(f"OpenAIError: {e}")
        return "An error occurred with the OpenAI API."
    except Exception as e:
        st.error("An error occurred while processing the request.")
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
        response = get_chatgpt_response(st.session_state.messages)
        if response:
            st.markdown(response)  # Prikaz konačnog odgovora
            # Dodaj odgovor asistenta u istoriju chat-a
            st.session_state.messages.append({"role": "assistant", "content": response})
