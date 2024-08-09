import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load tokenizer and model
model_name = "TheBloke/Llama-2-70B-Chat-GPTQ"  # Use your specific model name here
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_text(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")  # Tokenize the prompt
    outputs = model.generate(inputs['input_ids'], max_length=150, top_p=0.95, temperature=0.9)  # Generate text
    return tokenizer.decode(outputs[0], skip_special_tokens=True)  # Decode the output

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
        # Prepare the prompt for the model
        # Use only the latest user message for a more direct response
        response = generate_text(prompt)
        st.markdown(response)  # Display final response
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
