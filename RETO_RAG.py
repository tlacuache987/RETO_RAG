#!/usr/bin/env python3
"""
Sistema RAG (Retrieval-Augmented Generation) Completo
Implementación para el reto del Certificado en Desarrollo de Software con IA Generativa

Este sistema permite:
1. Extraer texto de archivos PDF y TXT
2. Dividir texto en fragmentos (chunking)
3. Crear embeddings vectoriales
4. Almacenar en base de datos vectorial (ChromaDB)
5. Recuperar información relevante
6. Generar respuestas contextualizadas
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import json
import time

# Librerías principales
try:
    from dotenv import load_dotenv
    import openai
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_chroma import Chroma
    from langchain.schema import Document
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.chains import RetrievalQA
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    import chromadb
    from tqdm import tqdm
except ImportError as e:
    print(f"Error importando librerías: {e}")
    print("Instala las dependencias con:")
    print("pip install openai langchain langchain-openai langchain-chroma chromadb pypdf python-dotenv tqdm")
    sys.exit(1)

class DocumentProcessor:
    """Procesador de documentos para extraer y limpiar texto"""

    @staticmethod
    def load_documents_from_directory(directory_path: str) -> List[Document]:
        """
        Carga documentos desde todos los archivos PDF y TXT en un directorio

        Args:
            directory_path: Ruta al directorio que contiene los archivos

        Returns:
            Lista de documentos procesados
        """
        documents = []
        dir_path = Path(directory_path)
        # Buscar todos los .txt y .pdf en el directorio
        file_paths = list(dir_path.glob("*.txt")) + list(dir_path.glob("*.pdf"))

        for file_path in file_paths:
            file_path_str = str(file_path)
            try:
                if file_path_str.endswith('.pdf'):
                    loader = PyPDFLoader(file_path_str)
                    docs = loader.load()
                    print(f"✅ Cargado PDF: {file_path_str} ({len(docs)} páginas)")

                elif file_path_str.endswith('.txt'):
                    loader = TextLoader(file_path_str, encoding='utf-8')
                    docs = loader.load()
                    print(f"✅ Cargado TXT: {file_path_str}")

                else:
                    print(f"❌ Formato no soportado: {file_path_str}")
                    continue

                # Agregar metadatos adicionales
                for doc in docs:
                    doc.metadata['source_file'] = os.path.basename(file_path_str)
                    doc.metadata['file_type'] = file_path_str.split('.')[-1]

                documents.extend(docs)

            except Exception as e:
                print(f"❌ Error cargando {file_path_str}: {e}")

        return documents

class TextChunker:
    """Divisor de texto en fragmentos manejables"""

    def __init__(self, chunk_size: int = 1200, chunk_overlap: int = 200):
        """
        Inicializa el divisor de texto

        Args:
            chunk_size: Tamaño máximo de cada fragmento
            chunk_overlap: Solapamiento entre fragmentos
        """
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Divide documentos en fragmentos

        Args:
            documents: Lista de documentos a dividir

        Returns:
            Lista de fragmentos de documentos
        """
        chunks = self.splitter.split_documents(documents)

        # Agregar metadatos de fragmento
        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_id'] = i
            chunk.metadata['chunk_size'] = len(chunk.page_content)

        print(f"📄 Documentos divididos en {len(chunks)} fragmentos")
        return chunks

