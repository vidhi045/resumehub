from pydantic import BaseModel

class ResumeOut(BaseModel):
    id: str | None = None
    filename: str
    message: str = "File uploaded successfully"
