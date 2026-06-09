from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from config import tenant_config

embeddings = OllamaEmbeddings(
    model=tenant_config.get("embed_model", "nomic-embed-text"),
    base_url="http://ollama:11434"
)

vector_store = Chroma(
    collection_name="company_knowledge",
    embedding_function=embeddings,
    persist_directory="/opt/ragapp/vectordb"
)

def embed_and_store(chunks):
    if chunks:
        vector_store.add_documents(chunks)
        print(f"Stored {len(chunks)} chunks in ChromaDB.")
