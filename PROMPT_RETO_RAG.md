# PROMPT MAESTRO COMPLETO - Sistema RAG usando Framework C.R.E.A.T.E

```
=== C - CONTEXTO ===
Actúa como un senior AI/ML engineer especializado en sistemas RAG (Retrieval-Augmented Generation) y automatización CI/CD.
Estoy implementando un reto para el "Certificado en Desarrollo de Software con IA Generativa" que requiere crear un sistema RAG completo para consultar documentos internos de empresa.
El proyecto debe demostrar competencias en IA generativa, prompt engineering, LangChain, bases de datos vectoriales y DevOps.
Necesito una solución production-ready que se ejecute automáticamente y pase validaciones de CI/CD.

=== R - REQUISITOS ===
ANTES DE PROGRAMAR, CREA UN PLAN PASO A PASO DETALLADO que incluya:
1. Arquitectura del sistema RAG (diagrama textual)
2. Pipeline de procesamiento (flujo de datos)
3. Lista de archivos a generar con descripción
4. Dependencias y tecnologías específicas
5. Estrategia de testing y validación
6. Configuración de CI/CD

DESPUÉS implementa un sistema RAG que:
- Procese documentos PDF y TXT de empresa (políticas y guías técnicas)
- Implemente pipeline completo: extracción → chunking → embeddings → vectorstore → retrieval → generación
- Responda 10 consultas específicas: 5 directas sobre documentos internos + 5 capciosas para validación
- Incluya documentos de ejemplo auto-generados
- Funcione con CI/CD automatizado en GitHub Actions
- Tenga testing completo y documentación exhaustiva

=== E - ESPECIFICACIONES ===
**Stack Tecnológico:**
- Python 3.9+
- LangChain (NO usar langchain.document_loaders - DEPRECADO, usar langchain_community.document_loaders)
- OpenAI API (text-embedding-3-small + gpt-4o-mini)
- ChromaDB para almacenamiento vectorial local
- GitHub Actions para CI/CD
- unittest para testing

**Configuración del Sistema (OPTIMIZADA):**
- Chunk size: 1200 caracteres, overlap: 200 (optimizado para mejor contexto)
- Retrieval: k=7 documentos por consulta con búsqueda "mmr" (Maximal Marginal Relevance)
- Lambda mult: 0.5 (balance diversidad vs relevancia)
- Fetch k: 20 (candidatos para MMR)
- Carga automática: todos los archivos .txt y .pdf desde directorio sample_docs/
- Vector store: persistente en ./chroma_db/
- API key: configurable via .env
- Rate limiting: pausas automáticas

**Documentos de Ejemplo (auto-generar en sample_docs/):**

**1. Archivo: manual_politicas.txt**
```
Manual de Políticas de la Empresa TechCorp

1. POLÍTICAS DE TRABAJO REMOTO

1.1 Elegibilidad
Los empleados pueden trabajar de forma remota si:
- Han completado al menos 6 meses en la empresa
- Su supervisor directo aprueba la solicitud
- Su rol permite trabajo remoto efectivo

1.2 Horarios de Trabajo
- Horario flexible entre 7:00 AM y 7:00 PM
- Mínimo 6 horas de solapamiento con el equipo
- Disponibilidad para reuniones importantes

2. POLÍTICAS DE VACACIONES

2.1 Días de Vacaciones
- Empleados nuevos: 15 días al año
- Empleados con 2+ años: 20 días al año
- Empleados con 5+ años: 25 días al año

2.2 Solicitud de Vacaciones
- Solicitar con al menos 2 semanas de anticipación
- Aprobación requerida del supervisor
- No más de 10 días consecutivos sin aprobación especial

3. CÓDIGO DE CONDUCTA

3.1 Principios Básicos
- Respeto mutuo entre colegas
- Confidencialidad de información empresarial
- Profesionalismo en todas las interacciones

3.2 Uso de Tecnología
- Equipos de la empresa solo para uso profesional
- Prohibido instalar software no autorizado
- Reportar inmediatamente cualquier problema de seguridad
```

**2. Archivo: guia_desarrollo.txt**
```
Guía de Desarrollo de Software - TechCorp

1. ESTÁNDARES DE CÓDIGO

1.1 Lenguajes de Programación
- Python: Seguir PEP 8
- JavaScript: Usar ESLint con configuración estándar
- Java: Seguir Google Java Style Guide

