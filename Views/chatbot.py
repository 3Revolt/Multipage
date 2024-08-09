import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load the model and tokenizer directly
model_name = "TheBloke/Llama-2-70B-Chat-GPTQ"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Ensure the model is in evaluation mode
model.eval()

def generate_text(prompt):
    # Encode the prompt and generate text
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=150,
            top_p=0.95,
            temperature=0.9
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

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
        # Generate the response using the model
        response = generate_text(prompt)
        st.markdown(response)  # Display final response
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
