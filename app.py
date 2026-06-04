import streamlit as st
import requests
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.skills.roadmap_pdf import exportar_pdf

st.set_page_config(
    page_title="DevMotiva + Luna STEM",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
    .main { background-color: #0f0f1a; }
    .stTextInput input { border-radius: 20px; }
    .stButton button {
        background: linear-gradient(135deg, #6B46C1, #EC4899);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    .user-message {
        background: #1e1e3a;
        border-left: 4px solid #6B46C1;
    }
    .bot-message {
        background: #1a1a2e;
        border-left: 4px solid #EC4899;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🚀 DevMotiva + Luna STEM")
st.markdown("*Tu mentora de IA para mujeres desarrolladoras*")
st.divider()

tab1, tab2 = st.tabs(["💬 Chat con la IA", "📄 Genera tu Roadmap PDF"])

# TAB 1 - CHAT
with tab1:
    st.markdown("### Habla con tu mentora")
    st.markdown("Pregúntame sobre programación, síndrome del impostor, rutas de aprendizaje o motivación.")

    if "historial" not in st.session_state:
        st.session_state.historial = []

    for mensaje in st.session_state.historial:
        if mensaje["rol"] == "usuario":
            st.markdown(f'<div class="chat-message user-message">👩‍💻 <b>Tú:</b> {mensaje["texto"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">🤖 <b>Mentora:</b> {mensaje["texto"]}</div>', unsafe_allow_html=True)
            if mensaje.get("recursos"):
                with st.expander("📚 Recursos recomendados"):
                    st.markdown(mensaje["recursos"])
            if mensaje.get("fuentes"):
                st.caption(f"Fuentes: {', '.join(mensaje['fuentes'])}")

    pregunta = st.text_input("Escribe tu pregunta...", placeholder="Ej: ¿Cómo supero el síndrome del impostor?")

    if st.button("Enviar 💬") and pregunta:
        st.session_state.historial.append({"rol": "usuario", "texto": pregunta})
        with st.spinner("Tu mentora está pensando..."):
            try:
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={"texto": pregunta}
                )
                data = response.json()
                st.session_state.historial.append({
                    "rol": "mentora",
                    "texto": data["respuesta"],
                    "recursos": data.get("recursos", ""),
                    "fuentes": data.get("fuentes", [])
                })
            except Exception as e:
                st.error(f"Error conectando con la API: {e}")
        st.rerun()

    if st.button("Limpiar chat 🗑️"):
        st.session_state.historial = []
        st.rerun()

# TAB 2 - ROADMAP PDF
with tab2:
    st.markdown("### Genera tu roadmap personalizado")
    st.markdown("Cuéntame sobre ti y te creo un plan de aprendizaje de 4 semanas.")

    col1, col2, col3 = st.columns(3)
    with col1:
        area = st.selectbox("¿Qué quieres aprender?", [
            "Desarrollo web frontend",
            "Desarrollo web backend",
            "Ciencia de datos",
            "Inteligencia artificial",
            "Desarrollo móvil",
            "DevOps y cloud"
        ])
    with col2:
        tiempo = st.selectbox("¿Cuánto tiempo tienes al día?", [
            "30 minutos",
            "1 hora",
            "2 horas",
            "3 horas o más"
        ])
    with col3:
        nivel = st.selectbox("¿Cuál es tu nivel actual?", [
            "Principiante (nunca he programado)",
            "Básico (conozco lo fundamental)",
            "Intermedio (tengo proyectos propios)",
            "Avanzado (trabajo en tecnología)"
        ])

    if st.button("Generar mi roadmap 🗺️"):
        with st.spinner("Creando tu plan personalizado..."):
            try:
                pdf_path = exportar_pdf(area, tiempo, nivel, "./mi_roadmap.pdf")
                st.success("¡Tu roadmap está listo!")
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Descargar PDF",
                        data=f,
                        file_name="mi_roadmap_devmotiva.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Error generando el roadmap: {e}")