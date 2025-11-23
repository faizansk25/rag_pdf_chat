from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from ingest import save_upload_file, process_pdf
from vector_store import add_documents_to_store, get_vector_store
from rag import get_retrieval_chain

# Load environment variables
load_dotenv()

app = FastAPI(title="RAG PDF Chat API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    chat_history: List[tuple] = []

@app.get("/")
async def root():
    return {"message": "RAG PDF Chat API is running"}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    processed_files = []
    for file in files:
        file_path = save_upload_file(file)
        chunks = process_pdf(file_path)
        add_documents_to_store(chunks)
        processed_files.append(file.filename)
        
    return {"message": f"Successfully processed {len(processed_files)} files: {', '.join(processed_files)}"}

@app.post("/chat")
async def chat(request: ChatRequest):
    vector_store = get_vector_store()
    chain = get_retrieval_chain(vector_store)
    
    # Convert chat history to list of tuples if needed, or handle in RAG
    # LangChain expects list of (human, ai) tuples
    formatted_history = []
    for msg in request.chat_history:
        # Assuming msg is dict or similar, adjust based on frontend
        pass 

    response = chain({"question": request.question, "chat_history": request.chat_history})
    
    answer = response["answer"]
    sources = [doc.metadata.get("source", "Unknown") for doc in response["source_documents"]]
    
    return {"answer": answer, "sources": list(set(sources))}
