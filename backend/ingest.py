from langchain_community.document_loaders import PyPDFLoader
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import shutil

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def save_upload_file(upload_file):
    file_path = os.path.join(UPLOAD_DIR, upload_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

import fitz  # PyMuPDF
from rapidocr_onnxruntime import RapidOCR
from langchain.docstore.document import Document

# Initialize OCR
ocr = RapidOCR()

def process_pdf(file_path):
    doc = fitz.open(file_path)
    documents = []
    
    for page_num, page in enumerate(doc):
        text = page.get_text()
        
        # If text is sparse, try OCR
        if len(text.strip()) < 50:
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("png")
            result, _ = ocr(img_bytes)
            if result:
                ocr_text = "\n".join([line[1] for line in result])
                text += "\n" + ocr_text
        
        documents.append(Document(
            page_content=text,
            metadata={"source": os.path.basename(file_path), "page": page_num}
        ))
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    # Filter out empty chunks
    chunks = [chunk for chunk in chunks if chunk.page_content.strip()]
    return chunks
