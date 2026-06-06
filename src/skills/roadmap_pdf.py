from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm
from groq import Groq
from dotenv import load_dotenv
import os

# --- CARGAR VARIABLES DE ENTORNO ---
load_dotenv()

# --- CLIENTE DE GROQ ---
# Usa llama-3.1-8b-instant — modelo ligero suficiente para generar roadmaps
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generar_roadmap(area: str, tiempo: str, nivel: str) -> str:
    """
    Skill principal — genera el contenido del roadmap usando el LLM.
    Recibe el área, tiempo disponible y nivel de la usuaria.
    Retorna el roadmap como texto con formato Markdown.
    """

    # --- PROMPT PERSONALIZADO ---
    # Le pide al LLM un plan de 4 semanas estructurado
    # adaptado al área, tiempo y nivel de la usuaria
    prompt = f"""Eres una mentora experta en tecnologia para mujeres desarrolladoras.
Crea un roadmap de aprendizaje detallado y motivador.
Area: {area}
Tiempo disponible: {tiempo} por dia
Nivel actual: {nivel}
Crea un plan de 4 semanas con:
- Semana 1: Fundamentos
- Semana 2: Practica
- Semana 3: Proyecto
- Semana 4: Consolidacion
Para cada semana incluye: temas, recursos gratuitos y un mini proyecto.
Responde en español."""

    respuesta = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return respuesta.choices[0].message.content


def exportar_pdf(area: str, tiempo: str, nivel: str, output_path: str = "./roadmap.pdf") -> str:
    """
    Skill completa — genera el roadmap y lo exporta como PDF descargable.
    Usa ReportLab para construir el PDF con estilos personalizados.
    Retorna la ruta del PDF generado.
    """

    # --- PASO 1: GENERAR CONTENIDO CON EL LLM ---
    contenido = generar_roadmap(area, tiempo, nivel)

    # --- PASO 2: CONFIGURAR EL DOCUMENTO PDF ---
    # SimpleDocTemplate maneja el layout automáticamente (saltos de página, márgenes)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # --- PASO 3: DEFINIR ESTILOS ---
    # Colores de la identidad visual de DevMotiva
    styles = getSampleStyleSheet()
    color_morado = HexColor('#4C1D95')
    color_rosa = HexColor('#EC4899')

    # Estilo para el título principal
    estilo_titulo = ParagraphStyle(
        'titulo',
        parent=styles['Title'],
        fontSize=22,
        textColor=color_morado,
        spaceAfter=6
    )

    # Estilo para el subtítulo (área del roadmap)
    estilo_subtitulo = ParagraphStyle(
        'subtitulo',
        parent=styles['Normal'],
        fontSize=14,
        textColor=color_rosa,
        spaceAfter=4
    )

    # Estilo para información secundaria (nivel y tiempo)
    estilo_info = ParagraphStyle(
        'info',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#666666'),
        spaceAfter=12
    )

    # Estilo para encabezados de sección (## en el texto)
    estilo_seccion = ParagraphStyle(
        'seccion',
        parent=styles['Normal'],
        fontSize=13,
        textColor=color_morado,
        fontName='Helvetica-Bold',
        spaceAfter=6,
        spaceBefore=10
    )

    # Estilo para el texto normal del roadmap
    estilo_normal = ParagraphStyle(
        'normal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=4,
        leading=16  # Espaciado entre líneas
    )

    # --- PASO 4: CONSTRUIR EL CONTENIDO DEL PDF ---
    elementos = []

    # Encabezado fijo del documento
    elementos.append(Paragraph("DevMotiva + Luna STEM", estilo_titulo))
    elementos.append(Paragraph(f"Roadmap: {area}", estilo_subtitulo))
    elementos.append(Paragraph(f"Nivel: {nivel} | Tiempo diario: {tiempo}", estilo_info))
    elementos.append(Spacer(1, 0.3*cm))

    # --- PASO 5: PARSEAR EL TEXTO DEL LLM ---
    # Convierte el Markdown generado por el LLM en elementos visuales del PDF
    for linea in contenido.split("\n"):
        linea = linea.strip()

        # Línea vacía → espacio en blanco
        if not linea:
            elementos.append(Spacer(1, 0.2*cm))
            continue

        # Convierte **texto** de Markdown a <b>texto</b> de HTML para ReportLab
        linea_html = linea.replace("**", "<b>", 1).replace("**", "</b>", 1)

        # Líneas con ## → encabezado de sección (ej: ## Semana 1)
        if linea.startswith("##"):
            texto = linea.replace("##", "").strip()
            elementos.append(Paragraph(texto, estilo_seccion))

        # Líneas con * o - → elemento de lista con bullet
        elif linea.startswith("*") or linea.startswith("-"):
            texto = linea.lstrip("*- ").strip()
            elementos.append(Paragraph(f"• {texto}", estilo_normal))

        # Cualquier otro texto → párrafo normal
        else:
            elementos.append(Paragraph(linea_html, estilo_normal))

    # --- PASO 6: GENERAR EL PDF ---
    # build() ensambla todos los elementos y escribe el archivo
    doc.build(elementos)

    return output_path  # Retorna la ruta para que Streamlit pueda ofrecerlo para descarga