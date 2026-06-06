from groq import Groq
from dotenv import load_dotenv
import os

# --- CARGAR VARIABLES DE ENTORNO ---
# Lee el archivo .env para obtener la GROQ_API_KEY de forma segura
load_dotenv()

# --- CLIENTE DE GROQ ---
# Usa un modelo más ligero (llama-3.1-8b-instant) porque sugerir recursos
# es una tarea más simple que generar la respuesta motivacional
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def sugerir_recursos(estado: dict) -> dict:
    """
    Agente Curador — sugiere 3 recursos gratuitos y relevantes
    basándose en la pregunta y las fuentes encontradas por el Orientador.
    Es el último agente en ejecutarse en el flujo.
    """

    # --- EXTRAE DATOS DEL ESTADO ---
    # Recibe el estado ya enriquecido por Orientador y Mentor
    pregunta = estado["pregunta"]   # Pregunta original de la usuaria
    fuentes = estado["fuentes"]     # Categorías del corpus (ej: stem_*, impostor_*)

    # --- CONSTRUCCIÓN DEL PROMPT ---
    # Le pide al LLM exactamente 3 recursos concretos y gratuitos
    # Usa las fuentes del Orientador como contexto temático
    prompt = f"""Eres una curadora de recursos para mujeres en tecnología.
Basándote en la pregunta de la usuaria, sugiere 3 recursos concretos y gratuitos.
Responde en español. Formato: nombre del recurso, por qué es útil, URL si la conoces.
Pregunta: {pregunta}
Temas relacionados: {", ".join(fuentes)}
Sugiere exactamente 3 recursos relevantes:"""

    # --- LLAMADA AL LLM ---
    # Usa llama-3.1-8b-instant (más rápido y liviano)
    # porque esta tarea no requiere el modelo de 70B
    respuesta = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    # --- RETORNA EL ESTADO FINAL ---
    # Conserva pregunta, respuesta y fuentes del estado anterior
    # y agrega los recursos sugeridos — este es el estado final del sistema
    return {
        "pregunta": estado["pregunta"],
        "respuesta": estado["respuesta"],   # Respuesta del Mentor (sin cambios)
        "fuentes": estado["fuentes"],       # Fuentes del Orientador (sin cambios)
        "recursos": respuesta.choices[0].message.content  # Recursos generados
    }