import os
import logging
from openai import AzureOpenAI
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get Azure OpenAI credentials and deployment info from environment or settings
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", settings.AZURE_OPENAI_ENDPOINT)
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", settings.AZURE_OPENAI_DEPLOYMENT)
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", settings.AZURE_OPENAI_KEY)

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version=getattr(settings, "AZURE_API_VERSION", "2025-01-01-preview"),
)

def get_chat_response(prompt: str, context: str = "") -> str:
    try:
        logger.info("🧩 Building chat prompt with context and user question.")
        # Builds the context from the embeddings plus the user's question
        chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a helpful assistant. Use the context below to answer exclusively about the file:\n" + context
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

        logger.info("🚀 Sending request to Azure OpenAI for chat completion.")
        # Call Azure OpenAI to generate a chat completion based on the prompt and context
        completion = client.chat.completions.create(
            model=deployment,           # Model deployment name
            messages=chat_prompt,       # Chat prompt with context and user question
            max_tokens=150,             # Maximum number of tokens in the response
            temperature=0.7,            # Controls randomness/creativity
            top_p=0.95,                 # Controls diversity of the response
            frequency_penalty=0,        # Penalizes repeated phrases
            presence_penalty=0,         # Encourages new topics in the response avoiding repetition
            stop=None,                  # Optional stop sequences
            stream=False                # If True, returns response as a stream
        )
        
        logger.info("✅ Received response from Azure OpenAI.")
        # Return the generated answer
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"❌ Error getting chat response: {str(e)}")
        raise Exception(f"Error getting chat response: {str(e)}")