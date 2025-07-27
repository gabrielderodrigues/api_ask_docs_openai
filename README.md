# API Ask Docs OpenAI

This project is an API built with FastAPI and LangChain, designed to process PDF documents, generate embeddings using Azure OpenAI, and answer user questions based on the content of uploaded files. It is ideal for document Q&A, knowledge extraction, and contextual chat applications.

## Features

- **PDF Upload:** Users can upload PDF files via a REST endpoint. Files are stored in the `files/` directory.
- **Embeddings Generation:** Uploaded PDFs are split into chunks and embeddings are generated using Azure OpenAI's embedding models.
- **Vector Database:** Embeddings are stored locally using FAISS for fast similarity search.
- **Contextual Q&A:** Users can ask questions about a specific file. The API retrieves relevant chunks and uses Azure OpenAI to generate answers based only on the file's content.
- **Logging:** All major operations are logged with clear icons for easy debugging.
- **Environment Configuration:** Credentials and endpoints are managed via `.env` and `.env.example` files.

## How It Works

1. **Upload a PDF:**
   - Endpoint: `POST /upload`
   - Upload your PDF file using form-data (`file` field).
2. **Process & Store:**
   - The file is saved, split into chunks, and embeddings are generated and stored in a local FAISS vector database.
3. **Ask Questions:**
   - Endpoint: `POST /file-ask`
   - Send a JSON body with `file_name` and `query`.
   - The API retrieves the most relevant chunks and uses Azure OpenAI to answer your question based on the file content.

## Example Usage

### Upload a PDF
```
POST /upload
form-data:
  file: yourfile.pdf
```

### Ask a Question
```
POST /file-ask
Body (JSON):
{
  "file_name": "yourfile.pdf",
  "query": "What is the main topic of this document?"
}
```

## Environment Variables
See `.env.example` for all required variables:
- `AZURE_OPENAI_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_OPENAI_DEPLOYMENT_EMBEDDING`

## Project Structure
```
app/
  main.py
  api/
    v1/
      api.py
  core/
    config.py
  models/
    chat.py
  services/
    openai_service.py
    process_file.py
```

## Requirements
- Python 3.12+
- FastAPI
- LangChain
- Azure OpenAI
- FAISS (`faiss-cpu` or `faiss-gpu`)
- pypdf

## Setup
1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your Azure OpenAI credentials.
5. Run the API:
   ```
   uvicorn app.main:app --reload
   ```

## License
MIT

## Author
Gabriel Oliveira
