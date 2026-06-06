# tests/test_agents.py
def test_buscar_contexto_saludo():
    from src.agents.orientador import buscar_contexto
    resultado = buscar_contexto('hola')
    assert resultado['es_saludo'] == True

def test_buscar_contexto_pregunta():
    from src.agents.orientador import buscar_contexto
    resultado = buscar_contexto('como supero el sindrome del impostor')
    assert 'pregunta' in resultado