1.2 Documentación
- Todos los métodos públicos deben tener docstrings
- README.md obligatorio en cada repositorio
- Comentarios en código complejo

2. CONTROL DE VERSIONES

2.1 Git Workflow
- Usar GitFlow para manejo de ramas
- Commits descriptivos y atómicos
- Pull requests obligatorios para main

2.2 Revisión de Código
- Al menos 2 revisores para cambios críticos
- Ejecutar tests antes de merge
- Revisar seguridad y performance

3. TESTING

3.1 Cobertura de Tests
- Mínimo 80% de cobertura de código
- Tests unitarios para toda lógica de negocio
- Tests de integración para APIs

3.2 Automatización
- CI/CD pipeline configurado
- Tests automáticos en cada PR
- Deploy automático a staging

4. SEGURIDAD

4.1 Mejores Prácticas
- Nunca hardcodear credenciales
- Usar variables de entorno para configuración
- Validar todas las entradas de usuario

4.2 Dependencias
- Mantener dependencias actualizadas
- Escaneo de vulnerabilidades semanal
- Usar herramientas como Snyk o OWASP

5. DEPLOYMENT

5.1 Ambientes
- Development: Para desarrollo local
- Staging: Para testing de QA
- Production: Ambiente productivo

5.2 Proceso de Deploy
- Deploy solo desde rama main
- Backup antes de cada deploy a producción
- Rollback plan siempre disponible
```

**CRÍTICO**: La función create_sample_documents() debe generar EXACTAMENTE estos 2 archivos con el contenido textual idéntico mostrado arriba. 

**VALIDACIÓN DE RESPUESTAS ESPERADAS:**
- "empleados nuevos vacaciones" → debe contener "15 días al año"
- "trabajo remoto horarios" → debe contener "7:00 AM y 7:00 PM"
- "Python estándares" → debe contener "PEP 8"
- "cobertura tests" → debe contener "80%"
- "deploy producción" → debe contener "main", "backup", "rollback"

**VALIDACIÓN NEGATIVA (preguntas capciosas):**
- "VisionBox AI" → debe responder "No tengo información" (NO inventar)
- "cliente sector salud" → debe responder "No tengo información" (NO inventar)
- "ventas 2024/2025" → debe responder "No tengo información" (NO inventar)
- "migración nube" → debe responder "No tengo información" (NO inventar)

**Consultas de Prueba Exactas (incluir preguntas críticas para validación):**

**Preguntas Directas (respondibles con documentos):**
1. "¿Cuántos días de vacaciones tienen los empleados nuevos?"
2. "¿Cuál es la política de trabajo remoto de la empresa?"
3. "¿Qué estándares de código se deben seguir para Python?"
4. "¿Cuál es el proceso para hacer deploy a producción?"
5. "¿Qué porcentaje mínimo de cobertura de tests se requiere?"

**Preguntas Capciosas (para validar comportamiento ante datos no disponibles):**
6. "¿Cuál fue el producto más vendido de TechCorp durante el segundo trimestre de 2024 y cuál fue su participación en el total de ventas de ese trimestre?"
7. "¿Cuál fue el ahorro mensual aproximado en infraestructura tras la migración parcial a la nube durante 2025?"
8. "¿Qué cliente del sector salud adquirió VisionBox AI y en qué año lo hizo?"
9. "¿Cuál fue el porcentaje de reducción del inventario ocioso tras la optimización de la cadena de suministro en 2025?"
10. "¿Qué solución se relanç en 2025 con una nueva versión que integra inteligencia artificial?"

=== A - ARTEFACTOS ===
Genera exactamente estos archivos:

**1. RETO_RAG.py** (Script principal)
- Clases: DocumentProcessor (con carga automática desde sample_docs/), TextChunker (1200 chars, overlap 200), RAGSystem (MMR search, k=7, lambda_mult=0.5, fetch_k=20)
- Función create_sample_documents() que genere los 2 documentos exactos en directorio sample_docs/ (manual_politicas.txt y guia_desarrollo.txt)
- Auto-detección y carga de todos los archivos .txt y .pdf del directorio
- Pipeline completo con retrieval optimizado (MMR para diversidad semántica)
- Ejecución automática de las 10 consultas (5 directas + 5 capciosas)
- Modificación del prompt con "--- Responde concretamente, sin tanto choro"
- Validación de entidades, fechas, porcentajes y relaciones
- Guardado en rag_results.json con estructura: {"question": str, "answer": str, "timestamp": str, "sources": list, "num_sources": int}
- Main function que ejecute todo el pipeline automáticamente
- Inspección de chunks para búsqueda de patrones específicos
- Batch processing con pausas para rate limits

**2. RETO_RAG.ipynb** (Notebook educativo)
- 6 secciones: Setup, Extracción (carga automática), Chunking (optimizado 1200/200), Embeddings, VectorStore, RAG (MMR retrieval k=7)
- Demostración de carga automática desde sample_docs/
- Análisis de calidad de chunks con nuevo tamaño
- Comparación entre búsqueda similarity vs MMR
- Validación con preguntas críticas y capciosas
- Outputs visuales de estadísticas de retrieval
- Sección interactiva para consultas personalizadas

**3. requirements.txt**
- openai>=1.0.0
- langchain>=0.1.0
- langchain-openai>=0.1.0
- langchain-chroma>=0.1.0
- langchain-community>=0.1.0
- chromadb>=0.4.0
- pypdf>=3.0.0
- python-dotenv>=1.0.0
- tqdm>=4.65.0
- pytest>=7.0.0

**4. .github/workflows/rag-ci.yml** (CI/CD)
- Trigger: push a main, PR, workflow_dispatch
- Jobs: test-rag-system, security-scan, performance-test
- Secrets: OPENAI_API_KEY
- Validación de archivos generados (rag_results.json, chroma_db/)
- Upload artifacts

**5. test_rag.py** (Testing completo)
- TestRAGSystem con unittest
- Tests: document_loading (incluyendo carga automática), text_chunking (1200 chars), vectorstore_creation, retrieval_system (MMR k=7), qa_chain, multiple_queries (10 preguntas: 5 directas + 5 capciosas)
- **Test de coherencia de respuestas**: Validar que las respuestas a preguntas directas contengan información exacta de los documentos (ej: "15 días" para empleados nuevos, "80%" para cobertura, "PEP 8" para Python)
- **Test de preguntas capciosas**: Verificar que el sistema responda "No tengo información" o similar para preguntas sobre VisionBox AI, clientes de salud, datos de 2024/2025
- Performance tests
- Integration tests con validación crítica
- setup/teardown apropiados

**6. README.md** (Documentación completa)
- Descripción del proyecto con optimizaciones
- Arquitectura del sistema (diagrama textual actualizado)
- Instalación paso a paso
- Uso del sistema (carga automática, MMR, chunks optimizados)
- Configuración CI/CD
- Resultados esperados con métricas optimizadas
- Respuestas del cuestionario académico

**7. .env.template**
- OPENAI_API_KEY=sk-your-key-here
- Configuraciones opcionales comentadas (chunk_size, retrieval_k, search_type)

**8. .gitignore**
- .env, chroma_db/, sample_docs/, rag_results.json
- Python estándar (__pycache__, *.pyc, venv/)

**9. Makefile**
- Targets: install, setup, test, run, clean, check-env
- Comandos automatizados para desarrollo

=== T - TESTING ===
**Testing Strategy:**
- Tests unitarios: cada componente por separado (incluyendo carga automática)
- Tests de integración: pipeline completo con MMR retrieval
- Tests de calidad: validación con preguntas críticas y capciosas
- **Tests de coherencia textual**: Verificar que las respuestas contengan datos exactos de los documentos base
- **Tests de validación negativa**: Confirmar que preguntas capciosas NO generen información inventada
- Tests de rendimiento: < 5 minutos ejecución total
- Validación de resultados: JSON bien formado, respuestas coherentes con entidades correctas
- CI/CD tests: ejecución automática en GitHub Actions

**Métricas de Validación:**
- ✅ 10/10 consultas respondan correctamente (5 directas + 5 capciosas para validar comportamiento)
- ✅ **Coherencia textual**: Respuestas directas deben contener datos exactos ("15 días", "80%", "PEP 8", "7:00 AM y 7:00 PM", "2+ años: 20 días")
- ✅ **Validación negativa**: Preguntas capciosas deben generar "No tengo información" o similar (NO inventar datos sobre VisionBox AI, clientes, ventas 2024/2025)
- ✅ Carga automática de documentos desde sample_docs/ funcione
- ✅ Retrieval MMR genere respuestas más diversas y completas
- ✅ Base de datos vectorial se cree exitosamente con chunks optimizados
- ✅ Archivos de resultado se generen con validación de entidades
- ✅ No errores en ejecución completa
- ✅ Tests pasen con >80% éxito incluyendo validación crítica
- ✅ CI/CD se ejecute sin fallos

**Error Handling:**
- Rate limits de OpenAI con reintentos
- Archivos faltantes o corruptos en sample_docs/
- API key inválida o ausente
- Fallos de red en embeddings
- Memoria insuficiente para vectorstore
- Errores en carga automática de archivos

=== E - EXTRAS ===
**Funcionalidades Avanzadas:**
- Carga automática y detección de archivos en sample_docs/
- Batch processing para optimizar rate limits
- Metadata enriquecida en documentos con tipos de archivo
- Scores de relevancia en respuestas con MMR
- Validación de entidades (fechas, porcentajes, números específicos)
- Logging estructurado de operaciones de carga y retrieval
- Cache de embeddings para desarrollo
- Métricas de diversidad semántica en respuestas

**Optimizaciones:**
- Chunking optimizado (1200 chars) para mejor continuidad contextual
- Búsqueda MMR para mayor diversidad semántica vs similarity simple
- Auto-detección de tipos de documento y carga inteligente
- Filtros por metadata de documentos y tipos
- Persistencia de configuraciones de retrieval
- Resumenes ejecutivos con validación de datos críticos

**Documentación Adicional:**
- Diagramas de arquitectura en ASCII actualizados
- Ejemplos de uso avanzado con optimizaciones
- Troubleshooting guide para carga automática
- Performance benchmarks comparativos
- Roadmap de mejoras futuras

**Consideraciones de Producción:**
- Secrets management seguro
- Monitoreo de costos API optimizado
- Backup de base de datos vectorial
- Escalabilidad horizontal con carga automática
- Multi-tenancy support

IMPORTANTE: 
1. PRIMERO presenta el PLAN DETALLADO paso a paso
2. DESPUÉS implementa cada archivo exactamente como se especifica
3. USA langchain_community.document_loaders (NO langchain.document_loaders)
4. IMPLEMENTA carga automática de documentos desde sample_docs/ (no rutas hardcodeadas)
5. CONFIGURA retrieval con MMR (search_type="mmr"), k=7, lambda_mult=0.5 y fetch_k=20 para mayor diversidad
6. OPTIMIZA chunking a 1200 caracteres con overlap 200 para mejor contexto
7. INCLUYE las 10 preguntas exactas (5 directas + 5 capciosas) para validación completa
8. INCLUYE manejo robusto de errores en todo el código (rate limits, archivos faltantes, API key inválida)
9. GENERA contenido auto-ejecutable sin intervención manual (directorio sample_docs/, documentos, configuración)
10. IMPLEMENTA la modificación del prompt con "--- Responde concretamente, sin tanto choro"
11. DOCUMENTA cada decisión técnica importante y las mejoras implementadas
12. ASEGURAR que las preguntas capciosas busquen información NO disponible en los documentos generados
13. IMPLEMENTA tests que verifiquen respuestas exactas ("15 días", "80%", "PEP 8") vs documentos base
14. IMPLEMENTA tests que validen que preguntas capciosas NO generen información inventada

**MEJORAS TÉCNICAS ESPECÍFICAS IMPLEMENTADAS:**
1. **Carga automática mejorada**: Se implementó un método para cargar todos los archivos .txt y .pdf desde un directorio (sample_docs), eliminando la necesidad de especificar rutas manualmente.
2. **Optimización del chunking**: Se ajustó el tamaño de fragmento a 1200 caracteres con un solapamiento de 200, lo que mejora la continuidad del contexto entre secciones clave.
3. **Mejora del recuperador**: Se configuró el sistema para recuperar 7 chunks (k=7) con búsqueda "mmr" (Maximal Marginal Relevance), lambda_mult=0.5 y fetch_k=20, permitiendo mayor diversidad semántica y mejor cobertura de respuestas complejas.
4. **Validación con preguntas capciosas**: Se ejecutaron pruebas con 10 preguntas (5 directas + 5 capciosas) para asegurar que el sistema no invente información no disponible en los documentos.
5. **Modificación del prompt**: Se agregó "--- Responde concretamente, sin tanto choro" al final de cada consulta para obtener respuestas más directas.
```