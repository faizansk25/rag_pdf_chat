from starlette.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app

# Configure client
client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "RAG PDF Chat API is running"}

@patch("backend.main.process_pdf")
@patch("backend.main.add_documents_to_store")
@patch("backend.main.save_upload_file")
def test_upload_files(mock_save, mock_add, mock_process):
    # Mock dependencies
    mock_save.return_value = "dummy_path.pdf"
    mock_process.return_value = ["chunk1", "chunk2"]
    mock_add.return_value = None

    # Create a dummy file
    files = [("files", ("test.pdf", b"dummy content", "application/pdf"))]
    
    response = client.post("/upload", files=files)
    
    assert response.status_code == 200
    assert "Successfully processed 1 files" in response.json()["message"]
    mock_save.assert_called_once()
    mock_process.assert_called_once()
    mock_add.assert_called_once()

@patch("backend.main.get_vector_store")
@patch("backend.main.get_retrieval_chain")
def test_chat_endpoint(mock_get_chain, mock_get_store):
    # Mock chain response
    mock_chain_instance = MagicMock()
    mock_chain_instance.return_value = {
        "answer": "Test answer",
        "source_documents": [
            MagicMock(metadata={"source": "doc1.pdf"}),
            MagicMock(metadata={"source": "doc2.pdf"})
        ]
    }
    mock_get_chain.return_value = mock_chain_instance
    
    # Mock vector store
    mock_get_store.return_value = MagicMock()

    payload = {
        "question": "What is this?",
        "chat_history": []
    }
    
    response = client.post("/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Test answer"
    assert "doc1.pdf" in data["sources"]
    assert "doc2.pdf" in data["sources"]
