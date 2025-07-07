from fastapi import FastAPI
from app.routes import validate

app = FastAPI(
    title="IA Validador Multimodal Inteligente de archivos",
    version="0.1.0-beta",
    description="""
**IA Validador Multimodal Inteligente de archivos**

Una solución desarrollada por el equipo de Ciencia de Datos e Inteligencia Artificial de la Oficina de Tecnologías de la Información (OTI), 
que permite validar automáticamente la calidad de los documentos cargados por los ciudadanos en los formularios web de la Superintendencia de Industria y Comercio (SIC).

Actualmente en **versión beta**, este validador permite realizar análisis multimodal según el tipo de archivo (.pdf, .docx, .xlsx, .txt, entre otros) y determinar si cumple condiciones mínimas de integridad y contenido.
""",
    contact={
        "name": "Equipo de Ciencia de Datos IA - OTI",
        "email AMMS": "c.ammunozs@sic.gov.co",
        "email JEVP": "c.jevanegas@sic.gov.co",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(validate.router)
