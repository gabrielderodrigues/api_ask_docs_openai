from fastapi import FastAPI
from app.api.v1 import api

app = FastAPI(
    title="AskDocs API with Azure OpenAI",
    version="1.0.0"
)

app.include_router(api.router, prefix="/api/v1")