from groq import Groq
from dotenv import load_dotenv
import json
import os
from datetime import datetime

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# MCP propio: herramientas que los agentes pueden usar
MCP_TOOLS = [
    {
        "name": "crear_meta",
        "description": "Crea una meta SMART para la usuaria",
        "parameters": {
            "titulo": "string",
            "descripcion": "string",
            "fecha_limite": "string"
        }
    },
    {
        "name": "obtener_consejo_meta",
        "description": "Da un consejo motivacional para cumplir una meta",
        "parameters": {
            "meta": "string",
            "dificultad": "string"
        }
    },
    {
        "name": "generar_plan_habitos",
        "description": "Genera un plan de hábitos diarios para alcanzar una meta",
        "parameters": {
            "meta": "string",
            "tiempo_disponible": "string"
        }
    }
]

def ejecutar_herramienta(nombre: str, params: dict) -> str:
    if nombre == "crear_meta":
        return json.dumps({
            "status": "creada",
            "meta": params.get("titulo"),
            "fecha_limite": params.get("fecha_limite"),
            "mensaje": f"Meta '{params.get('titulo')}' creada exitosamente"
        })

    elif nombre == "obtener_consejo_meta":
        prompt = f"""Da un consejo motivacional corto y práctico para una mujer desarrolladora
que quiere lograr esta meta: {params.get('meta')}
Nivel de dificultad percibido: {params.get('dificultad')}
Responde en 2-3 oraciones en español."""
        respuesta = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return respuesta.choices[0].message.content

    elif nombre == "generar_plan_habitos":
        prompt = f"""Crea un plan de hábitos diarios simple para lograr esta meta: {params.get('meta')}
Tiempo disponible: {params.get('tiempo_disponible')}
Lista 5 hábitos concretos en español, uno por línea."""
        respuesta = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return respuesta.choices[0].message.content

    return json.dumps({"error": f"Herramienta {nombre} no encontrada"})

def listar_herramientas() -> list:
    return MCP_TOOLS