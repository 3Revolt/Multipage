import streamlit as st
from transformers import pipeline

# Initialize the pipeline with the specific model
model_name = "TheBloke/Llama-2-70B-Chat-GPTQ"
pipe = pipeline("text-generation", model=model_name)

def generate_text(prompt):
    # Generate text using the pipeline
    results = pipe(prompt, max_length=150, top_p=0.95, temperature=0.9)
    return results[0]['generated_text'].strip()

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
        # Generate the response using the pipeline
        response = generate_text(prompt)
        st.markdown(response)  # Display final response
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
