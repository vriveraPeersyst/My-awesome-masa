# src/agent/rag_agent.py

import os
import logging
from src.agent.data.data_loader import load_documents
from src.agent.rag.rag_chain_setup import setup_rag_chain
from src.agent.graph.graph_workflow import setup_workflow
from src.agent.search_tools.search_tools import get_web_search_tool
from src.agent.data.vector_store import create_vectorstore_and_retriever
from src.agent.utils import extract_team_names

# Global variables
rag_chain = None
web_search_tool = None

def initialize_agent():
    global rag_chain, web_search_tool
    rag_chain = setup_rag_chain()
    graph = setup_workflow()
    web_search_tool = get_web_search_tool()
    return graph

def get_rag_response(graph, question: str, history: str):
    logging.info(f"Generating response for question: {question}")

    # Extract team names from the question
    team_folders = extract_team_names(question, history)
    if not team_folders:
        logging.info("No team names found in question. Loading all data.")
        # Optionally, load all teams or handle differently
        team_folders = os.listdir('data/LaLigaEquipos')  # Load all teams
    else:
        logging.info(f"Found team folders: {team_folders}")

    # Load documents from relevant team folders
    data = load_documents(team_folders)
    if not data:
        logging.warning("No data loaded. Proceeding without data.")
        data = []

    # Create vectorstore and retriever
    retriever = create_vectorstore_and_retriever(data)
    if retriever is None:
        logging.error("Failed to create retriever.")
    else:
        logging.info("Retriever created successfully.")

    # Pass the retriever to the graph's state
    response = graph.invoke({
        "question": question,
        "history": history,
        "steps": [],
        "retriever": retriever
    })
    return response["generation"], response["steps"]

