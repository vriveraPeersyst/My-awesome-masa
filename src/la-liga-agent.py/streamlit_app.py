
import sys
import os
import logging
import time
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from dotenv import load_dotenv

st.set_page_config(page_title="💬 La Kiniela Chat", page_icon="💬")

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
sys.path.append(project_root)

from src.agent import rag_agent

# Initialize the agent only once per session
@st.cache_resource
def initialize_agent_cached():
    return rag_agent.initialize_agent()

# Use the cached agent initialization
graph = initialize_agent_cached()

def get_streaming_rag_response(question: str):
    logging.info(f"Generating response for question: {question}")

    # Construct conversation history
    history = ""
    for msg in st.session_state['message_history']:
        role = "Usuario" if msg["role"] == "user" else "Asistente"
        content = msg["content"]
        history += f"{role}: {content}\n"

    response, steps = rag_agent.get_rag_response(graph, question, history)
    
    words = response.split()
    for word in words:
        yield word + " "
        time.sleep(0.05)

st.title("💬 La Kiniela Chat")

st.markdown("""
Welcome to la Kiniela Chat!
        
Soy un asistente especializado en LaLiga. Puedo ayudarte a resolver tus dudas sobre equipos, partidos, jornadas y cualquier dato relevante. Además, puedo analizar tweets para proporcionar contexto adicional sobre situaciones recientes. Los datos sobre los equipos, partidos y jornadas los tengo cargados en mi base de datos, por lo que puedo responder de manera clara y concisa a tus consultas. ¿Sobre qué equipo, partido o tema te gustaría obtener más información?
""")

st.markdown("---")

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

def display_chat_history():
    for msg in st.session_state['message_history']:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

display_chat_history()

if prompt := st.chat_input("Escribe tu pregunta:"):
    st.session_state.message_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Display thinking animation
        thinking_placeholder = st.empty()
        with thinking_placeholder:
            for i in range(3):
                for dot in [".", "..", "..."]:
                    thinking_placeholder.markdown(f"Pensando{dot}")
                    time.sleep(0.3)
        
        # Start streaming the response
        for chunk in get_streaming_rag_response(prompt):
            thinking_placeholder.empty()  # Remove thinking animation
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.message_history.append({"role": "assistant", "content": full_response})

add_vertical_space(5)

