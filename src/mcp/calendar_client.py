from groq import Groq
from dotenv import load_dotenv
import json
import os
from datetime import datetime

# --- CARGAR VARIABLES DE ENTORNO ---
load_dotenv()

# --- CLIENTE DE GROQ ---
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- DEFINICIÓN DE HERRAMIENTAS MCP ---
# MCP (Model Context Protocol) permite exponer herramientas externas
# para que los agentes las puedan usar desde la API
# Cada herramienta tiene nombre, descripción y parámetros que recibe
MCP_TOOLS = [
    {
        "name": "crear_meta",
        "description": "Crea una meta SMART para la usuaria",
        "parameters": {
            "titulo": "string",        # Nombre de la meta
            "descripcion": "string",   # Descripción detallada
            "fecha_limite": "string"   # Fecha límite para cumplirla
        }
    },
    {
        "name": "obtener_consejo_meta",
        "description": "Da un consejo motivacional para cumplir una meta",
        "parameters": {
            "meta": "string",          # Meta que quiere lograr
            "dificultad": "string"     # Qué tan difícil le parece (fácil/media/difícil)
        }
    },
    {
        "name": "generar_plan_habitos",
        "description": "Genera un plan de hábitos diarios para alcanzar una meta",
        "parameters": {
            "meta": "string",              # Meta que quiere lograr
            "tiempo_disponible": "string"  # Cuánto tiempo tiene al día
        }
    }
]


def ejecutar_herramienta(nombre: str, params: dict) -> str:
    """
    Ejecuta la herramienta MCP solicitada por nombre.
    Recibe el nombre de la herramienta y sus parámetros.
    Retorna el resultado como string (JSON o texto).
    """

    # --- HERRAMIENTA 1: CREAR META ---
    # No usa el LLM — solo estructura los datos en formato JSON
    # y confirma que la meta fue creada exitosamente
    if nombre == "crear_meta":
        return json.dumps({
            "status": "creada",
            "meta": params.get("titulo"),
            "fecha_limite": params.get("fecha_limite"),
            "mensaje": f"Meta '{params.get('titulo')}' creada exitosamente"
        })

    # --- HERRAMIENTA 2: CONSEJO MOTIVACIONAL ---
    # Usa el LLM para generar un consejo personalizado
    # según la meta y el nivel de dificultad percibido
    elif nombre == "obtener_consejo_meta":
        prompt = f"""Da un consejo motivacional corto y práctico para una mujer desarrolladora
que quiere lograr esta meta: {params.get('meta')}
Nivel de dificultad percibido: {params.get('dificultad')}
Responde en 2-3 oraciones en español."""

        respuesta = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Modelo ligero — tarea simple
            messages=[{"role": "user", "content": prompt}]
        )
        return respuesta.choices[0].message.content

    # --- HERRAMIENTA 3: PLAN DE HÁBITOS ---
    # Usa el LLM para generar 5 hábitos diarios concretos
    # adaptados al tiempo disponible de la usuaria
    elif nombre == "generar_plan_habitos":
        prompt = f"""Crea un plan de hábitos diarios simple para lograr esta meta: {params.get('meta')}
Tiempo disponible: {params.get('tiempo_disponible')}
Lista 5 hábitos concretos en español, uno por línea."""

        respuesta = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return respuesta.choices[0].message.content

    # --- HERRAMIENTA NO ENCONTRADA ---
    # Si el nombre no coincide con ninguna herramienta registrada
    return json.dumps({"error": f"Herramienta {nombre} no encontrada"})


def listar_herramientas() -> list:
    """
    Retorna la lista completa de herramientas MCP disponibles.
    Se expone en el endpoint GET /mcp/tools de la API.
    """
    return MCP_TOOLS