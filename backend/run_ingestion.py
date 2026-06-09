import os
import sys

# Add backend directory to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import tenant_config
from ingestion.db_connector import process_database
from ingestion.doc_processor import process_pdf
from ingestion.embedder import embed_and_store

def main():
    print("Starting full data ingestion...")
    all_chunks = []
    
    # 1. Process databases
    print("Processing databases...")
    for db_config in tenant_config.get("db_connections", []):
        chunks = process_database(db_config)
        all_chunks.extend(chunks)
        print(f"Extracted {len(chunks)} rows from {db_config.get('name')}")
        
    # 2. Process documents
    print("Processing documents...")
    for doc_source in tenant_config.get("doc_sources", []):
        path = doc_source.get("path")
        if os.path.exists(path):
            for file_name in os.listdir(path):
                file_path = os.path.join(path, file_name)
                if file_name.lower().endswith('.pdf'):
                    chunks = process_pdf(file_path)
                    all_chunks.extend(chunks)
                    print(f"Extracted {len(chunks)} chunks from {file_name}")
                    
    # 3. Embed and store
    print(f"Total chunks to embed: {len(all_chunks)}")
    embed_and_store(all_chunks)
    print("Ingestion complete!")

if __name__ == "__main__":
    main()
