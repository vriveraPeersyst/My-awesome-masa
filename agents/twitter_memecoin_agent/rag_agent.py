import sys
import logging 
from src.agent.core.config import * 
from src.agent.data.data_management import load_and_prepare_data
from src.agent.rag.rag_chain_setup import setup_rag_chain
from src.agent.graph.graph_workflow import setup_workflow
from src.agent.search_tools.search_tools import get_web_search_tool 

# Setup
retriever = load_and_prepare_data(DATA_URLS)
rag_chain = setup_rag_chain()
graph = setup_workflow()
web_search_tool = get_web_search_tool()

def get_rag_response(question: str):
    logging.info(f"Generating response for question: {question}")
    response = graph.invoke({"question": question, "steps": []})
    return response["generation"], response["steps"]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        logging.info(f"Received question: {question}")
        answer, steps = get_rag_response(question)
        print(f"Answer: {answer}")
        print("\nSteps:")
        for step in steps:
            print(f"- {step}")
    else:
        print("Please provide a question as a command-line argument.")