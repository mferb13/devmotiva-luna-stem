from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv
import os

load_dotenv()

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="devmotiva_corpus",
    metadata={"hnsw:space": "cosine"}
)

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def ingest_text(text, category, doc_id_prefix):
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        doc_id = f"{doc_id_prefix}_{abs(hash(chunk))}"
        collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"category": category, "chunk": i}]
        )

def ingest_local_files():
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
        if any(kw.lower() in title.lower() for kw in keywords):
            docs.append((title, text[:3000]))
            print(f"  Encontrado: {title}")
        if len(docs) >= 10:
            break
    for title, text in docs:
        ingest_text(text, "wikipedia_stem", title.replace(" ", "_"))

if __name__ == "__main__":
    print("Iniciando ingesta completa...")
    ingest_local_files()
    ingest_wikipedia()
    total = collection.count()
    print(f"\nIngesta completa. Total chunks en ChromaDB: {total}")