# src/agent/data/vector_store.py

from langchain_community.vectorstores import Annoy
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import logging

def create_vectorstore_and_retriever(data):
    if not data:
        logging.error("No data provided to create vector store.")
        raise ValueError("No data provided to create vector store.")
    logging.info(f"Creating vector store with {len(data)} documents.")

    # Convert text to Document objects
    documents = [Document(page_content=text) for text in data]

    # Use a multilingual embeddings model suitable for Spanish
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # Pass the embeddings instance directly
    vectorstore = Annoy.from_documents(
        documents=documents,
        embedding=embeddings,
        n_trees=20
    )

    retriever = vectorstore.as_retriever(k=10)
    return retriever





# # src/data_processing/vector_store.py
# from langchain.vectorstores import FAISS
# from langchain.embeddings import OpenAIEmbeddings
# import os

# def create_vector_store(processed_data_dir):
#     texts = []
#     for filename in os.listdir(processed_data_dir):
#         with open(os.path.join(processed_data_dir, filename), 'r') as file:
#             texts.append(file.read())

#     embeddings = OpenAIEmbeddings()
#     vectorstore = FAISS.from_texts(texts, embeddings)
#     vectorstore.save_local('data/vectorstores/faiss_index')
#     return vectorstore

# # Usage
# vectorstore = create_vector_store('data/processed/')

# # src/agents/retriever_agent.py
# from langchain.vectorstores import FAISS

# def get_retriever(vectorstore_path):
#     vectorstore = FAISS.load_local(vectorstore_path)
#     retriever = vectorstore.as_retriever(search_type="similarity", k=5)
#     return retriever

# # Usage
# retriever = get_retriever('data/vectorstores/faiss_index')

