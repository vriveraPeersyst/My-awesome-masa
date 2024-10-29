from typing import List, TypedDict
import logging

class GraphState(TypedDict):
    question: str
    history: str
    generation: str
    search: str
    data: List[str]
    steps: List[str]

def retrieve(state):
    retriever = state.get("retriever")
    if not retriever:
        logging.error("No retriever provided in state.")
        return state  # Handle the error as appropriate

    logging.info(f"Retrieving data for question: {state['question']}")

    question = state["question"]
    retrieved_docs = retriever.get_relevant_documents(question)
    data = [doc.page_content for doc in retrieved_docs]
    steps = state["steps"]
    steps.append("retrieve_data")
    return {
        "data": data,
        "question": question,
        "history": state.get("history", ""),
        "steps": steps,
        "retriever": retriever
    }
def generate(state):
    from src.agent.rag_agent import rag_chain
    logging.info(f"Generating answer for question: {state['question']}")
    question = state["question"]
    data = state.get("data", [])
    history = state.get("history", "")

    # Ensure data is a list of strings
    data_texts = []
    for item in data:
        if isinstance(item, dict):
            # Extract text from the dictionary
            # Adjust the key based on your web search result structure
            text = item.get('snippet') or item.get('text') or item.get('content', '')
            if text:
                data_texts.append(text)
        elif isinstance(item, str):
            data_texts.append(item)
        else:
            logging.warning(f"Unexpected data type in data: {type(item)}")

    data_text = "\n".join(data_texts)

    # Prepare inputs for the chain
    chain_inputs = {
        "history": history,
        "question": question,
        "data": data_text
    }

    generation = rag_chain.invoke(chain_inputs)
    steps = state["steps"]
    steps.append("generate_answer")
    return {
        "data": data,
        "question": question,
        "history": history,
        "generation": generation,
        "steps": steps,
        "retriever": state.get("retriever")  # Include retriever if needed
    }

def web_search(state):
    from src.agent.rag_agent import web_search_tool
    logging.info(f"Performing web search for question: {state['question']}")
    question = state["question"]
    data = state.get("data", [])
    steps = state["steps"]
    steps.append("web_search")
    web_results = web_search_tool.invoke({"query": question})
    data.extend(web_results)
    return {"data": data, "question": question, "history": state.get("history", ""), "steps": steps}

def decide_to_generate(state):
    logging.info("Deciding whether to generate or search...")
    data = state.get("data", [])
    if not data:
        logging.info("No data found, deciding to search.")
        return "search"
    else:
        logging.info("Data found, deciding to generate.")
        return "generate"

