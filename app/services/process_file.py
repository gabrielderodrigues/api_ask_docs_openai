import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.core.config import settings

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

    Args:
        file_name (str): The name of the file to save.
        file_bytes (bytes): The content of the file in bytes.

    Returns:
        dict: A dictionary containing the filename and its content.
    """
    try:
        files_dir = os.path.join(os.getcwd(), "files")
        
        # Ensure the directory exists
        if not os.path.exists(files_dir):
            os.makedirs(files_dir)

        file_path = os.path.join(files_dir, file_name)
        
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        
        # Process the file content
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        # Split the documents into smaller chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = splitter.split_documents(documents)
        
        # Create embeddings for the documents
        db = FAISS.from_documents(docs, embeddings)
        
        # Save the vector database to a local file
        vector_path = os.path.join(VECTOR_DB_DIR, file_name)
        db.save_local(vector_path)
        
        return {"filename": file_name, "message": "File uploaded and processed (replaced if existed)."}
    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")

    
def query_file(file_name: str, query: str, k: int = 3):
    """
    Queries the file's vector database to find the most relevant chunks for the user's question.

    Args:
        file_name (str): Name of the already processed file.
        query (str): User's question.
        k (int): Number of relevant chunks to return.

    Returns:
        list: List of contents of the chunks most similar to the query.
    """
    try:
        # Load the locally saved vector database
        vector_path = os.path.join(VECTOR_DB_DIR, file_name)
        db = FAISS.load_local(
            vector_path,
            embeddings,
            allow_dangerous_deserialization=True
        )
        
        # Search for the k most similar chunks to the query
        docs = db.similarity_search(query, k=k)
        
        # Return only the content of the chunks
        return [doc.page_content for doc in docs]
    except Exception as e:
        raise Exception(f"Error querying file: {str(e)}")