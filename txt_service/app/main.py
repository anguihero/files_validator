from fastapi import FastAPI, UploadFile, File
from app.services.txt_validator import validate_txt

app = FastAPI(title="TXT Validator")

@app.post("/validate")
async def validate(file: UploadFile = File(...)):
    file_bytes = await file.read()
    return await validate_txt(file_bytes, file.filename)
