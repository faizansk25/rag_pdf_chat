from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os

# Initialize embeddings (lightweight, local)
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize LLM (API-based for low-end PC)
def get_llm():
    if os.getenv("GROQ_API_KEY"):
        return ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=0.3
        )
    elif os.getenv("GOOGLE_API_KEY"):
        return ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    elif os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
    else:
        raise ValueError("No API key found. Please set GROQ_API_KEY, GOOGLE_API_KEY or OPENAI_API_KEY.")

def get_retrieval_chain(vector_store):
    llm = get_llm()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )
    return chain
