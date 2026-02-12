# 🏦 AI Financial Compliance Agent (RAG) 🤖

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Latest-1C3C3C?style=flat&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/Model-GPT--4o-412991?style=flat&logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production_Ready-success)

> **Automatización inteligente para el análisis de riesgo crediticio y cumplimiento normativo (AML/KYC).**

Este repositorio contiene la implementación de un **Agente Autónomo** capaz de interpretar manuales bancarios no estructurados (PDF), extraer reglas de negocio complejas (tablas de tasas, excepciones) y ejecutar validaciones de seguridad financiera.

---

## 🚀 Acceso Rápido (Demo)

Este proyecto está diseñado para ejecutarse en la nube. Haz clic en el botón de abajo para interactuar con el agente en un entorno aislado.

| Notebook | Visualizar en Colab (Recomendado) | Descripción |
| :--- | :--- | :--- |
| **1. Agente** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BGIA1/ai-financial-agent-rag/blob/main/notebooks/AI_Credit_Compliance_Agent_DummyBank.ipynb) | Pipeline completo: Ingesta, RAG híbrido y Lógica de Agente. |

> **Nota:** Se requiere una API Key de OpenAI para ejecutar las celdas de inferencia.

---

## 📋 Descripción del Proyecto

El análisis de manuales normativos en la banca suele ser un proceso manual, lento y propenso a errores humanos. Este proyecto automatiza dicha tarea utilizando una arquitectura **RAG (Retrieval-Augmented Generation)** avanzada.

A diferencia de un chatbot estándar, este sistema implementa un **Agente con uso de herramientas (Tool Calling)**, lo que le permite "razonar" cuándo consultar el documento y cuándo aplicar lógica deductiva, reduciendo las alucinaciones a cero.

## 🛠️ Tecnologías Clave

* **Orquestación:** LangChain (Implementación de *OpenAI Tools Agent*).
* **LLM:** GPT-4o (Configurado con `temperature=0` para determinismo financiero).
* **Base Vectorial:** ChromaDB (Persistencia local).
* **Embeddings:** Hugging Face (`all-MiniLM-L6-v2`) para eficiencia y privacidad.
* **Ingeniería de Datos:** `RecursiveCharacterTextSplitter` optimizado para tablas financieras.

---

## ⚙️ Metodología y Arquitectura

El flujo de trabajo se divide en 4 etapas críticas para asegurar la precisión bancaria:

1.  **Ingesta de Alta Precisión:**
    * Se implementó un filtro de caracteres (`len > 10`) para evitar la pérdida de celdas pequeñas en tablas numéricas (ej. "18.2%").
2.  **Búsqueda Híbrida (MMR):**
    * Se sustituyó la búsqueda por similitud simple por **MMR (Maximal Marginal Relevance)**. Esto permite recuperar contextos diversos simultáneamente (ej. reglas de lavado de dinero en la pág. 4 y tasas de interés en la pág. 1) sin saturar la ventana de contexto.
3.  **Razonamiento del Agente:**
    * El agente evalúa condiciones lógicas complejas, como la aprobación de excepciones basada en antigüedad vs. score.
4.  **Safety & Guardrails:**
    * Implementación de *Negative Testing*: El agente está programado para rechazar solicitudes de productos fuera de su dominio (ej. Hipotecas) explícitamente.


---

## 📊 Casos de Prueba (Unit Tests)

El sistema ha superado las siguientes pruebas de validación lógica:

| Caso de Prueba | Input del Usuario | Resultado del Agente | Estado |
| :--- | :--- | :--- | :--- |
| **Extracción Tabular** | "Score 720" | Tasa 18.2% / Monto $300k | ✅ Pasó |
| **Lógica de Excepción** | "Score 640 + 6 años antigüedad" | Aprobado (Requiere firma Gerente) | ✅ Pasó |
| **Cumplimiento AML** | "Préstamo de $150,000" | Requiere Declaración de Origen de Fondos | ✅ Pasó |
| **Lógica Negativa** | "Solicito Hipoteca" | "Información no consta en manual" | ✅ Pasó |

---

## 📁 Disponibilidad de los Datos

El sistema opera sobre el documento `Politica_Credito_DummyBank.pdf` (disponible en la carpeta `/data`), un documento sintético generado para simular políticas reales de:
* Matriz de Riesgo (Score vs Tasa).
* Requisitos KYC (Know Your Customer).
* Políticas AML (Anti-Money Laundering).

---

## 👤 Autor

**Braulio Gael Porras Zuñiga**
*Data Scientist & AI Engineer | ESCOM IPN*

[LinkedIn](https://www.linkedin.com/in/braulio-porras-zuniga) | [GitHub](https://github.com/BGIA1)
