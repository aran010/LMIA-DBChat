from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from config import tenant_config
from rag.guardrails import SYSTEM_PROMPT
import os

llm_model = tenant_config.get("llm_model", "mistral:7b-instruct-q4_K_M")
embed_model = tenant_config.get("embed_model", "nomic-embed-text")

ollama_base_url = os.environ.get("OLLAMA_BASE_URL", "http://ollama:11434")

embeddings = OllamaEmbeddings(model=embed_model, base_url=ollama_base_url)

vectordb_dir = "/opt/ragapp/vectordb"
if not os.path.exists(vectordb_dir):
    vectordb_dir = os.path.join(os.path.dirname(__file__), "..", "..", "vectordb")

vectorstore = Chroma(
    collection_name="company_knowledge",
    embedding_function=embeddings,
    persist_directory=vectordb_dir
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": tenant_config.get("max_retrieved_chunks", 5)}
)

llm = ChatOllama(
    model=llm_model,
    base_url=ollama_base_url,
    temperature=tenant_config.get("response_temperature", 0.0)
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}")
])

def format_docs(docs):
    return "\n\n".join(f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}" for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def query_rag(question: str):
    return rag_chain.invoke(question)

async def astream_rag(question: str):
    async for chunk in rag_chain.astream(question):
        yield chunk
