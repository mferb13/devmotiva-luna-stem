from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generar_roadmap(area: str, tiempo: str, nivel: str) -> str:
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
    contenido = generar_roadmap(area, tiempo, nivel)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    color_morado = HexColor('#4C1D95')
    color_rosa = HexColor('#EC4899')

    estilo_titulo = ParagraphStyle(
        'titulo',
        parent=styles['Title'],
        fontSize=22,
        textColor=color_morado,
        spaceAfter=6
    )
    estilo_subtitulo = ParagraphStyle(
        'subtitulo',
        parent=styles['Normal'],
        fontSize=14,
        textColor=color_rosa,
        spaceAfter=4
    )
    estilo_info = ParagraphStyle(
        'info',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#666666'),
        spaceAfter=12
    )
    estilo_seccion = ParagraphStyle(
        'seccion',
        parent=styles['Normal'],
        fontSize=13,
        textColor=color_morado,
        fontName='Helvetica-Bold',
        spaceAfter=6,
        spaceBefore=10
    )
    estilo_normal = ParagraphStyle(
        'normal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=4,
        leading=16
    )

    elementos = []
    elementos.append(Paragraph("DevMotiva + Luna STEM", estilo_titulo))
    elementos.append(Paragraph(f"Roadmap: {area}", estilo_subtitulo))
    elementos.append(Paragraph(f"Nivel: {nivel} | Tiempo diario: {tiempo}", estilo_info))
    elementos.append(Spacer(1, 0.3*cm))

    for linea in contenido.split("\n"):
        linea = linea.strip()
        if not linea:
            elementos.append(Spacer(1, 0.2*cm))
            continue
        linea_html = linea.replace("**", "<b>", 1).replace("**", "</b>", 1)
        if linea.startswith("##"):
            texto = linea.replace("##", "").strip()
            elementos.append(Paragraph(texto, estilo_seccion))
        elif linea.startswith("*") or linea.startswith("-"):
            texto = linea.lstrip("*- ").strip()
            elementos.append(Paragraph(f"• {texto}", estilo_normal))
        else:
            elementos.append(Paragraph(linea_html, estilo_normal))

    doc.build(elementos)
    return output_path