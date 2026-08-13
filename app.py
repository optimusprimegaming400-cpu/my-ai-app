import os
import streamlit as st
from groq import Groq

# Set page title and layout
st.set_page_config(page_title="Mohammed's AI Assistant", page_icon="🤖")
st.title("Mohammed's AI Assistant 🤖")

# Safely retrieve Groq API Key from Streamlit Secrets or Environment Variables
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY"))

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream AI response
    with st.chat_message("assistant"):
        # Custom system prompt instructing the AI about its creator
        system_instruction = {
            "role": "system",
            "content": "You are a helpful, friendly AI assistant created and built by Mohammed Nahian using Streamlit and Groq."
        }
        
        # Combine system prompt with message history
        formatted_messages = [system_instruction] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]

        # Call Groq API with Llama 3.3 model
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=formatted_messages,
            stream=True,
        )

        # Generator function to stream tokens smoothly
        def parse_groq_stream(stream):
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        response = st.write_stream(parse_groq_stream(stream))
    
    # Save assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})