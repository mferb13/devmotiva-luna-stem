from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def sugerir_recursos(estado: dict) -> dict:
    pregunta = estado["pregunta"]
    fuentes = estado["fuentes"]

    prompt = f"""Eres una curadora de recursos para mujeres en tecnología.
Basándote en la pregunta de la usuaria, sugiere 3 recursos concretos y gratuitos.
Responde en español. Formato: nombre del recurso, por qué es útil, URL si la conoces.

Pregunta: {pregunta}
Temas relacionados: {", ".join(fuentes)}

Sugiere exactamente 3 recursos relevantes:"""

    respuesta = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "pregunta": estado["pregunta"],
        "respuesta": estado["respuesta"],
        "fuentes": estado["fuentes"],
        "recursos": respuesta.choices[0].message.content
    }