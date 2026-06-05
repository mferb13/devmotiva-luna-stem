# 🚀 DevMotiva + Luna STEM

> Asistente inteligente de IA para mujeres desarrolladoras. Combina motivación, orientación técnica y herramientas de productividad en una sola plataforma.

**Proyecto Final — Introducción a la Inteligencia Artificial 2026**  
**Integrantes:** María Fernanda Bedoya & Manuela Cruz  
**Repositorio IA:** https://github.com/mferb13/devmotiva-luna-stem  
**Repositorio Frontend:** https://github.com/mferb13/hack-her-flow

---

## 🎯 ¿Qué hace?

- Responde preguntas sobre programación, síndrome del impostor y rutas de aprendizaje usando RAG
- Coordina 3 agentes con LangGraph: Orientador, Mentor y Curador
- Genera roadmaps PDF personalizados de 4 semanas
- Expone herramientas MCP para metas y hábitos
- Se integra con el frontend DevMotiva via botón "Hablar con Luna STEM 🚀"

---

## 🏗️ Arquitectura

- **LLM:** Groq (llama-3.3-70b-versatile)
- **Embeddings:** paraphrase-multilingual-MiniLM-L12-v2
- **Base vectorial:** ChromaDB (95 chunks, 17 documentos)
- **Agentes:** LangGraph (Orientador → Mentor → Curador)
- **Interfaz IA:** Streamlit (localhost:8501)
- **Frontend:** React/Vite — hack-her-flow (localhost:8080)

---

## ⚙️ Instalación

### Requisitos
- Python 3.11+
- Node.js 18+
- Git
- GROQ_API_KEY (gratis en console.groq.com)

### 1. Clonar los repositorios
```bash
git clone https://github.com/mferb13/devmotiva-luna-stem.git
git clone https://github.com/mferb13/hack-her-flow.git
```

### 2. Configurar el backend (Luna STEM)
```bash
cd devmotiva-luna-stem
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # Mac/Linux
pip install -r requirements.txt
cp .env.example .env
# Edita .env y agrega tu GROQ_API_KEY
```

### 3. Cargar el corpus en ChromaDB
```bash
python src/rag/ingest.py
```

### 4. Configurar el frontend (DevMotiva)
```bash
cd ../hack-her-flow
npm install
```

---

## 🚀 Uso

### Terminal 1 — Backend FastAPI
```bash
cd devmotiva-luna-stem
source venv/Scripts/activate
uvicorn src.api:app --reload
```
API disponible en: http://localhost:8000

### Terminal 2 — Interfaz Streamlit (Luna STEM)
```bash
cd devmotiva-luna-stem
streamlit run app.py
```
Interfaz disponible en: http://localhost:8501

### Terminal 3 — Frontend DevMotiva
```bash
cd hack-her-flow
npm run dev
```
Frontend disponible en: http://localhost:8080

---

## 📁 Estructura del proyecto

devmotiva-luna-stem/
├── src/
│   ├── agents/
│   │   ├── orientador.py    # Busca en ChromaDB con filtro de relevancia
│   │   ├── mentor.py        # Genera respuesta motivacional (Groq)
│   │   ├── curador.py       # Sugiere recursos adicionales
│   │   └── graph.py         # Orquestación LangGraph
│   ├── rag/
│   │   └── ingest.py        # Pipeline ingesta → chunking → embedding
│   ├── skills/
│   │   └── roadmap_pdf.py   # Skill: genera roadmap PDF personalizado
│   ├── mcp/
│   │   └── calendar_client.py  # Servidor MCP propio
│   └── api.py               # FastAPI endpoints
├── data/
│   └── corpus/              # 17 documentos .txt
├── docs/                    # Diagramas y decisiones técnicas
├── tests/
├── app.py                   # Interfaz Streamlit
├── requirements.txt
├── .env.example
└── README.md
hack-her-flow/               # Frontend React/Vite
├── src/
│   └── components/          # Chat flotante con botón Luna STEM
└── …

---

## 🔌 Endpoints API

| Endpoint | Método | Descripción |
|---|---|---|
| `/chat` | POST | Chat con los 3 agentes |
| `/mcp/tools` | GET | Lista herramientas MCP |
| `/mcp/execute` | POST | Ejecuta una herramienta MCP |

---

## 🧠 Conceptos implementados

| Concepto | Implementación |
|---|---|
| Transformer | llama-3.3-70b-versatile vía Groq API |
| Embeddings | paraphrase-multilingual-MiniLM-L12-v2 |
| Base vectorial | ChromaDB local con 95 chunks |
| RAG | Ingesta → chunking → embedding → recuperación con filtro por distancia |
| Multiagentes | LangGraph: Orientador, Mentor, Curador |
| MCP | Servidor propio en src/mcp/calendar_client.py |
| Skills | Generación de roadmap PDF personalizado |

---

## 👩‍💻 Integrantes

- María Fernanda Bedoya — [@mferb13](https://github.com/mferb13)
- Manuela Cruz