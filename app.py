import streamlit as st
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool
from langchain.agents import create_agent

# -------------------------------------------------
# 1. Configuración de página
# -------------------------------------------------

st.set_page_config(
    page_title="DummyBank AI Agent",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Asistente de Cumplimiento - DummyBank")
st.markdown("---")

# -------------------------------------------------
# 2. Cargar variables de entorno
# -------------------------------------------------

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ No se encontró la API Key en el archivo .env")
    st.stop()

# -------------------------------------------------
# 3. Inicialización con cache (evita recalcular embeddings)
# -------------------------------------------------

@st.cache_resource
def initialize_agent():

    with st.spinner("🔄 Cargando manual y configurando agente..."):

        # A. Cargar PDF
        loader = PyPDFLoader("data/Politica_Credito_DummyBank.pdf")
        docs = loader.load()

        # B. Chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80
        )
        chunks = text_splitter.split_documents(docs)

        # C. Embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # D. Vector Store (persistente en memoria)
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings
        )

        # E. Retriever con MMR (mejor diversidad)
        retriever = vector_db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 6,
                "lambda_mult": 0.7
            }
        )

        # F. Tool controlada
        @tool
        def buscar_manual(query: str) -> str:
            """Busca información oficial en el manual de crédito."""
            docs = retriever.invoke(query)

            if not docs:
                return "NO_CONTEXT_FOUND"

            context = "\n\n---\n\n".join(
                [d.page_content for d in docs if len(d.page_content) > 50]
            )

            return context[:4000]  # evitar prompt inflation

        # G. LLM determinista
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=500
        )

        # H. Crear agente (LangChain 1.x)
        agent = create_agent(
            model=llm,
            tools=[buscar_manual],
            system_prompt="""
Eres un auditor de riesgos experto de DummyBank.

Reglas obligatorias:
1. Responde exclusivamente usando la información recuperada.
2. Si la herramienta devuelve NO_CONTEXT_FOUND,
   responde: "La información no consta en el manual."
3. No inventes información.
4. No uses conocimiento externo.
"""
        )

        return agent

# -------------------------------------------------
# 4. Inicializar agente
# -------------------------------------------------

try:
    agent_executor = initialize_agent()
except Exception as e:
    st.error(f"Error al inicializar el agente: {e}")
    st.stop()

# -------------------------------------------------
# 5. Historial de chat
# -------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------------------------
# 6. Input del usuario
# -------------------------------------------------

if prompt := st.chat_input("Consulta sobre políticas de crédito..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Analizando manual..."):
            try:
                response = agent_executor.invoke({
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                })

                output_text = response["messages"][-1].content

                st.markdown(output_text)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": output_text
                })

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
