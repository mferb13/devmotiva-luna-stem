import chromadb
from sentence_transformers import SentenceTransformer

client_db = chromadb.PersistentClient(path="./chroma_db")
collection = client_db.get_or_create_collection("devmotiva_corpus")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def buscar_contexto(pregunta: str) -> dict:
    embedding = model.encode(pregunta).tolist()
    resultados = collection.query(
        query_embeddings=[embedding],
        n_results=4
    )
    chunks = resultados["documents"][0]
    metadatas = resultados["metadatas"][0]
    contexto = "\n\n".join(chunks)
    fuentes = list(set([m["category"] for m in metadatas]))
    return {
        "contexto": contexto,
        "fuentes": fuentes,
        "pregunta": pregunta
    }