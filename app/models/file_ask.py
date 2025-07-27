from pydantic import BaseModel


class FileAskRequest(BaseModel):
    file_name: str
    query: str