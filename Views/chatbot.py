import openai
import streamlit as st
import time

st.title("ChatGPT-like Clone")

# Load OpenAI API key
try:
    openai.api_key = st.secrets["openai"]["OPEN_API_KEY"]
except KeyError as e:
    st.error(f"API key not found: {e}")
    st.stop()

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"  # or "text-davinci-003"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
prompt = st.chat_input("What is up")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Retry logic for rate limits
        retries = 5
        for attempt in range(retries):
            try:
                for response in openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                ):
                    full_response += response.choices[0].delta.get("content", "")
                    message_placeholder.markdown(full_response + "|")
                break  # Break the loop if successful
            except openai.error.RateLimitError as e:
                st.warning(f"Rate limit exceeded. Retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt)  # Exponential backoff
            except openai.error.OpenAIError as e:
                st.error(f"OpenAI API error: {e}")
                st.stop()

        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
