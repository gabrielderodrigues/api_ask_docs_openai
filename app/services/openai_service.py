import os
from openai import AzureOpenAI
from app.core.config import settings

endpoint = os.getenv("ENDPOINT_URL", settings.AZURE_OPENAI_ENDPOINT)
deployment = os.getenv("DEPLOYMENT_NAME", settings.AZURE_DEPLOYMENT_NAME)
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", settings.AZURE_OPENAI_KEY)

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version=getattr(settings, "AZURE_API_VERSION", "2025-01-01-preview"),
)

def get_chat_response(prompt: str) -> str:
    # O bloco "system" define o comportamento do assistente (contexto).
    # O bloco "user" traz a pergunta ou comando do usuário.
    # Não é obrigatório ter o "system", mas é recomendado para melhores resultados.
    # O "user" é essencial, pois representa a entrada do usuário.
    chat_prompt = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "Você é um assistente útil."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]

    completion = client.chat.completions.create(
        model=deployment,
        messages=chat_prompt,
        max_tokens=6553,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    return completion.choices[0].message.content