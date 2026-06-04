from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.agents.graph import procesar_pregunta
from src.mcp.calendar_client import ejecutar_herramienta, listar_herramientas
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="DevMotiva + Luna STEM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pregunta(BaseModel):
    texto: str

class HerramientaRequest(BaseModel):
    nombre: str
    params: dict = {}

@app.post("/chat")
def chat(pregunta: Pregunta):
    resultado = procesar_pregunta(pregunta.texto)
    return {
        "respuesta": resultado["respuesta"],
        "recursos": resultado["recursos"],
        "fuentes": resultado["fuentes"]
    }

@app.get("/mcp/tools")
def get_tools():
    return {"tools": listar_herramientas()}

@app.post("/mcp/execute")
def execute_tool(request: HerramientaRequest):
    resultado = ejecutar_herramienta(request.nombre, request.params)
    return {"resultado": resultado}

@app.get("/")
def root():
    return {
        "status": "DevMotiva API funcionando",
        "agentes": ["orientador", "mentor", "curador"],
        "mcp_tools": [t["name"] for t in listar_herramientas()]
    }