class RAGSystem:
    """Sistema RAG completo"""

    def __init__(self, openai_api_key: str = None, persist_directory: str = "./chroma_db"):
        """
        Inicializa el sistema RAG

        Args:
            openai_api_key: Clave API de OpenAI
            persist_directory: Directorio para persistir la base de datos vectorial
        """
        # Configurar OpenAI
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        elif not os.getenv("OPENAI_API_KEY"):
            raise ValueError("Se requiere OPENAI_API_KEY")

        # Inicializar componentes
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=2000
        )

        self.persist_directory = persist_directory
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None

        # Inicializar procesadores
        self.doc_processor = DocumentProcessor()
        self.text_chunker = TextChunker()

    def build_vectorstore(self, documents: List[Document]):
        """
        Construye la base de datos vectorial

        Args:
            documents: Lista de documentos a indexar
        """
        print("🔧 Construyendo base de datos vectorial...")

        # Crear o cargar vectorstore
        self.vectorstore = Chroma(
            collection_name="rag_documents",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

        # Agregar documentos en lotes para evitar rate limits
        batch_size = 100

        for i in tqdm(range(0, len(documents), batch_size), desc="Indexando documentos"):
            batch = documents[i:i + batch_size]
            try:
                self.vectorstore.add_documents(batch)
                time.sleep(1)  # Pausa para evitar rate limits
            except Exception as e:
                print(f"❌ Error en lote {i//batch_size + 1}: {e}")
                time.sleep(5)  # Pausa más larga en caso de error

        print(f"✅ Base de datos vectorial creada con {len(documents)} documentos")

    def setup_retriever(self, k: int = 5, search_type: str = "similarity"):
        """
        Configura el recuperador de documentos

        Args:
            k: Número de documentos a recuperar
            search_type: Tipo de búsqueda ("similarity" o "mmr")
        """
        if not self.vectorstore:
            raise ValueError("Primero debe construir la base de datos vectorial")

        self.retriever = self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k, "fetch_k": 20,"lambda_mult": 0.5}
        )

        print(f"🔍 Recuperador configurado: {search_type}, k={k}")

    def setup_qa_chain(self):
        """Configura la cadena de pregunta-respuesta"""
        if not self.retriever:
            raise ValueError("Primero debe configurar el recuperador")

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            verbose=False
        )

        print("🤖 Cadena de QA configurada")

    def query(self, question: str, return_sources: bool = True) -> Dict[str, Any]:
        """
        Procesa una consulta y genera respuesta

        Args:
            question: Pregunta del usuario
            return_sources: Si incluir documentos fuente

        Returns:
            Diccionario con respuesta y metadatos
        """
        if not self.qa_chain:
            raise ValueError("Sistema no inicializado completamente")

        print(f"❓ Procesando consulta: {question}")

        try:
            result = self.qa_chain.invoke({"query": question + " --- Responde concretamente, sin tanto choro"})

            response = {
                "question": question,
                "answer": result["result"],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            if return_sources and "source_documents" in result:
                sources = []
                for i, doc in enumerate(result["source_documents"]):
                    source_info = {
                        "document_id": i + 1,
                        "source_file": doc.metadata.get("source_file", "Unknown"),
                        "chunk_id": doc.metadata.get("chunk_id", "Unknown"),
                        "content_preview": doc.page_content[:200] + "..."
                    }
                    sources.append(source_info)

                response["sources"] = sources
                response["num_sources"] = len(sources)

            return response

        except Exception as e:
            return {
                "question": question,
                "answer": f"Error procesando consulta: {e}",
                "error": True,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

    def search_similar_documents(self, query: str, k: int = 3) -> List[Dict]:
        """
        Busca documentos similares sin generar respuesta

        Args:
            query: Consulta de búsqueda
            k: Número de documentos a retornar

        Returns:
            Lista de documentos similares
        """
        if not self.vectorstore:
            raise ValueError("Base de datos vectorial no inicializada")

        docs = self.vectorstore.similarity_search_with_score(query, k=k)

        results = []
        for doc, score in docs:
            result = {
                "content": doc.page_content,
                "similarity_score": float(score),
                "metadata": doc.metadata
            }
            results.append(result)

        return results

def create_sample_documents():
    """Crea documentos de ejemplo si no existen archivos"""
    sample_dir = Path("sample_docs")
    sample_dir.mkdir(exist_ok=True)

    # Documento 1: Manual de políticas de empresa
    doc1_content = """
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
    """

    # Documento 2: Guía técnica de desarrollo
    doc2_content = """
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
    """

    # Guardar documentos
    with open(sample_dir / "manual_politicas.txt", "w", encoding="utf-8") as f:
        f.write(doc1_content)

    with open(sample_dir / "guia_desarrollo.txt", "w", encoding="utf-8") as f:
        f.write(doc2_content)

    return [str(sample_dir / "manual_politicas.txt"), str(sample_dir / "guia_desarrollo.txt")]

def main():
    """Función principal para demostrar el sistema RAG"""
    print("🚀 Iniciando Sistema RAG")
    print("=" * 50)

    # Cargar variables de entorno
    load_dotenv()

    # Verificar API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No se encontró OPENAI_API_KEY")
        print("Por favor configura tu API key en el archivo .env")
        return

    try:
        # Inicializar sistema RAG
        rag_system = RAGSystem()

        # Crear documentos de ejemplo si es necesario
        sample_files = create_sample_documents()
        print(f"📁 Documentos de ejemplo creados: {sample_files}")

        # 1. EXTRACCIÓN DE ARCHIVOS
        print("\n📖 Paso 1: Extrayendo texto de archivos...")
        # Usar el nuevo método para cargar todos los .txt y .pdf del directorio sample_docs
        documents = rag_system.doc_processor.load_documents_from_directory("sample_docs")

        if not documents:
            print("❌ No se pudieron cargar documentos")
            return

        # 2. DIVISIÓN EN FRAGMENTOS
        print("\n✂️ Paso 2: Dividiendo texto en fragmentos...")
        chunks = rag_system.text_chunker.split_documents(documents)

        # Inspeccionar chunks que contienen la frase clave
        print("\n🔍 Buscando chunks con 'VisionBox AI' y 'salud'...")

        for i, chunk in enumerate(chunks):
            content = chunk.page_content.lower()
            if "visionbox ai" in content and "salud" in content:
                print(f"\n🧩 Chunk {i} — {chunk.metadata.get('source_file')}")
                print(chunk.page_content)
                print("-" * 80)

        # 3. CREACIÓN DE EMBEDDINGS Y ALMACENAMIENTO
        print("\n🧠 Paso 3: Creando embeddings y almacenando...")
        rag_system.build_vectorstore(chunks)

        # 4. CONFIGURACIÓN DEL SISTEMA DE RECUPERACIÓN
        print("\n🔍 Paso 4: Configurando sistema de recuperación...")
        rag_system.setup_retriever(k=7, search_type="mmr")
        rag_system.setup_qa_chain()

        # 5. PRUEBAS DEL SISTEMA
        print("\n🧪 Paso 5: Probando el sistema RAG...")

        # Lista de preguntas de prueba (sin duplicados ni fuera de contexto, con capciosas incluidas)
        test_questions = [
            # Preguntas directas de los documentos de ejemplo
            "¿Cuántos días de vacaciones tienen los empleados nuevos?",
            "¿Cuál es la política de trabajo remoto de la empresa?",
            "¿Qué estándares de código se deben seguir para Python?",
            "¿Cuál es el proceso para hacer deploy a producción?",
            "¿Qué porcentaje mínimo de cobertura de tests se requiere?",
            # Preguntas capciosas (no respondibles con los documentos de ejemplo)
            "¿Cuál fue el producto más vendido de TechCorp durante el segundo trimestre de 2024 y cuál fue su participación en el total de ventas de ese trimestre?",
            "¿Cuál fue el ahorro mensual aproximado en infraestructura tras la migración parcial a la nube durante 2025?",
            "¿Qué cliente del sector salud adquirió VisionBox AI y en qué año lo hizo?",
            "¿Cuál fue el porcentaje de reducción del inventario ocioso tras la optimización de la cadena de suministro en 2025?",
            "¿Qué solución se relanzó en 2025 con una nueva versión que integra inteligencia artificial?",
            "¿Qué país no logró apertura de oficina regional en la expansión de TechCorp a Centroamérica?",
            "¿Qué porcentaje del total de ventas en Q1 2025 provino del canal de partners?",
            "¿Cuál fue el ciclo promedio de venta en días durante todo el año 2024 y cómo se comparó con el de 2025?",
            "¿Qué proyecto estratégico incluyó la implementación de asistentes conversacionales basados en LLMs y qué porcentaje de tickets logró resolver automáticamente?",
            "¿Cuál fue el cliente del sector agroindustrial que adquirió dos productos de TechCorp en el primer semestre de 2025, y cuáles fueron esos productos?"
        ]

        results = []

        for i, question in enumerate(test_questions, 1):
            print(f"\n--- Consulta {i} ---")
            result = rag_system.query(question)
            results.append(result)

            print(f"❓ Pregunta: {result['question']}")
            print(f"✅ Respuesta: {result['answer']}")

            if 'sources' in result:
                print(f"📚 Fuentes utilizadas: {result['num_sources']}")
                for source in result['sources']:
                    print(f"   - {source['source_file']} (chunk {source['chunk_id']})")

            print("-" * 50)

        # Guardar resultados
        results_file = "rag_results.json"
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Resultados guardados en: {results_file}")

        # Estadísticas finales
        print("\n📊 Estadísticas del Sistema:")
        print(f"   - Documentos procesados: {len(documents)}")
        print(f"   - Fragmentos creados: {len(chunks)}")
        print(f"   - Consultas realizadas: {len(test_questions)}")
        print(f"   - Base de datos: {rag_system.persist_directory}")

        print("\n✅ Sistema RAG ejecutado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error en ejecución: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
