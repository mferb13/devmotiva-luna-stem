from langgraph.graph import StateGraph, END
from typing import TypedDict
from src.agents.orientador import buscar_contexto
from src.agents.mentor import generar_respuesta
from src.agents.curador import sugerir_recursos

# --- ESTADO COMPARTIDO ENTRE AGENTES ---
# TypedDict define la estructura del estado que fluye entre los 3 agentes
# Cada agente recibe este estado, lo enriquece y lo pasa al siguiente
class EstadoAgente(TypedDict):
    pregunta: str      # Pregunta original de la usuaria
    contexto: str      # Chunks relevantes encontrados por el Orientador
    fuentes: list      # Categorías de las fuentes citadas
    respuesta: str     # Respuesta generada por el Mentor
    recursos: str      # Recursos sugeridos por el Curador
    es_saludo: bool    # True si la pregunta fue un saludo corto


# --- NODOS DEL GRAFO ---
# Cada nodo envuelve a un agente y actualiza el estado compartido

def nodo_orientador(estado: EstadoAgente) -> EstadoAgente:
    """Llama al Orientador — busca contexto en ChromaDB"""
    resultado = buscar_contexto(estado["pregunta"])
    return {**estado, **resultado}  # Fusiona el estado actual con el resultado

def nodo_mentor(estado: EstadoAgente) -> EstadoAgente:
    """Llama al Mentor — genera la respuesta con Groq"""
    resultado = generar_respuesta(estado)
    return {**estado, **resultado}

def nodo_curador(estado: EstadoAgente) -> EstadoAgente:
    """Llama al Curador — sugiere recursos adicionales"""
    resultado = sugerir_recursos(estado)
    return {**estado, **resultado}


def crear_grafo():
    """
    Construye y compila el grafo de agentes con LangGraph.
    Define el flujo: Orientador → Mentor → Curador → END
    """

    # --- CREAR EL GRAFO ---
    # StateGraph recibe el TypedDict para validar el estado en cada nodo
    grafo = StateGraph(EstadoAgente)

    # --- REGISTRAR LOS NODOS ---
    # Asocia un nombre con la función de cada agente
    grafo.add_node("orientador", nodo_orientador)
    grafo.add_node("mentor", nodo_mentor)
    grafo.add_node("curador", nodo_curador)

    # --- DEFINIR EL FLUJO ---
    # El Orientador es el punto de entrada — siempre ejecuta primero
    grafo.set_entry_point("orientador")

    # Aristas: definen el orden de ejecución secuencial
    grafo.add_edge("orientador", "mentor")   # Después del Orientador → Mentor
    grafo.add_edge("mentor", "curador")      # Después del Mentor → Curador
    grafo.add_edge("curador", END)           # Después del Curador → termina

    # --- COMPILAR ---
    # Valida el grafo y lo deja listo para invocar
    return grafo.compile()


# --- INSTANCIA GLOBAL DEL AGENTE ---
# Se compila una sola vez al cargar el módulo para no recompilar en cada request
agente = crear_grafo()


def procesar_pregunta(pregunta: str) -> dict:
    """
    Función principal que recibe la pregunta de la usuaria
    y ejecuta el flujo completo de los 3 agentes.
    """

    # --- ESTADO INICIAL ---
    # Todos los campos vacíos excepto la pregunta
    # Cada agente irá llenando los campos a medida que avanza
    estado_inicial = {
        "pregunta": pregunta,
        "contexto": "",      # El Orientador lo llenará
        "fuentes": [],       # El Orientador lo llenará
        "respuesta": "",     # El Mentor lo llenará
        "recursos": "",      # El Curador lo llenará
        "es_saludo": False   # El Orientador lo actualizará si es saludo
    }

    # --- EJECUTAR EL GRAFO ---
    # invoke() corre todos los nodos en orden y retorna el estado final
    resultado = agente.invoke(estado_inicial)
    return resultado