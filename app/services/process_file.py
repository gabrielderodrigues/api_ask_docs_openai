import os
import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VECTOR_DB_DIR = "vector_db"

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", settings.AZURE_OPENAI_ENDPOINT),
    api_key=os.getenv("AZURE_OPENAI_API_KEY", settings.AZURE_OPENAI_KEY),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_EMBEDDING", settings.AZURE_OPENAI_DEPLOYMENT_EMBEDDING),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", settings.AZURE_OPENAI_API_VERSION)
)

def save_and_process_file(file_name: str, file_bytes: bytes):
    """
    Save the uploaded file and process its content.
    """
    try:
        logger.info(f"📥 Starting to process file: {file_name}")
        files_dir = os.path.join(os.getcwd(), "files")
        
        # Ensure the directory exists
        if not os.path.exists(files_dir):
            os.makedirs(files_dir)
            logger.info(f"📁 Created directory: {files_dir}")

        file_path = os.path.join(files_dir, file_name)
        
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        logger.info(f"💾 Saved file to: {file_path}")
        
        # Process the file content
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        logger.info(f"📄 Loaded {len(documents)} documents from PDF.")

        # Split the documents into smaller chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = splitter.split_documents(documents)
        logger.info(f"✂️ Split documents into {len(docs)} chunks.")

        # Create embeddings for the documents
        db = FAISS.from_documents(docs, embeddings)
        logger.info("🧠 Created embeddings for the document chunks.")

        # Save the vector database to a local file
        vector_path = os.path.join(VECTOR_DB_DIR, file_name)
        db.save_local(vector_path)
        logger.info(f"📦 Saved vector database to: {vector_path}")

        return {"filename": file_name, "message": "File uploaded and processed (replaced if existed)."}
    except Exception as e:
        logger.error(f"❌ Error processing file {file_name}: {str(e)}")
        raise Exception(f"Error processing file: {str(e)}")

def query_file(file_name: str, query: str, k: int = 3):
    """
    Queries the file's vector database to find the most relevant chunks for the user's question.
    """
    try:
        logger.info(f"🔎 Querying file: {file_name} with query: '{query}'")
        
        # Load the locally saved vector database
        vector_path = os.path.join(VECTOR_DB_DIR, file_name)
        
        if not os.path.exists(vector_path):
            logger.warning(f"🚫 File not found in vector database: {vector_path}")
            return [f"File '{file_name}' not found in the vector database."]
        
        db = FAISS.load_local(
            vector_path,
            embeddings,
            allow_dangerous_deserialization=True
        )
        logger.info(f"📦 Loaded vector database from: {vector_path}")

        # Search for the k most similar chunks to the query
        docs = db.similarity_search(query, k=k)
        logger.info(f"✅ Found {len(docs)} relevant chunks for the query.")

        # Return only the content of the chunks
        return [doc.page_content for doc in docs]
    except Exception as e:
        logger.error(f"❌ Error querying file {file_name}: {str(e)}")
        raise Exception(f"Error querying file: {str(e)}")