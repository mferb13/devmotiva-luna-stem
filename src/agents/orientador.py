import chromadb
from sentence_transformers import SentenceTransformer

# --- CONEXIÓN A CHROMADB ---
# Crea o abre la base de datos vectorial persistente en disco
client_db = chromadb.PersistentClient(path="./chroma_db")

# Obtiene la colección donde están almacenados los 95 chunks del corpus
collection = client_db.get_or_create_collection("devmotiva_corpus")

# --- MODELO DE EMBEDDINGS ---
# Carga el modelo multilingüe para convertir texto en vectores de 384 dimensiones
# Se carga UNA sola vez al iniciar para no repetir el proceso en cada pregunta
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def buscar_contexto(pregunta: str) -> dict:
    """
    Agente Orientador — busca contexto relevante en ChromaDB
    para responder la pregunta de la usuaria.
    """

    # --- DETECCIÓN DE SALUDOS ---
    # Si la pregunta es un saludo o muy corta (menos de 10 caracteres),
    # no tiene sentido buscar en el corpus — se marca como saludo
    saludos = ["hola", "hi", "hello", "buenas", "hey", "buenos dias", "buenas tardes", "buenas noches"]
    if pregunta.lower().strip() in saludos or len(pregunta.strip()) < 10:
        return {
            "contexto": "",       # Sin contexto — no hay qué buscar
            "fuentes": [],        # Sin fuentes
            "pregunta": pregunta,
            "es_saludo": True     # Le avisa al Mentor que debe saludar
        }

    # --- EMBEDDING DE LA PREGUNTA ---
    # Convierte la pregunta en un vector numérico de 384 dimensiones
    # Esto permite comparar semánticamente con los chunks del corpus
    embedding = model.encode(pregunta).tolist()

    # --- BÚSQUEDA EN CHROMADB ---
    # Busca los 3 chunks más similares al embedding de la pregunta
    # Incluye documentos, metadatos y distancias para poder filtrar
    resultados = collection.query(
        query_embeddings=[embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )

    chunks = resultados["documents"][0]    # Textos de los chunks encontrados
    metadatas = resultados["metadatas"][0] # Metadatos (categoría, fuente)
    distances = resultados["distances"][0] # Distancia coseno — qué tan relevante es

    # --- FILTRO DE RELEVANCIA (mejora sobre RAG básico) ---
    # Solo se usan chunks con distancia < 1.2
    # Distancia alta = el chunk no es relevante para la pregunta
    # Esto evita que el LLM reciba contexto irrelevante e invente respuestas
    chunks_filtrados = []
    metadatas_filtradas = []
    for chunk, meta, dist in zip(chunks, metadatas, distances):
        if dist < 1.2:
            chunks_filtrados.append(chunk)
            metadatas_filtradas.append(meta)

    # --- SIN RESULTADOS RELEVANTES ---
    # Si ningún chunk pasó el filtro, se retorna vacío
    # El Mentor sabrá que no hay información y responderá apropiadamente
    if not chunks_filtrados:
        return {
            "contexto": "",
            "fuentes": [],
            "pregunta": pregunta,
            "es_saludo": False
        }

    # --- CONSTRUCCIÓN DEL CONTEXTO ---
    # Une los chunks relevantes en un solo texto para pasarlo al Mentor
    contexto = "\n\n".join(chunks_filtrados)

    # Extrae las categorías únicas de los metadatos como fuentes citadas
    fuentes = list(set([m["category"] for m in metadatas_filtradas]))

    return {
        "contexto": contexto,     # Texto relevante para que el Mentor responda
        "fuentes": fuentes,       # Fuentes para citar en la respuesta
        "pregunta": pregunta,
        "es_saludo": False
    }