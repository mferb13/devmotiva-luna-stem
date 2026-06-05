\# Decisiones Técnicas — DevMotiva + Luna STEM



\## Decisión 1: LangGraph sobre CrewAI



\*\*Contexto:\*\* Se necesitaba orquestar 3 agentes con roles diferenciados y estado compartido entre ellos.



\*\*Decisión:\*\* Se eligió LangGraph sobre CrewAI.



\*\*Consecuencias:\*\*

\- ✅ Mayor control sobre el flujo de ejecución

\- ✅ Estado tipado con TypedDict, fácil de depurar

\- ✅ Grafo determinístico: Orientador → Mentor → Curador → END

\- ❌ Requiere definir explícitamente cada nodo y arista



\---



\## Decisión 2: ChromaDB sobre FAISS



\*\*Contexto:\*\* Se necesitaba una base de datos vectorial para almacenar 95 chunks del corpus.



\*\*Decisión:\*\* Se eligió ChromaDB sobre FAISS.



\*\*Consecuencias:\*\*

\- ✅ Soporte nativo para metadatos (filtrar por categoría)

\- ✅ Persistencia automática en disco sin código adicional

\- ✅ API más intuitiva para proyectos pequeños y medianos

\- ❌ Menor rendimiento que FAISS en corpus muy grandes



\---



\## Decisión 3: Corpus propio sobre datasets públicos de Hugging Face



\*\*Contexto:\*\* Se necesitaban 15+ documentos especializados en mujeres en tecnología.



\*\*Decisión:\*\* Se crearon 17 documentos .txt propios complementados con 10 artículos de Wikipedia en español.



\*\*Consecuencias:\*\*

\- ✅ Contenido 100% relevante al dominio

\- ✅ Control total sobre calidad y estructura

\- ✅ Respuestas más precisas y contextualizadas

\- ❌ Requirió tiempo de creación manual del contenido



\---



\## Decisión 4: ReportLab sobre fpdf2



\*\*Contexto:\*\* Se necesitaba generar PDFs con contenido en español para la Skill de roadmap.



\*\*Decisión:\*\* Se migró de fpdf2 a ReportLab.



\*\*Consecuencias:\*\*

\- ✅ Manejo correcto de UTF-8 y caracteres especiales del español

\- ✅ Mayor control sobre estilos y layout del PDF

\- ✅ Compatible con Python 3.11 sin conflictos

\- ❌ API más verbosa que fpdf2

