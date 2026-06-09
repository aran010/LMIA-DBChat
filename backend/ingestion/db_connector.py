from sqlalchemy import create_engine, MetaData, select
from langchain_core.documents import Document
from config import tenant_config

DIALECT_MAP = {
    "postgresql": "postgresql+psycopg2",
    "oracle": "oracle+cx_oracle",
    "mssql": "mssql+pyodbc",
    "mysql": "mysql+pymysql",
    "sqlite": "sqlite"
}

def get_engine(connection_config):
    db_type = connection_config.get("type", "sqlite")
    dialect = DIALECT_MAP.get(db_type, "sqlite")
    
    if db_type == "sqlite":
        # For our test sample
        db_path = connection_config.get("database", "/opt/ragapp/config/sample_hr.db")
        return create_engine(f"sqlite:///{db_path}")
        
    # Standard connection logic for others
    user = connection_config.get("username", "")
    password = "" # Would fetch from os.getenv(connection_config.get("password_env"))
    host = connection_config.get("host", "")
    port = connection_config.get("port", "")
    db = connection_config.get("database", connection_config.get("service_name", ""))
    
    url = f"{dialect}://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)

def process_database(connection_config):
    engine = get_engine(connection_config)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    chunks = []
    tables_to_index = connection_config.get("tables_to_index", [])
    
    with engine.connect() as conn:
        for table_name in tables_to_index:
            if table_name in metadata.tables:
                table = metadata.tables[table_name]
                result = conn.execute(select(table)).fetchall()
                
                columns = table.columns.keys()
                for row in result:
                    # Convert row to "column: value" format
                    row_text = "\n".join([f"{col}: {val}" for col, val in zip(columns, row)])
                    
                    doc_metadata = {
                        "source": f"DB:{connection_config.get('name')} Table:{table_name}",
                        "type": "database_row"
                    }
                    chunks.append(Document(page_content=row_text, metadata=doc_metadata))
    
    return chunks
