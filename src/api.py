from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.agents.graph import procesar_pregunta
from src.mcp.calendar_client import ejecutar_herramienta, listar_herramientas
from dotenv import load_dotenv

# --- CARGAR VARIABLES DE ENTORNO ---
# Lee el .env para tener disponible GROQ_API_KEY en todo el sistema
load_dotenv()

# --- INSTANCIA DE FASTAPI ---
# Es el servidor que recibe las peticiones del frontend y Streamlit
app = FastAPI(title="DevMotiva + Luna STEM API")

# --- CORS ---
# Permite que el frontend en React (localhost:8080) y Streamlit (localhost:8501)
# puedan hacer peticiones a esta API (localhost:8000) sin bloqueos del navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Acepta peticiones de cualquier origen
    allow_methods=["*"],    # Acepta GET, POST, etc.
    allow_headers=["*"],    # Acepta cualquier header
)

# --- MODELOS DE DATOS ---
# Pydantic valida automáticamente que los datos del request tengan el formato correcto

class Pregunta(BaseModel):
    texto: str  # Texto de la pregunta de la usuaria

class HerramientaRequest(BaseModel):
    nombre: str     # Nombre de la herramienta MCP a ejecutar
    params: dict = {}  # Parámetros opcionales para la herramienta


# --- ENDPOINT PRINCIPAL: CHAT ---
# Recibe la pregunta del frontend o Streamlit
# La pasa por el flujo completo de los 3 agentes (Orientador → Mentor → Curador)
# Retorna respuesta, recursos sugeridos y fuentes citadas
@app.post("/chat")
def chat(pregunta: Pregunta):
    resultado = procesar_pregunta(pregunta.texto)
    return {
        "respuesta": resultado["respuesta"],  # Generada por el Mentor
        "recursos": resultado["recursos"],    # Sugeridos por el Curador
        "fuentes": resultado["fuentes"]       # Citadas por el Orientador
    }


# --- ENDPOINT MCP: LISTAR HERRAMIENTAS ---
# Retorna todas las herramientas disponibles en el servidor MCP propio
# El frontend puede consultar qué herramientas existen antes de ejecutarlas
@app.get("/mcp/tools")
def get_tools():
    return {"tools": listar_herramientas()}


# --- ENDPOINT MCP: EJECUTAR HERRAMIENTA ---
# Ejecuta una herramienta específica del servidor MCP
# Ejemplo: crear una meta, generar un plan de hábitos
@app.post("/mcp/execute")
def execute_tool(request: HerramientaRequest):
    resultado = ejecutar_herramienta(request.nombre, request.params)
    return {"resultado": resultado}


# --- ENDPOINT DE SALUD ---
# Verifica que la API está funcionando correctamente
# Muestra los agentes activos y las herramientas MCP disponibles
@app.get("/")
def root():
    return {
        "status": "DevMotiva API funcionando",
        "agentes": ["orientador", "mentor", "curador"],
        "mcp_tools": [t["name"] for t in listar_herramientas()]
    }