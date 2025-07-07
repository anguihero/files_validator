from fastapi import FastAPI, UploadFile, File
from app.routes.eml_validator import validate_eml

app = FastAPI(title="EML Validator")

@app.post("/validate")
async def validate(file: UploadFile = File(...)):
    file_bytes = await file.read()
    return await validate_eml(file_bytes, file.filename)
