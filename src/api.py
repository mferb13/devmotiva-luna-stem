from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
client_db = chromadb.PersistentClient(path="./chroma_db")
collection = client_db.get_or_create_collection("devmotiva_corpus")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Pregunta(BaseModel):
    texto: str

@app.post("/chat")
def chat(pregunta: Pregunta):
    embedding = model.encode(pregunta.texto).tolist()
    resultados = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )
    contexto = "\n\n".join(resultados["documents"][0])
    prompt = f"""Eres una mentora empática para mujeres desarrolladoras.
Usa el siguiente contexto para responder la pregunta.
Responde en español, de forma motivadora y práctica.

Contexto:
{contexto}

Pregunta: {pregunta.texto}

Respuesta:"""

    respuesta = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return {
        "respuesta": respuesta.choices[0].message.content,
        "fuentes": resultados["metadatas"][0]
    }

@app.get("/")
def root():
    return {"status": "DevMotiva API funcionando"}