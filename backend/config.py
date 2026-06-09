import json
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret: str = os.getenv("JWT_SECRET", "default_secret")
    db_erp_password: str = os.getenv("DB_ERP_PASSWORD", "")
    config_path: str = "/opt/ragapp/config/tenant.json"

    def get_tenant_config(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            # Fallback for local testing outside docker
            local_path = os.path.join(os.path.dirname(__file__), "..", "config", "tenant.json")
            if os.path.exists(local_path):
                with open(local_path, 'r') as f:
                    return json.load(f)
            return {}

settings = Settings()
tenant_config = settings.get_tenant_config()
