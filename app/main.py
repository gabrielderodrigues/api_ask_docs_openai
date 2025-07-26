from fastapi import FastAPI
from app.api.v1 import chat

app = FastAPI(
    title="API Chat Azure OpenAI",
    version="1.0.0"
)

# Prefixo para versão da API
app.include_router(chat.router, prefix="/api/v1")