# Sistema RAG (Retrieval-Augmented Generation)

## 🎯 Descripción del Proyecto

Este proyecto implementa un sistema completo de **RAG (Retrieval-Augmented Generation)** que permite a los usuarios consultar documentos internos de manera inteligente. El sistema combina la recuperación de información específica con la generación de respuestas contextualizadas usando modelos de IA generativa.

### ✨ Características Principales

- **Carga automática**: Detección y procesamiento automático de archivos desde sample_docs/
- **Extracción de documentos**: Soporte para archivos PDF y TXT
- Chunking optimizado: División en fragmentos de 1200 caracteres con overlap de 200
- **Embeddings vectoriales**: Usando OpenAI text-embedding-3-small
- **Base de datos vectorial**: Almacenamiento persistente con ChromaDB
- **Recuperación MMR**: Búsqueda con Maximal Marginal Relevance para mayor diversidad
- **Generación contextualizada**: Respuestas inteligentes con GPT-4o-mini
- **Validación crítica**: Preguntas específicas para validar entidades y relaciones
- **CI/CD automatizado**: Validación continua con GitHub Actions

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   sample_docs/  │────│   Carga          │────│   Chunking      │
│   (PDF/TXT)     │    │   Automática     │    │   (1200/200)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                 │
                                 ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Respuesta     │◄───│   LLM GPT-4o     │◄───│   ChromaDB      │
│   + Fuentes     │    │   + MMR Context  │    │   (Vectores)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                 ▲
                                 │
                         ┌──────────────────┐
                         │   Consulta       │
                         │   del Usuario    │
                         └──────────────────┘
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- Cuenta de OpenAI con API key
- Git (para CI/CD)

### Paso 1: Clonar el repositorio

```bash
git clone <tu-repositorio>
cd sistema-rag
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Configurar variables de entorno

```bash
# Copiar template
cp .env.template .env

# Editar .env y agregar tu API key
OPENAI_API_KEY=sk-tu-api-key-aqui
```

### Paso 4: Ejecutar el sistema

```bash
python RETO_RAG.py
```

## 📚 Uso del Sistema

### Ejecución Básica

El sistema incluye documentos de ejemplo y se ejecuta automáticamente:

```python
from RETO_RAG import RAGSystem, create_sample_documents

# Inicializar sistema
rag_system = RAGSystem()

# Cargar documentos
documents = rag_system.doc_processor.load_documents(file_paths)

# Procesar y construir base de datos
chunks = rag_system.text_chunker.split_documents(documents)
rag_system.build_vectorstore(chunks)
rag_system.setup_retriever()
rag_system.setup_qa_chain()

# Hacer consultas
result = rag_system.query("¿Cuál es la política de vacaciones?")
print(result["answer"])
```

### Consultas de Ejemplo

El sistema incluye estas consultas de prueba optimizadas:

**Preguntas directas (respondibles con los documentos):**
1. "¿Cuántos días de vacaciones tienen los empleados nuevos?"
2. "¿Cuál es la política de trabajo remoto de la empresa?"
3. "¿Qué estándares de código se deben seguir para Python?"
4. "¿Cuál es el proceso para hacer deploy a producción?"
5. "¿Qué porcentaje mínimo de cobertura de tests se requiere?"

**Preguntas capciosas (para validar comportamiento ante datos no disponibles):**
6. "¿Cuál fue el producto más vendido de TechCorp durante el segundo trimestre de 2024?"
7. "¿Qué cliente del sector salud adquirió VisionBox AI y en qué año?"
8. "¿Cuál fue el ahorro mensual tras la migración a la nube durante 2025?"

Estas preguntas capciosas validan que el sistema no invente información no disponible en los documentos.

## 🔧 Configuración Avanzada

### Parámetros del Sistema

```python
# Configuración de chunking
text_chunker = TextChunker(
    chunk_size=1200,      # Tamaño de fragmento optimizado
    chunk_overlap=200     # Solapamiento para continuidad
)

# Configuración de recuperación
rag_system.setup_retriever(
    k=7,                  # Número de documentos a recuperar
    search_type="mmr",    # MMR para mayor diversidad
    fetch_k=20,           # Candidatos para MMR
    lambda_mult=0.5       # Balance diversidad vs relevancia
)

# Carga automática de documentos
documents = load_documents_from_directory("sample_docs/")
```

### Modelos y Configuración

- **LLM**: GPT-4o-mini (OpenAI) con temperatura 0
- **Embeddings**: text-embedding-3-small (OpenAI)
- **Vector Store**: ChromaDB con persistencia local
- **Chunking**: 1200 caracteres con overlap 200
- **Retrieval**: MMR (Maximal Marginal Relevance) con k=7
- **Carga**: Automática desde directorio sample_docs/

## 🧪 Testing y CI/CD

### GitHub Actions

El proyecto incluye un workflow completo de CI/CD:

```yaml
# .github/workflows/rag-ci.yml
- Instalación de dependencias
- Ejecución del sistema RAG
- Validación de resultados
- Análisis de seguridad
- Tests de rendimiento
```

### Configurar Secrets en GitHub

1. Ve a Settings → Secrets and variables → Actions
2. Agrega: `OPENAI_API_KEY` con tu API key

### Ejecutar Tests Localmente

```bash
# Test básico
python RETO_RAG.py

