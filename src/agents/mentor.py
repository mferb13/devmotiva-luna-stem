from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generar_respuesta(estado: dict) -> dict:
    pregunta = estado["pregunta"]
    contexto = estado["contexto"]
    fuentes = estado["fuentes"]

    prompt = f"""Eres una mentora empática y motivadora para mujeres desarrolladoras.
Tu rol es responder preguntas usando el contexto proporcionado.
Responde en español, de forma cálida, motivadora y con consejos prácticos.

Contexto recuperado:
{contexto}

Pregunta de la usuaria: {pregunta}

Responde de forma estructurada:
1. Validación emocional (1-2 oraciones)
2. Respuesta basada en el contexto (3-4 párrafos)
3. Consejo práctico concreto (1-2 oraciones)
"""

    respuesta = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "pregunta": pregunta,
        "contexto": contexto,
        "fuentes": fuentes,
        "respuesta": respuesta.choices[0].message.content
    }