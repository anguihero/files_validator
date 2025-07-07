from PyPDF2 import PdfReader 
from fastapi.responses import JSONResponse
from datetime import datetime
import io

async def validate_pdf(file_bytes: bytes, filename: str):
    time_val_file_init = datetime.utcnow().isoformat()
    size_bytes = len(file_bytes)
    size_mb = round(size_bytes / (1024 * 1024), 2)

    result = {
        "id_file": filename,
        "time_val_file_init": time_val_file_init,
        "time_val_file_end": None,
        "format": "pdf",
        "weight_file": size_mb,
        "pages": None,
        "FLAG_OK_file": False,
        "error_type_01_file": False,  # archivo corrupto
        "error_type_02_file": False,  # archivo vacío
        "error_type_03_file": False,  # peso mínimo no alcanzado
        "error_type_04_file": False,  # peso máximo excedido
        "error_type_09_file": False,  # error inesperado
        "message": ""
    }

    try:
        if size_bytes == 0:
            result["error_type_02_file"] = True
            result["message"] = "El archivo está vacío."
        elif size_mb < 0.009:
            result["error_type_03_file"] = True
            result["message"] = "El archivo es demasiado liviano para ser válido."
        elif size_mb > 10:
            result["error_type_04_file"] = True
            result["message"] = "El archivo excede el tamaño máximo permitido (10MB)."
        else:
            try:
                reader = PdfReader(io.BytesIO(file_bytes))
                result["pages"] = len(reader.pages)
                result["FLAG_OK_file"] = True
                result["message"] = "Validación exitosa."
            except Exception as e:
                result["error_type_01_file"] = True
                result["message"] = f"El archivo parece estar corrupto: {str(e)}"
    except Exception as e:
        result["error_type_09_file"] = True
        result["message"] = f"Error inesperado durante validación: {str(e)}"

    result["time_val_file_end"] = datetime.utcnow().isoformat()
    return JSONResponse(status_code=200 if result["FLAG_OK_file"] else 400, content=result)
