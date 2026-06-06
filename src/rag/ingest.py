from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv
import os

# --- CARGAR VARIABLES DE ENTORNO ---
load_dotenv()

# --- CONEXIÓN A CHROMADB ---
# Crea o abre la base de datos vectorial persistente en disco
client = chromadb.PersistentClient(path="./chroma_db")

# Colección con similitud coseno — ideal para comparar textos
collection = client.get_or_create_collection(
    name="devmotiva_corpus",
    metadata={"hnsw:space": "cosine"}
)

# --- MODELO DE EMBEDDINGS ---
# Se carga UNA sola vez para no repetir en cada chunk
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def chunk_text(text, chunk_size=500, overlap=50):
    # Divide el texto en chunks de 500 palabras
    # overlap=50 repite las últimas 50 palabras en el siguiente chunk
    # para no perder contexto en los bordes
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks


def ingest_text(text, category, doc_id_prefix):
    # Pipeline: texto → chunks → embeddings → ChromaDB
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()  # Vector de 384 dimensiones
        doc_id = f"{doc_id_prefix}_{abs(hash(chunk))}"  # ID único por chunk
        collection.upsert(  # upsert = insert si no existe, update si ya existe
            ids=[doc_id],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"category": category, "chunk": i}]
        )


def ingest_local_files():
    # Carga los 17 documentos .txt propios desde data/corpus/
    # El nombre del archivo se usa como categoría para filtrar en el Orientador
    corpus_path = "./data/corpus"
    archivos = [f for f in os.listdir(corpus_path) if f.endswith(".txt")]
    print(f"\nCargando {len(archivos)} archivos locales...")
    for filename in archivos:
        with open(os.path.join(corpus_path, filename), "r", encoding="utf-8") as f:
            text = f.read()
        category = filename.replace(".txt", "")
        ingest_text(text, category, category)
        print(f"  Cargado: {filename}")


def ingest_wikipedia():
    # Descarga artículos de Wikipedia en español sobre mujeres en STEM
    # streaming=True evita descargar todo el dataset — lee solo lo necesario
    # Se limita a 10 artículos para no sobrecargar el corpus
    print("Cargando articulos de Wikipedia...")
    dataset = load_dataset(
        "wikimedia/wikipedia",
        "20231101.es",
        split="train",
        streaming=True
    )
    keywords = [
        "Ada Lovelace", "Grace Hopper", "Katherine Johnson",
        "Hedy Lamarr", "Marie Curie", "Maryam Mirzakhani",
        "sindrome del impostor", "mujeres en tecnologia"
    ]
    docs = []
    for article in dataset:
        title = article.get("title", "")
        text = article.get("text", "")
        # Si el título contiene alguna palabra clave — se incluye
        if any(kw.lower() in title.lower() for kw in keywords):
            docs.append((title, text[:3000]))  # Solo primeros 3000 caracteres
            print(f"  Encontrado: {title}")
        if len(docs) >= 10:
            break
    for title, text in docs:
        ingest_text(text, "wikipedia_stem", title.replace(" ", "_"))


# Solo se ejecuta cuando corres: python src/rag/ingest.py
if __name__ == "__main__":
    print("Iniciando ingesta completa...")
    ingest_local_files()   # Paso 1: documentos propios
    ingest_wikipedia()     # Paso 2: artículos de Wikipedia
    total = collection.count()
    print(f"\nIngesta completa. Total chunks en ChromaDB: {total}")