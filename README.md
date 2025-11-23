# RAG PDF Chat

A full-stack application to chat with multiple PDF documents using Retrieval-Augmented Generation (RAG). Optimized for low-end hardware by using API-based LLMs (Gemini/OpenAI) and lightweight local embeddings.

## Features
- **Multi-PDF Support**: Upload and chat with multiple documents simultaneously.
- **Low-End PC Optimized**: Uses `all-MiniLM-L6-v2` for fast, CPU-friendly embeddings.
- **API Integration**: Supports Groq (Recommended for speed), Google Gemini, and OpenAI.
- **Modern UI**: Responsive React frontend with a premium dark mode design.

## Prerequisites
- Python 3.8+
- Node.js 16+
- Groq API Key, Google API Key, or OpenAI API Key

## Setup

### Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example` and add your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add GOOGLE_API_KEY
   ```
4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## Usage
1. Open the frontend URL (usually `http://localhost:5173`).
2. Drag and drop PDF files into the sidebar.
3. Wait for the "Successfully processed" message.
4. Start asking questions about your documents!
