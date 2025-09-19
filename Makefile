# Makefile para Sistema RAG
# Automatiza instalación, testing y ejecución

.PHONY: help install setup test run clean lint format check-env

# Variables
PYTHON := python3
PIP := pip3
VENV := venv
REQUIREMENTS := requirements.txt

# Colores para output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Mostrar ayuda
	@echo "$(GREEN)Sistema RAG - Comandos disponibles:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Instalar dependencias
	@echo "$(GREEN)Instalando dependencias...$(NC)"
	$(PIP) install -r $(REQUIREMENTS)
	@echo "$(GREEN)✅ Dependencias instaladas$(NC)"

setup: install ## Configuración completa del proyecto
	@echo "$(GREEN)Configurando proyecto...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)Creando archivo .env desde template...$(NC)"; \
		cp .env.template .env; \
		echo "$(RED)⚠️  Edita .env y agrega tu OPENAI_API_KEY$(NC)"; \
	fi
	@echo "$(GREEN)✅ Proyecto configurado$(NC)"

check-env: ## Verificar configuración de entorno
	@echo "$(GREEN)Verificando configuración...$(NC)"
	@$(PYTHON) -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ API Key:', 'Configurada' if os.getenv('OPENAI_API_KEY') else '❌ NO CONFIGURADA')"
	@$(PYTHON) -c "import openai, langchain, chromadb; print('✅ Dependencias: OK')" || echo "$(RED)❌ Faltan dependencias$(NC)"

test: check-env ## Ejecutar tests completos
	@echo "$(GREEN)Ejecutando tests...$(NC)"
	$(PYTHON) test_rag.py

test-quick: ## Ejecutar tests rápidos (solo unitarios)
	@echo "$(GREEN)Ejecutando tests unitarios...$(NC)"
	$(PYTHON) -m unittest test_rag.TestRAGSystem -v

run: check-env ## Ejecutar sistema RAG completo
	@echo "$(GREEN)Ejecutando sistema RAG...$(NC)"
	$(PYTHON) RETO_RAG.py

run-notebook: ## Ejecutar notebook (requiere Jupyter)
	@echo "$(GREEN)Iniciando Jupyter Notebook...$(NC)"
	jupyter notebook RETO_RAG.ipynb

lint: ## Verificar calidad del código
	@echo "$(GREEN)Verificando código con flake8...$(NC)"
	@$(PIP) list | grep flake8 > /dev/null || $(PIP) install flake8
	flake8 --max-line-length=100 --ignore=E501,W503 *.py

format: ## Formatear código con black
	@echo "$(GREEN)Formateando código...$(NC)"
	@$(PIP) list | grep black > /dev/null || $(PIP) install black
	black --line-length=100 *.py

clean: ## Limpiar archivos temporales
	@echo "$(GREEN)Limpiando archivos temporales...$(NC)"
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf *.egg-info/
	rm -f *.pyc
	rm -f *.pyo
	rm -f .coverage
	rm -rf htmlcov/
	rm -f rag_results.json
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

clean-all: clean ## Limpiar todo (incluyendo datos)
	@echo "$(YELLOW)⚠️  Eliminando datos del sistema...$(NC)"
	rm -rf chroma_db/
	rm -rf sample_docs/
	@echo "$(GREEN)✅ Limpieza completa$(NC)"

venv: ## Crear entorno virtual
	@echo "$(GREEN)Creando entorno virtual...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)✅ Entorno virtual creado$(NC)"
	@echo "$(YELLOW)Activa con: source $(VENV)/bin/activate$(NC)"

requirements: ## Actualizar requirements.txt
	@echo "$(GREEN)Actualizando requirements.txt...$(NC)"
	$(PIP) freeze > $(REQUIREMENTS)
	@echo "$(GREEN)✅ Requirements actualizados$(NC)"

docs: ## Generar documentación
	@echo "$(GREEN)Generando documentación...$(NC)"
	@echo "📚 README.md ya disponible"
	@echo "📓 Notebook documentado disponible"
	@echo "🔧 Makefile con comandos disponible"

demo: setup run ## Demo completo (setup + ejecución)

ci: lint test ## Simulación de CI (lint + test)
	@echo "$(GREEN)✅ CI checks passed$(NC)"

status: ## Mostrar estado del proyecto
	@echo "$(GREEN)Estado del Sistema RAG:$(NC)"
	@echo "📁 Archivos principales:"
	@ls -la *.py 2>/dev/null || echo "  ❌ Archivos Python no encontrados"
	@ls -la *.ipynb 2>/dev/null || echo "  ❌ Notebook no encontrado"
	@ls -la requirements.txt 2>/dev/null || echo "  ❌ Requirements no encontrado"
	@echo ""
	@echo "🗄️ Datos:"
	@ls -d chroma_db/ 2>/dev/null && echo "  ✅ Base de datos vectorial existe" || echo "  ❌ Base de datos no existe"
	@ls -d sample_docs/ 2>/dev/null && echo "  ✅ Documentos de ejemplo existen" || echo "  ❌ Documentos no existen"
	@ls rag_results.json 2>/dev/null && echo "  ✅ Resultados disponibles" || echo "  ❌ No hay resultados"
	@echo ""
	@echo "🔧 Configuración:"
	@test -f .env && echo "  ✅ Archivo .env existe" || echo "  ❌ Archivo .env no existe"

# Targets especiales para desarrollo
dev-setup: venv ## Setup completo para desarrollo
	@echo "$(GREEN)Setup de desarrollo...$(NC)"
	@source $(VENV)/bin/activate && make install
	@source $(VENV)/bin/activate && $(PIP) install jupyter black flake8 pytest
	@echo "$(GREEN)✅ Entorno de desarrollo listo$(NC)"

quick-test: ## Test rápido para desarrollo
	@$(PYTHON) -c "from RETO_RAG import create_sample_documents; print('✅ Import OK')"
	@$(PYTHON) -c "import openai, langchain, chromadb; print('✅ Dependencies OK')"

# Default target
all: setup test run