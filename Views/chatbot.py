import requests
import streamlit as st

# Retrieve Hugging Face API key from secrets.toml
hf_api_key = st.secrets["huggingface"]["api_key"]
hf_endpoint = "https://api-inference.huggingface.co/models/distilgpt2"  # Replace with your actual model

def get_hf_response(messages):
    headers = {
        "Authorization": f"Bearer {hf_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "inputs": {
            "past_user_inputs": [msg["content"] for msg in messages if msg["role"] == "user"],
            "generated_responses": [msg["content"] for msg in messages if msg["role"] == "assistant"],
            "text": messages[-1]["content"]
        },
        "parameters": {
            "max_length": 150,
            "top_p": 0.95,
            "temperature": 0.9
        }
    }
    try:
        response = requests.post(hf_endpoint, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        if 'generated_text' in response_data:
            return response_data['generated_text'].strip()
        else:
            st.error("Unexpected response format.")
            return "Unexpected response format."
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP error occurred while contacting Hugging Face API: {e.response.status_code} - {e.response.text}")
        print(f"HTTPError: {e.response.status_code} - {e.response.text}")
        return "An error occurred while contacting the Hugging Face API."
    except requests.exceptions.RequestException as e:
        st.error(f"RequestException: {e}")
        print(f"RequestException: {e}")
        return "An unexpected error occurred."
    except ValueError as e:
        st.error(f"ValueError: {e}")
        print(f"ValueError: {e}")
        return "Failed to parse response JSON."
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        print(f"Error: {e}")
        return "An unexpected error occurred."
    return None

st.title("Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history on app reload
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Prepare all messages for API call
        response = get_hf_response(st.session_state.messages)
        st.markdown(response)  # Display final response
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
