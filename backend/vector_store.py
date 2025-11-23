from langchain_community.vectorstores import Chroma
import chromadb
from rag import get_embeddings
import os
import shutil

PERSIST_DIRECTORY = "db"

def get_vector_store():
    embeddings = get_embeddings()
    client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
    return Chroma(
        client=client,
        embedding_function=embeddings,
    )

def add_documents_to_store(documents):
    vector_store = get_vector_store()
    vector_store.add_documents(documents)
    return vector_store

def clear_vector_store():
    if os.path.exists(PERSIST_DIRECTORY):
        shutil.rmtree(PERSIST_DIRECTORY)
