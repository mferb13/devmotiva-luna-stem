from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generar_respuesta(estado: dict) -> dict:
    pregunta = estado["pregunta"]
    contexto = estado.get("contexto", "")
    fuentes = estado.get("fuentes", [])
    es_saludo = estado.get("es_saludo", False)

    if es_saludo:
        prompt = f"""Eres Luna, una mentora cálida y empática para mujeres desarrolladoras.
La usuaria te está saludando. Responde con un saludo amigable y breve (máximo 2 oraciones).
Pregúntale en qué puedes ayudarle hoy relacionado con programación, rutas de aprendizaje o motivación.
NO menciones concursos, eventos ni temas que ella no haya mencionado."""
    elif not contexto:
        prompt = f"""Eres Luna, una mentora para mujeres desarrolladoras.
La usuaria preguntó: {pregunta}
No tienes información específica sobre ese tema en tu base de conocimiento.
Dile amablemente que no tienes información sobre ese tema exacto y sugiérele reformular la pregunta sobre programación, síndrome del impostor o rutas de aprendizaje.
Máximo 2 oraciones."""
    else:
        prompt = f"""Eres Luna, una mentora concisa y empática para mujeres desarrolladoras.
Responde SOLO basándote en el contexto proporcionado.
NO uses asteriscos ni formato Markdown excesivo.
NO inventes información. Sé directa y práctica.
NO menciones concursos, eventos ni personas que no estén en el contexto.

Contexto:
{contexto}

Pregunta: {pregunta}

Responde directamente y con calidez, sin encabezados ni etiquetas.
2-3 párrafos cortos basados SOLO en el contexto.
Termina con un consejo práctico concreto."""

    respuesta = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "pregunta": pregunta,
        "contexto": contexto,
        "fuentes": fuentes,
        "respuesta": respuesta.choices[0].message.content
    }