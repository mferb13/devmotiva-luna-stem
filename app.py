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
    .stButton button {
        background: linear-gradient(135deg, #6B46C1, #EC4899);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    /* Fija el chat input al fondo */
    .stChatInput {
        position: fixed;
        bottom: 1rem;
        width: 60%;
        z-index: 999;
    }
    /* Espacio para que el historial no quede tapado por el input */
    .chat-container {
        padding-bottom: 80px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🚀 DevMotiva + Luna STEM")
st.markdown("*Tu mentora de IA para mujeres desarrolladoras*")
st.markdown('<a href="http://localhost:8080" target="_blank"><button style="background: linear-gradient(135deg, #6B46C1, #EC4899); color: white; border-radius: 20px; border: none; padding: 0.5rem 2rem; font-weight: bold; cursor: pointer;">← Volver a DevMotiva</button></a>', unsafe_allow_html=True)
st.divider()

tab1, tab2 = st.tabs(["💬 Chat con la IA", "📄 Genera tu Roadmap PDF"])

with tab1:
    st.markdown("### Habla con tu mentora")
    st.markdown("Pregúntame sobre programación, síndrome del impostor, rutas de aprendizaje o motivación.")

    if "historial" not in st.session_state:
        st.session_state.historial = []

    # Contenedor del historial con clase para padding
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for mensaje in st.session_state.historial:
        if mensaje["rol"] == "usuario":
            with st.chat_message("user"):
                st.markdown(mensaje["texto"])
        else:
            with st.chat_message("assistant"):
                st.markdown(mensaje["texto"])
                if mensaje.get("recursos"):
                    with st.expander("📚 Recursos recomendados"):
                        st.markdown(mensaje["recursos"])
                if mensaje.get("fuentes"):
                    st.caption(f"Fuentes: {', '.join(mensaje['fuentes'])}")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Limpiar chat 🗑️"):
        st.session_state.historial = []
        st.rerun()

    # Input fijo al fondo
    pregunta = st.chat_input("Escribe tu pregunta y presiona Enter...")

    if pregunta:
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
                st.session_state.historial.append({
                    "rol": "mentora",
                    "texto": f"Error conectando con la API: {e}",
                    "recursos": "",
                    "fuentes": []
                })
        st.rerun()

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