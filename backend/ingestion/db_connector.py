from config import tenant_config

DIALECT_MAP = {
    "postgresql": "postgresql+psycopg2",
    "oracle": "oracle+cx_oracle",
    "mssql": "mssql+pyodbc",
    "mysql": "mysql+pymysql",
}

def get_engine(connection_config):
    # Mocked for skeleton
    return None

def extract_tables():
    pass
