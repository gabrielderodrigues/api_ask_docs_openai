from fastapi import FastAPI
from app.api.v1 import chat

app = FastAPI(
    title="AskDocs API with Azure OpenAI",
    version="1.0.0"
)

app.include_router(chat.router, prefix="/api/v1")