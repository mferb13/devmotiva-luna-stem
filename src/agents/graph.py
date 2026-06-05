from langgraph.graph import StateGraph, END
from typing import TypedDict
from src.agents.orientador import buscar_contexto
from src.agents.mentor import generar_respuesta
from src.agents.curador import sugerir_recursos

class EstadoAgente(TypedDict):
    pregunta: str
    contexto: str
    fuentes: list
    respuesta: str
    recursos: str
    es_saludo: bool

def nodo_orientador(estado: EstadoAgente) -> EstadoAgente:
    resultado = buscar_contexto(estado["pregunta"])
    return {**estado, **resultado}

def nodo_mentor(estado: EstadoAgente) -> EstadoAgente:
    resultado = generar_respuesta(estado)
    return {**estado, **resultado}

def nodo_curador(estado: EstadoAgente) -> EstadoAgente:
    resultado = sugerir_recursos(estado)
    return {**estado, **resultado}

def crear_grafo():
    grafo = StateGraph(EstadoAgente)
    grafo.add_node("orientador", nodo_orientador)
    grafo.add_node("mentor", nodo_mentor)
    grafo.add_node("curador", nodo_curador)
    grafo.set_entry_point("orientador")
    grafo.add_edge("orientador", "mentor")
    grafo.add_edge("mentor", "curador")
    grafo.add_edge("curador", END)
    return grafo.compile()

agente = crear_grafo()

def procesar_pregunta(pregunta: str) -> dict:
    estado_inicial = {
        "pregunta": pregunta,
        "contexto": "",
        "fuentes": [],
        "respuesta": "",
        "recursos": "",
        "es_saludo": False
    }
    resultado = agente.invoke(estado_inicial)
    return resultado