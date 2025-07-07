import magic

def detect_format(file_bytes: bytes) -> str:
    try:
        mime = magic.from_buffer(file_bytes, mime=True)

        # Mapeo robusto de MIME -> tipo lógico de archivo
        mime_map = {
            "application/pdf": "pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
            "message/rfc822": "eml",
            "application/zip": "zip",
            "text/plain": "txt"
        }

        # Coincidencia exacta
        if mime in mime_map:
            return mime_map[mime]

        # Coincidencias por prefijo (fallbacks)
        if mime.startswith("text/"):
            return "txt"
        elif mime.startswith("application/pdf"):
            return "pdf"
        elif "wordprocessingml" in mime:
            return "docx"
        elif "spreadsheetml" in mime:
            return "xlsx"
        elif "rfc822" in mime:
            return "eml"

        return "unknown"

    except Exception as e:
        # Opción de loguear el error si usas logging
        return "unknown"
