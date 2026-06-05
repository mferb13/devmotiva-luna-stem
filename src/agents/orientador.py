import chromadb
from sentence_transformers import SentenceTransformer

client_db = chromadb.PersistentClient(path="./chroma_db")
collection = client_db.get_or_create_collection("devmotiva_corpus")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def buscar_contexto(pregunta: str) -> dict:
    saludos = ["hola", "hi", "hello", "buenas", "hey", "buenos dias", "buenas tardes", "buenas noches"]
    if pregunta.lower().strip() in saludos or len(pregunta.strip()) < 10:
        return {
            "contexto": "",
            "fuentes": [],
            "pregunta": pregunta,
            "es_saludo": True
        }

    embedding = model.encode(pregunta).tolist()
    resultados = collection.query(
        query_embeddings=[embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )

    chunks = resultados["documents"][0]
    metadatas = resultados["metadatas"][0]
    distances = resultados["distances"][0]

    chunks_filtrados = []
    metadatas_filtradas = []
    for chunk, meta, dist in zip(chunks, metadatas, distances):
        if dist < 1.2:
            chunks_filtrados.append(chunk)
            metadatas_filtradas.append(meta)

    if not chunks_filtrados:
        return {
            "contexto": "",
            "fuentes": [],
            "pregunta": pregunta,
            "es_saludo": False
        }

    contexto = "\n\n".join(chunks_filtrados)
    fuentes = list(set([m["category"] for m in metadatas_filtradas]))

    return {
        "contexto": contexto,
        "fuentes": fuentes,
        "pregunta": pregunta,
        "es_saludo": False
    }