# Verificar resultados
cat rag_results.json
```

## 📊 Resultados y Métricas

### Archivos Generados

- `rag_results.json`: Resultados de las consultas
- `chroma_db/`: Base de datos vectorial persistente
- `sample_docs/`: Documentos de ejemplo

### Métricas del Sistema

- **Documentos procesados**: Carga automática desde sample_docs/
- **Fragmentos creados**: ~25-35 chunks optimizados (1200 chars)
- **Tiempo de respuesta**: < 3 segundos por consulta
- **Precisión**: Respuestas basadas en documentos fuente con MMR
- **Diversidad**: Mayor cobertura semántica con retrieval MMR
- **Validación**: 7 consultas incluyendo preguntas críticas

## 🔒 Seguridad y Mejores Prácticas

### Seguridad

- ✅ API keys en variables de entorno
- ✅ No hardcodear credenciales
- ✅ Validación de entradas
- ✅ Scanning automático de seguridad

### Mejores Prácticas

- **Rate limiting**: Pausas entre llamadas a API
- **Error handling**: Manejo robusto de errores
- **Logging**: Información detallada de ejecución
- **Modularidad**: Código organizado en clases
- **Testing**: Validación automatizada

## 🚧 Roadmap y Mejoras Futuras

### Próximas Funcionalidades

- [ ] Soporte para más formatos (DOCX, CSV, Excel)
- [ ] Interface web con Streamlit
- [ ] Búsqueda híbrida (MMR + keyword)
- [ ] Métricas de calidad automatizadas
- [ ] Integración con modelos locales (Ollama)
- [ ] Filtros avanzados por metadata

### Optimizaciones Implementadas

- [x] Chunking optimizado (1200/200) para mejor contexto
- [x] Carga automática de documentos desde directorio
- [x] Búsqueda MMR para mayor diversidad semántica
- [x] Validación con preguntas críticas
- [x] Cache de embeddings para desarrollo
- [x] Respuestas con mayor cobertura contextual

## 📞 Soporte y Contribución

### Problemas Comunes

**Error: "No module named 'chromadb'"**
```bash
pip install --upgrade chromadb
```

**Error: "Invalid API key"**
- Verifica que tu API key sea válida
- Revisa el archivo `.env`

**Error: "Rate limit exceeded"**
- El sistema incluye rate limiting automático
- Espera unos minutos y vuelve a intentar

### Contribuir

1. Fork del repositorio
2. Crear feature branch
3. Hacer commits descriptivos
4. Ejecutar tests
5. Crear Pull Request

## 📄 Licencia

Este proyecto es parte del Certificado en Desarrollo de Software con IA Generativa.

## 🎓 Contexto Académico

### Objetivos de Aprendizaje Cumplidos

- ✅ Implementación de sistema RAG funcional con optimizaciones
- ✅ Uso de embeddings vectoriales con retrieval MMR
- ✅ Integración con modelos de IA generativa optimizada
- ✅ Configuración de CI/CD automatizado
- ✅ Aplicación de prompt engineering avanzado
- ✅ Mejores prácticas de desarrollo con validación crítica
- ✅ Carga automática y chunking optimizado

### Respuestas al Cuestionario

1. **Principal ventaja de RAG**: b) Respuestas más precisas y fundamentadas en datos
2. **Componente de búsqueda**: b) El indexador vectorial
3. **Limitación de IA generativa**: b) Puede inventar información o cometer errores de lógica
4. **Qué es Ollama**: c) Una plataforma para ejecutar modelos generativos localmente
5. **Importancia de revisar código**: b) Para asegurarse de que cumple con los estándares y es seguro

### Reflexión sobre RAG

Los sistemas RAG representan un paradigma transformador para los desarrolladores, permitiendo:

- **Acceso contextualizado**: Información específica sin necesidad de buscar manualmente
- **Conocimiento actualizado**: Respuestas basadas en documentación actual
- **Democratización del conocimiento**: Acceso fácil para todos los miembros del equipo
- **Eficiencia mejorada**: Reducción del tiempo de búsqueda de información

**Ejemplo práctico**: Un desarrollador puede preguntar "¿Cómo configurar el deploy para el microservicio de pagos?" y obtener una respuesta específica basada en la documentación interna, en lugar de revisar múltiples archivos manualmente.

---

**Desarrollado por**: [Tu Nombre]  
**Fecha**: Septiembre 2025  
**Versión**: 1.0.0