from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from datetime import datetime
from app.utils.detector import detect_format
import httpx
import logging

router = APIRouter()

# Configurar el logger
logger = logging.getLogger("gateway_logger")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

EXPECTED_FORMATS = ["pdf", "doc","docx", "xlsx", "txt", "eml"]

SERVICE_MAP = {
    "pdf": "http://pdf_validator:8000/validate",
    "docx": "http://docx_validator:8000/validate",
    "doc": "http://docx_validator:8000/validate",
    "xlsx": "http://xlsx_validator:8000/validate",
    "txt": "http://txt_validator:8000/validate",
    "eml": "http://eml_validator:8000/validate"
}

@router.post("/validate-file")
async def validate_file(file: UploadFile = File(...)):
    time_val_file_init = datetime.utcnow().isoformat()
    filename = file.filename

    contents = await file.read()
    size_bytes = len(contents)
    size_mb = round(size_bytes / (1024 * 1024), 2)

    # Intentar detectar el formato, si falla dejarlo como "desconocido"
    try:
        file_format = detect_format(contents)
    except Exception as e:
        file_format = "desconocido"
        logger.warning(f"No se pudo detectar el formato del archivo '{filename}': {str(e)}")

    result = {
        "id_file": filename,
        "time_val_file_init": time_val_file_init,
        "time_val_file_end": None,
        "format": file_format,
        "weight_file": size_mb,
        "items_in_file": None,
        "FLAG_OK_file": False,
        "error_type_01_file": False,
        "error_type_02_file": False,
        "error_type_03_file": False,
        "error_type_04_file": False,
        "error_type_09_file": False,
        "message": ""
    }

    if size_bytes > MAX_FILE_SIZE_BYTES:
        result["error_type_04_file"] = True
        result["message"] = f"Archivo demasiado grande. Máximo permitido: {MAX_FILE_SIZE_MB}MB"
        result["time_val_file_end"] = datetime.utcnow().isoformat()
        logger.info(f"Archivo '{filename}' excede el tamaño permitido: {size_mb}MB")
        return JSONResponse(status_code=413, content=result)

    if file_format not in EXPECTED_FORMATS:
        result["message"] = f"Formato de archivo '{file_format}' no soportado"
        result["time_val_file_end"] = datetime.utcnow().isoformat()
        logger.info(f"Archivo '{filename}' tiene un formato no soportado: {file_format}")
        return JSONResponse(status_code=400, content=result)

    try:
        logger.info(f"Enviando archivo '{filename}' al microservicio: {SERVICE_MAP[file_format]}")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                SERVICE_MAP[file_format],
                files={"file": (file.filename, contents, file.content_type)},
                timeout=600.0
            )
            response.raise_for_status()
            respuesta_microservicio = response.json()
    except httpx.HTTPStatusError as e:
        result["error_type_09_file"] = True
        result["message"] = f"Error HTTP al contactar microservicio especializado: {str(e)}"
        result["time_val_file_end"] = datetime.utcnow().isoformat()
        logger.error(f"[HTTPStatusError] Error contactando {SERVICE_MAP[file_format]}: {str(e)}")
        return JSONResponse(status_code=502, content=result)
    except httpx.TimeoutException:
        result["error_type_09_file"] = True
        result["message"] = "Timeout del microservicio especializado"
        result["time_val_file_end"] = datetime.utcnow().isoformat()
        logger.error(f"[TimeoutException] Tiempo excedido al contactar {SERVICE_MAP[file_format]}")
        return JSONResponse(status_code=504, content=result)
    except Exception as e:
        result["error_type_09_file"] = True
        result["message"] = f"Error inesperado: {str(e)}"
        result["time_val_file_end"] = datetime.utcnow().isoformat()
        logger.exception(f"[Exception] Error inesperado procesando archivo '{filename}'")
        return JSONResponse(status_code=500, content=result)

    result.update({
        "items_in_file": respuesta_microservicio.get("pages")
                         or respuesta_microservicio.get("paragraph_count")
                         or respuesta_microservicio.get("line_count"),
        "FLAG_OK_file": respuesta_microservicio.get("FLAG_OK_file", False),
        "error_type_01_file": respuesta_microservicio.get("error_type_01_file", False),
        "error_type_02_file": respuesta_microservicio.get("error_type_02_file", False),
        "error_type_03_file": respuesta_microservicio.get("error_type_03_file", False),
        "error_type_04_file": respuesta_microservicio.get("error_type_04_file", False),
        "error_type_09_file": respuesta_microservicio.get("error_type_09_file", False),
        "message": respuesta_microservicio.get("message", "")
    })
    result["time_val_file_end"] = datetime.utcnow().isoformat()

    logger.info(f"Archivo '{filename}' procesado exitosamente con formato {file_format}.")
    return JSONResponse(status_code=200, content=result)
