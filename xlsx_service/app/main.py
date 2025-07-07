from fastapi import FastAPI, UploadFile, File
from app.services.xlsx_validator import validate_xlsx

app = FastAPI(title="XLSX Validator")

@app.post("/validate")
async def validate(file: UploadFile = File(...)):
    file_bytes = await file.read()
    return await validate_xlsx(file_bytes, file.filename)
