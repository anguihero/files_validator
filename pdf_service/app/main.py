from fastapi import FastAPI, UploadFile, File
from app.services.pdf_validator import validate_pdf

app = FastAPI(title="PDF Validator")

@app.post("/validate")
async def validate(file: UploadFile = File(...)):
    file_bytes = await file.read()
    return await validate_pdf(file_bytes, file.filename)
