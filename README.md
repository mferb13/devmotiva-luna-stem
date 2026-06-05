\# 🚀 DevMotiva + Luna STEM



> Asistente inteligente de IA para mujeres desarrolladoras. Combina motivación, orientación técnica y herramientas de productividad en una sola plataforma.



\*\*Proyecto Final — Introducción a la Inteligencia Artificial 2026\*\*  

\*\*Repositorio:\*\* https://github.com/mferb13/devmotiva-luna-stem



\---



\## 🎯 ¿Qué hace?



\- Responde preguntas sobre programación, síndrome del impostor y rutas de aprendizaje usando RAG

\- Coordina 3 agentes con LangGraph: Orientador, Mentor y Curador

\- Genera roadmaps PDF personalizados de 4 semanas

\- Expone herramientas MCP para metas y hábitos

\- Se integra con el frontend DevMotiva via chat flotante



\---



\## 🏗️ Arquitectura

\- \*\*LLM:\*\* Groq (Llama 3.1-8b-instant)

\- \*\*Embeddings:\*\* paraphrase-multilingual-MiniLM-L12-v2

\- \*\*Base vectorial:\*\* ChromaDB (95 chunks)

\- \*\*Agentes:\*\* LangGraph

\- \*\*Interfaz:\*\* Streamlit + DevMotiva (React)



\---



\## ⚙️ Instalación



\### Requisitos

\- Python 3.11+

\- Node.js 18+

\- Git



\### 1. Clonar el repositorio

```bash

git clone https://github.com/mferb13/devmotiva-luna-stem.git

cd devmotiva-luna-stem

```



\### 2. Crear entorno virtual

```bash

python -m venv venv

source venv/Scripts/activate  # Windows

source venv/bin/activate       # Mac/Linux

```



\### 3. Instalar dependencias

```bash

pip install -r requirements.txt

```



\### 4. Configurar variables de entorno

```bash

cp .env.example .env

\# Edita .env y agrega tu GROQ\_API\_KEY desde console.groq.com

```



\### 5. Cargar el corpus en ChromaDB

```bash

python src/rag/ingest.py

```



\---



\## 🚀 Uso



\### Terminal 1 — API FastAPI

```bash

uvicorn src.api:app --reload

```

API disponible en: http://localhost:8000  

Documentación: http://localhost:8000/docs



\### Terminal 2 — Interfaz Streamlit

```bash

streamlit run app.py

```

Interfaz disponible en: http://localhost:8501



\---



\## 📁 Estructura del proyecto

devmotiva-luna-stem/

├── src/

│   ├── agents/

│   │   ├── orientador.py    # Busca en ChromaDB

│   │   ├── mentor.py        # Genera respuesta motivacional

│   │   ├── curador.py       # Sugiere recursos

│   │   └── graph.py         # Orquestación LangGraph

│   ├── rag/

│   │   └── ingest.py        # Pipeline de ingesta

│   ├── skills/

│   │   └── roadmap\_pdf.py   # Skill: genera PDF

│   ├── mcp/

│   │   └── calendar\_client.py # Servidor MCP propio

│   └── api.py               # FastAPI endpoints

├── data/

│   └── corpus/              # 17 documentos .txt

├── docs/                    # Diagramas y decisiones técnicas

├── tests/

├── app.py                   # Interfaz Streamlit

├── requirements.txt

├── .env.example

└── README.md



\---



\## 🔌 Endpoints MCP



| Endpoint | Método | Descripción |

|---|---|---|

| `/chat` | POST | Chat con los 3 agentes |

| `/mcp/tools` | GET | Lista herramientas MCP |

| `/mcp/execute` | POST | Ejecuta una herramienta MCP |



\---



\## 👩‍💻 Integrante



\- María Fernanda bedoya y manuela cruz — \[@mferb13](https://github.com/mferb13)

