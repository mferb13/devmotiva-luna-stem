from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generar_respuesta(estado: dict) -> dict:
    pregunta = estado["pregunta"]
    contexto = estado["contexto"]
    fuentes = estado["fuentes"]

    prompt = f"""Eres una mentora concisa y empática para mujeres desarrolladoras.
Responde SOLO basándote en el contexto proporcionado.
NO uses asteriscos ni formato Markdown excesivo.
NO inventes información. Sé directa y práctica.

Contexto:
{contexto}

Pregunta: {pregunta}

Responde directamente y con calidez, sin encabezados ni etiquetas.
2-3 párrafos cortos basados SOLO en el contexto.
Termina con un consejo práctico concreto."""

    respuesta = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "pregunta": pregunta,
        "contexto": contexto,
        "fuentes": fuentes,
        "respuesta": respuesta.choices[0].message.content
    }