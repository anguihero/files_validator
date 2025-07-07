from fastapi import FastAPI, UploadFile, File
from app.services.docx_validator import validate_docx

app = FastAPI(title="DOCX Validator")

@app.post("/validate")
async def validate(file: UploadFile = File(...)):
    file_bytes = await file.read()
    return await validate_docx(file_bytes, file.filename)
