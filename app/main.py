from fastapi import FastAPI, UploadFile, File
import aiofiles, uuid

app = FastAPI(title="ResumeHub API", version="0.1")

@app.get("/")
def home():
    return {"message": "Welcome to ResumeHub backend!"}

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    temp_path = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
    async with aiofiles.open(temp_path, "wb") as f:
        content = await file.read()
        await f.write(content)
    return {"status": "success", "filename": file.filename}
