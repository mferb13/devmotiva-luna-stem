from groq import Groq
from dotenv import load_dotenv
import os

# --- CARGAR VARIABLES DE ENTORNO ---
# Lee el archivo .env para obtener la GROQ_API_KEY de forma segura
# sin exponerla en el código fuente
load_dotenv()

# --- CLIENTE DE GROQ ---
# Inicializa la conexión con la API de Groq usando la clave del .env
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generar_respuesta(estado: dict) -> dict:
    """
    Agente Mentor — genera la respuesta motivacional usando el LLM.
    Recibe el estado enriquecido por el Orientador y produce la respuesta final.
    """

    # --- EXTRAE DATOS DEL ESTADO COMPARTIDO ---
    # El estado viene del Orientador con contexto, fuentes y tipo de pregunta
    pregunta = estado["pregunta"]
    contexto = estado.get("contexto", "")   # Chunks relevantes del corpus
    fuentes = estado.get("fuentes", [])     # Categorías de las fuentes citadas
    es_saludo = estado.get("es_saludo", False)  # True si fue un saludo corto

    # --- CASO 1: SALUDO ---
    # Si el Orientador detectó un saludo, Luna responde amigablemente
    # sin inventar temas ni mencionar cosas que la usuaria no dijo
    if es_saludo:
        prompt = f"""Eres Luna, una mentora cálida y empática para mujeres desarrolladoras.
La usuaria te está saludando. Responde con un saludo amigable y breve (máximo 2 oraciones).
Pregúntale en qué puedes ayudarle hoy relacionado con programación, rutas de aprendizaje o motivación.
NO menciones concursos, eventos ni temas que ella no haya mencionado."""

    # --- CASO 2: SIN CONTEXTO RELEVANTE ---
    # El Orientador no encontró chunks con distancia < 1.2
    # Luna le avisa a la usuaria que no tiene información sobre ese tema
    elif not contexto:
        prompt = f"""Eres Luna, una mentora para mujeres desarrolladoras.
La usuaria preguntó: {pregunta}
No tienes información específica sobre ese tema en tu base de conocimiento.
Dile amablemente que no tienes información sobre ese tema exacto y sugiérele reformular la pregunta sobre programación, síndrome del impostor o rutas de aprendizaje.
Máximo 2 oraciones."""

    # --- CASO 3: CON CONTEXTO RELEVANTE ---
    # El Orientador encontró chunks útiles — Luna responde basándose SOLO en ellos
    # Esto es el núcleo del RAG: el LLM no inventa, usa el contexto recuperado
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

    # --- LLAMADA AL LLM ---
    # Envía el prompt a llama-3.3-70b-versatile vía Groq
    # max_tokens=300 limita la longitud de la respuesta
    respuesta = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    # --- RETORNA EL ESTADO ACTUALIZADO ---
    # Agrega la respuesta generada al estado para que el Curador la reciba
    return {
        "pregunta": pregunta,
        "contexto": contexto,
        "fuentes": fuentes,
        "respuesta": respuesta.choices[0].message.content  # Texto generado por el LLM
    }