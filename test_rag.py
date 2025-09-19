#!/usr/bin/env python3
"""
Script de Testing para el Sistema RAG
Valida el funcionamiento completo del sistema y genera métricas
"""

import os
import sys
import json
import time
import unittest
from pathlib import Path

# Importar el sistema RAG
try:
    from RETO_RAG import RAGSystem, create_sample_documents
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Error importando dependencias: {e}")
    print("Ejecuta: pip install -r requirements.txt")
    sys.exit(1)


class TestRAGSystem(unittest.TestCase):
    """Tests unitarios para el sistema RAG"""

    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todos los tests"""
        load_dotenv()

        # Verificar API key
        cls.api_key = os.getenv("OPENAI_API_KEY")
        if not cls.api_key:
            raise ValueError("OPENAI_API_KEY no encontrada")

        # Crear documentos de ejemplo
        create_sample_documents()

        # Inicializar sistema RAG
        cls.rag_system = RAGSystem()

    def test_01_document_loading(self):
        """Test: Carga de documentos"""
        print("\n🧪 Test 1: Carga de documentos")

        documents = self.rag_system.doc_processor.load_documents_from_directory("sample_docs")

        self.assertGreater(len(documents), 0, "No se cargaron documentos")
        self.assertTrue(all(doc.page_content for doc in documents), "Documentos vacíos")

        print(f"✅ Cargados {len(documents)} documentos")

    def test_02_text_chunking(self):
        """Test: División en fragmentos"""
        print("\n🧪 Test 2: División en fragmentos")

        documents = self.rag_system.doc_processor.load_documents_from_directory("sample_docs")
        chunks = self.rag_system.text_chunker.split_documents(documents)

        self.assertGreater(len(chunks), len(documents), "No se dividieron los documentos")
        self.assertTrue(all(chunk.page_content for chunk in chunks), "Fragmentos vacíos")

        print(f"✅ Creados {len(chunks)} fragmentos desde {len(documents)} documentos")

    def test_03_vectorstore_creation(self):
        """Test: Creación de base de datos vectorial"""
        print("\n🧪 Test 3: Base de datos vectorial")

        documents = self.rag_system.doc_processor.load_documents_from_directory("sample_docs")
        chunks = self.rag_system.text_chunker.split_documents(documents)

        # Usar solo algunos fragmentos para el test (más rápido)
        test_chunks = chunks[:5]
        self.rag_system.build_vectorstore(test_chunks)

        self.assertIsNotNone(self.rag_system.vectorstore, "Vectorstore no inicializado")

        # Verificar que se pueden hacer búsquedas
        results = self.rag_system.vectorstore.similarity_search("vacaciones", k=1)
        self.assertGreater(len(results), 0, "No se encontraron resultados")

        print(f"✅ Base de datos vectorial creada con {len(test_chunks)} fragmentos")

    def test_04_retrieval_system(self):
        """Test: Sistema de recuperación"""
        print("\n🧪 Test 4: Sistema de recuperación")

        # Usar el vectorstore del test anterior
        if not hasattr(self.rag_system, 'vectorstore') or self.rag_system.vectorstore is None:
            self.test_03_vectorstore_creation()

        self.rag_system.setup_retriever(k=3)
        self.assertIsNotNone(self.rag_system.retriever, "Retriever no configurado")

        # Test de búsqueda
        docs = self.rag_system.retriever.get_relevant_documents("políticas de empresa")
        self.assertGreater(len(docs), 0, "No se recuperaron documentos")

        print(f"✅ Recuperador funcionando - encontró {len(docs)} documentos")

    def test_05_qa_chain(self):
        """Test: Cadena de pregunta-respuesta"""
        print("\n🧪 Test 5: Cadena QA completa")

        # Asegurar que el sistema esté completamente configurado
        if not hasattr(self.rag_system, 'retriever') or self.rag_system.retriever is None:
            self.test_04_retrieval_system()

        self.rag_system.setup_qa_chain()
        self.assertIsNotNone(self.rag_system.qa_chain, "Cadena QA no configurada")

        # Test de consulta simple
        test_question = "¿Cuántos días de vacaciones tienen los empleados nuevos?"
        result = self.rag_system.query(test_question)

        self.assertIn("question", result, "Respuesta mal formateada")
        self.assertIn("answer", result, "Sin respuesta")
        self.assertNotIn("error", result, f"Error en consulta: {result.get('answer', '')}")

        print(f"✅ Consulta exitosa: {result['answer'][:100]}...")

    def test_06_multiple_queries(self):
        """Test: Múltiples consultas"""
        print("\n🧪 Test 6: Múltiples consultas")

        if not hasattr(self.rag_system, 'qa_chain') or self.rag_system.qa_chain is None:
            self.test_05_qa_chain()

        test_questions = [
            "¿Cuál es la política de trabajo remoto?",
            "¿Qué estándares de código se usan?",
            "¿Cuántos días de vacaciones hay?"
        ]

        successful_queries = 0

        for question in test_questions:
            result = self.rag_system.query(question)
            if "error" not in result:
                successful_queries += 1
            time.sleep(1)  # Evitar rate limits

        success_rate = successful_queries / len(test_questions)
        self.assertGreaterEqual(success_rate, 0.7, f"Tasa de éxito muy baja: {success_rate:.2%}")

        print(f"✅ {successful_queries}/{len(test_questions)} consultas exitosas ({success_rate:.1%})")


def run_performance_test():
    """Ejecuta test de rendimiento del sistema"""
    print("\n⚡ Test de Rendimiento")
    print("=" * 50)

    load_dotenv()

    start_time = time.time()

    try:
        # Inicializar sistema
        rag_system = RAGSystem()
        create_sample_documents()

        # Procesar documentos
        documents = rag_system.doc_processor.load_documents_from_directory("sample_docs")
        chunks = rag_system.text_chunker.split_documents(documents)

        # Construir vectorstore (muestra pequeña para velocidad)
        test_chunks = chunks[:10]
        rag_system.build_vectorstore(test_chunks)
        rag_system.setup_retriever()
        rag_system.setup_qa_chain()

        # Test de consulta
        result = rag_system.query("¿Cuántos días de vacaciones hay?")

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"⏱️ Tiempo total de ejecución: {execution_time:.2f} segundos")
        print(f"📄 Documentos procesados: {len(documents)}")
        print(f"✂️ Fragmentos creados: {len(chunks)}")
        print(f"🗄️ Fragmentos indexados: {len(test_chunks)}")

        if "error" not in result:
            print(f"✅ Consulta exitosa")
        else:
            print(f"❌ Error en consulta: {result['answer']}")

        # Evaluación de rendimiento
        if execution_time < 60:
            print("🚀 Rendimiento: EXCELENTE")
        elif execution_time < 120:
            print("👍 Rendimiento: BUENO")
        else:
            print("⚠️ Rendimiento: MEJORABLE")

    except Exception as e:
        print(f"❌ Error en test de rendimiento: {e}")


def run_integration_test():
    """Ejecuta test de integración completo"""
    print("\n🔗 Test de Integración Completo")
    print("=" * 50)

    load_dotenv()

    try:
        # Simular el flujo completo del notebook
        from RETO_RAG import main

        print("Ejecutando flujo principal...")
        main()

        # Verificar archivos generados
        if Path("rag_results.json").exists():
            print("✅ Archivo de resultados generado")

            with open("rag_results.json", "r", encoding="utf-8") as f:
                results = json.load(f)

            successful = len([r for r in results if "error" not in r])
            total = len(results)

            print(f"📊 Resultados: {successful}/{total} consultas exitosas")

        if Path("chroma_db").exists():
            print("✅ Base de datos vectorial creada")
        else:
            print("❌ Base de datos vectorial no encontrada")

        if Path("sample_docs").exists():
            print("✅ Documentos de ejemplo creados")
        else:
            print("❌ Documentos de ejemplo no encontrados")

    except Exception as e:
        print(f"❌ Error en test de integración: {e}")


if __name__ == "__main__":
    print("🧪 Sistema de Testing para RAG")
    print("=" * 50)

    # Verificar configuración
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY no configurada")
        print("Configura tu API key en el archivo .env")
        sys.exit(1)

    # Ejecutar tests unitarios
    print("\n🔬 Ejecutando Tests Unitarios")
    unittest.main(argv=[''], exit=False, verbosity=2)

    # Ejecutar test de rendimiento
    run_performance_test()

    # Ejecutar test de integración
    run_integration_test()

    print("\n✅ Todos los tests completados!")