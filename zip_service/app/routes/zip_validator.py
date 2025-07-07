from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.utils.detector import detect_format
import httpx

router = APIRouter()

SERVICE_MAP = {
    "pdf": "http://pdf_validator:8000/validate",
    "docx": "http://docx_validator:8000/validate"
    # Agrega más servicios aquí
}

@router.post("/validate-file")
async def validate_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_format = detect_format(file_bytes)

    if file_format not in SERVICE_MAP:
        return JSONResponse(
            status_code=400,
            content={"error": "Formato no soportado", "format": file_format}
        )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            SERVICE_MAP[file_format],
            files={"file": (file.filename, file_bytes, file.content_type)}
        )
        return JSONResponse(status_code=response.status_code, content=response.json())
