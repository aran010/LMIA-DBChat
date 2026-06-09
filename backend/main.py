from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import chat, admin, auth
from scheduler import start_scheduler
from config import tenant_config

app = FastAPI(title="Offline AI Knowledge Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.on_event("startup")
async def startup_event():
    start_scheduler()

@app.get("/health")
def health_check():
    return {"status": "ok", "tenant": tenant_config.get("company_name", "Unknown")}
