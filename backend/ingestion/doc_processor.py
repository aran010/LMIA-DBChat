import os
import fitz
from langchain_core.documents import Document
from config import tenant_config

def process_pdf(file_path):
    print(f"Processing PDF: {file_path}")
    doc = fitz.open(file_path)
    chunks = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        
        # Skip empty pages
        if len(text.strip()) > 50:
            metadata = {
                "source": os.path.basename(file_path),
                "page": page_num + 1,
                "type": "document"
            }
            chunks.append(Document(page_content=text, metadata=metadata))
            
    doc.close()
    return chunks

def process_docx(file_path):
    # Stub for future implementation
    return []
