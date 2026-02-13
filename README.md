# 🏦 AI Financial Compliance Agent (RAG) 🤖

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EC2-232F3E?style=flat&logo=amazon-aws&logoColor=white)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-v0.1-1C3C3C?style=flat&logo=langchain&logoColor=white)
![Status](https://img.shields.io/badge/Status-Deployed-success)

> **Automatización inteligente para el análisis de riesgo crediticio y cumplimiento normativo (AML/KYC).**

Este repositorio contiene la implementación de un **Agente Autónomo** desplegado en producción, capaz de interpretar manuales bancarios no estructurados (PDF), extraer reglas de negocio complejas y ejecutar validaciones de seguridad financiera en tiempo real.

---

## 🚀 Demo en Vivo (AWS Cloud)

El agente se encuentra desplegado en una instancia **AWS EC2 (t3.small)** y es accesible públicamente vía web.

| Plataforma | Link de Acceso | Estado |
| :--- | :--- | :--- |
| **🌐 Web App (Streamlit)** | [**👉 Abrir Asistente Financiero**](http://3.144.71.18:8501) | 🟢 Online |
| **📓 Notebook (Código)** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BGIA1/ai-financial-agent-rag/blob/main/notebooks/AI_Credit_Compliance_Agent_DummyBank.ipynb) | Investigación |

> **⚠️ Nota de Infraestructura:** Al ser un entorno de demostración, la instancia utiliza una IP dinámica. Si el enlace superior no carga, por favor consulta el repositorio más tarde para obtener la IP actualizada.

---

## 🎯 Alcance y Preguntas Sugeridas

Para optimizar costos de inferencia y asegurar el cumplimiento, el agente cuenta con **Guardrails estrictos**: responde *únicamente* preguntas relacionadas con la Política de Crédito de DummyBank. Cualquier otro tema recibirá la respuesta: *"La información no consta en el manual."*

**Prueba el agente con estas consultas:**

* **Matriz de Riesgo:** *"Soy un cliente con score de 720. ¿Cuál es mi tasa y monto máximo?"*
* **Excepciones:** *"Tengo score 640 pero soy cliente hace 6 años sin atrasos. ¿Aplico a alguna excepción?"*
* **Cumplimiento (AML):** *"Quiero solicitar $150,000 MXN. ¿Qué documentos de lavado de dinero necesito?"*
* **Requisitos:** *"¿Cuál es la edad mínima y el ingreso requerido?"*

---

## 🛠️ Stack Tecnológico y Arquitectura

El sistema ha evolucionado de un prototipo en Notebook a una aplicación contenerizada en la nube:

* **Infraestructura:** AWS EC2 (t3.small / 30GB EBS / Ubuntu Server).
* **Frontend:** Streamlit (Interfaz de chat interactiva con manejo de sesiones).
* **Orquestación:** LangChain (Implementación de *OpenAI Tools Agent*).
* **LLM:** GPT-4o (Configurado con `temperature=0` para determinismo financiero).
* **Base Vectorial:** ChromaDB (Persistencia local en servidor).
* **Ingeniería de Datos:** `RecursiveCharacterTextSplitter` optimizado para tablas financieras.

---

## ⚙️ Metodología de RAG

El flujo de trabajo se divide en 4 etapas críticas para asegurar la precisión bancaria:

1.  **Ingesta de Alta Precisión:** Filtro de caracteres (`len > 10`) para evitar la pérdida de celdas pequeñas en tablas numéricas.
2.  **Búsqueda Híbrida (MMR):** Uso de *Maximal Marginal Relevance* para recuperar contextos diversos (ej. reglas AML vs. tablas de tasas) sin saturar la ventana de contexto.
3.  **Razonamiento del Agente:** Evaluación de condiciones lógicas complejas (ej. aprobación de excepciones por antigüedad).
4.  **Safety & Guardrails:** Implementación de *Negative Testing* para rechazar solicitudes fuera de dominio (ej. Hipotecas).

---

## 📦 Dependencias Principales

El entorno de producción utiliza las siguientes librerías clave (ver `requirements.txt` para lista completa):

```text
streamlit>=1.30.0
langchain>=0.1.0
langchain-openai>=0.1.0
langchain-chroma>=0.1.0
chromadb>=0.4.24
sentence-transformers>=2.7.0
pypdf>=4.0.0
python-dotenv>=1.0.0
```

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
