# 🧠 IA Validador Multimodal Inteligente de Archivos (versión beta)

**Desarrollado por el equipo de Ciencia de Datos e Inteligencia Artificial - Oficina de Tecnologías de la Información (OTI)  
Superintendencia de Industria y Comercio - SIC**



## 👨‍💻 Equipo de desarrollo


**Desarrollado por el equipo de Ciencia de Datos e Inteligencia Artificial - Oficina de Tecnologías de la Información (OTI)  
Superintendencia de Industria y Comercio - SIC**

* Equipo de Ciencia de Datos e Inteligencia Artificial
   * "AMMS": "c.ammunozs@sic.gov.co",
   * "JEVP": "c.jevanegas@sic.gov.co",




---

## 🧩 Descripción General

**IA Validador Multimodal Inteligente de Archivos** es una solución modular que permite validar de forma automática la calidad de los documentos cargados por los ciudadanos en los formularios web de la Superintendencia de Industria y Comercio (SIC).

La herramienta detecta el tipo de archivo (PDF, DOCX, XLSX, TXT, etc.) y aplica una serie de validaciones especializadas en función del formato, como detección de corrupción, peso mínimo/máximo, estructura interna y legibilidad.

---

## 🎯 Requerimientos que atiende

- ✅ Verificar si el archivo está vacío o corrupto.
- ✅ Validar que cumpla con un tamaño razonable (ni muy pequeño ni excesivo).
- ✅ Detectar el tipo real de archivo a partir del contenido, no solo de la extensión.
- ✅ Realizar análisis específicos según el tipo:
  - PDF: lectura y número de páginas.
  - DOCX: párrafos legibles.
  - XLSX: hojas del libro de trabajo.
  - TXT: líneas y caracteres.
- ✅ Generar una respuesta estructurada para la validación automática del formulario.

---

## ⚙️ Enfoque y arquitectura

La solución está construida con un enfoque **modular de microservicios**, desacoplados y fácilmente escalables, usando `FastAPI` + `Docker Compose`.

### 🧱 Microservicios principales

| Servicio           | Descripción                                       | Puerto interno |
|--------------------|---------------------------------------------------|----------------|
| `gateway_service`  | Recibe el archivo, detecta el tipo y enruta      | `8000`         |
| `pdf_validator`    | Valida archivos `.pdf` con `PyPDF2`              | `8000`         |
| `docx_validator`   | Valida archivos `.docx` con `python-docx`        | `8000`         |
| `xlsx_validator`   | Valida archivos `.xlsx` con `openpyxl`           | `8000`         |
| `txt_validator`    | Valida archivos `.txt` leyendo directamente       | `8000`         |

Todos están conectados por red interna `sic_net` y orquestados con `docker-compose`.

---

## 📁 Estructura del Proyecto

```text
IA-Validador/
├── docker-compose.yml
├── gateway_service/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   └── validate.py
│   │   └── utils/
│   │       └── detector.py
│   ├── Dockerfile
│   └── requirements.txt
├── pdf_service/
├── docx_service/
├── xlsx_service/
├── txt_service/
└── README.md
```


---

## 🚀 Instalación y ejecución local

### 📦 Requisitos

- Docker
- Docker Compose
- Python (solo si deseas pruebas fuera del contenedor)

### ▶️ Iniciar todo el sistema

```bash
docker-compose up --build
```

### 📥 Probar el validador
Puedes usar Postman o curl para hacer una solicitud:

```bash
curl -X POST http://localhost:8000/validate-file \
  -F "file=@ruta/al/archivo.pdf"
```



### 📘 Documentación interactiva
Abre en tu navegador:

```bash
http://localhost:8000/docs

```



### 📤 Ejemplo de respuesta JSON

#### 📦 Salida JSON esperada (cuando es válido):

```bash
{
  "id_file": "documento.pdf",
  "time_val_file": "2025-07-05T12:34:56.789123",
  "format": "pdf",
  "weight_file": 1.24,
  "FLAG_OK_file": true,
  "error_type_01_file": false,
  "error_type_02_file": false,
  "error_type_03_file": false,
  "error_type_04_file": false
}
```

#### ❌ Salida si excede el peso:

```bash
{
  "id_file": "pesado.pdf",
  "format": "desconocido",
  "weight_file": 17.83,
  "FLAG_OK_file": false,
  "error_type_01_file": false,
  "error_type_02_file": false,
  "error_type_03_file": false,
  "error_type_04_file": true,
  "message": "Archivo demasiado grande. Máximo permitido: 15MB"
}
```


#### ❌ Salida si excede el tiempo de procesamiento:

```bash
{
  "id_file": "ejemplo.pdf",
  "format": "desconocido",
  "weight_file": 170.83,
  "FLAG_OK_file": false,
  "error_type_01_file": false,
  "error_type_02_file": false,
  "error_type_03_file": false,
  "error_type_04_file": false,
  "message": "El microservicio especializado tardó demasiado en responder"
}
```






