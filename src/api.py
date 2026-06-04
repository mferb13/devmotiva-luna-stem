from fastapi import FastAPI
from pydantic import BaseModel
from src.agents.graph import procesar_pregunta
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="DevMotiva + Luna STEM API")

class Pregunta(BaseModel):
    texto: str

@app.post("/chat")
def chat(pregunta: Pregunta):
    resultado = procesar_pregunta(pregunta.texto)
    return {
        "respuesta": resultado["respuesta"],
        "recursos": resultado["recursos"],
        "fuentes": resultado["fuentes"]
    }

@app.get("/")
def root():
    return {"status": "DevMotiva API funcionando", "agentes": ["orientador", "mentor", "curador"]}