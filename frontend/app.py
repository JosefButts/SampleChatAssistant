import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the app
st.set_page_config(
    page_title="DuploCloud Assistant",
    page_icon="🤖",
    layout="centered"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# API Configuration
API_URL = os.getenv("API_URL", "http://backend:8000")

def get_assistant_response(question: str):
    """Get response from the assistant API"""
    try:
        response = requests.post(
            f"{API_URL}/api/query",
            json={"text": question},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the assistant: {str(e)}")
        return None

# App header
st.title("🤖 DuploCloud Assistant")
st.markdown("""
Ask questions about DuploCloud documentation and get instant answers!
""")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("source"):
            st.caption(f"Source: {message['source']}")
        if message.get("confidence"):
            st.caption(f"Confidence: {message['confidence']}")

# Chat input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_assistant_response(prompt)
            if response:
                st.markdown(response["answer"])
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"],
                    
                })

# Add some styling
st.markdown("""
<style>
    .stChat {
        padding: 0.5rem;
    }
    .stChatMessage {
        background-color: transparent;
        border-radius: 4px;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .stChatInput {
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True) 