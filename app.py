import streamlit as st
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

# ---------------------------------------
# CONFIGURACIÓN STREAMLIT
# ---------------------------------------
st.set_page_config(
    page_title="DummyBank AI Agent",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Asistente de Cumplimiento - DummyBank")
st.markdown("---")

# ---------------------------------------
# VARIABLES DE ENTORNO
# ---------------------------------------
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    st.error("No se encontró OPENAI_API_KEY.")
    st.stop()

# ---------------------------------------
# INICIALIZACIÓN DEL AGENTE (CACHE)
# ---------------------------------------
@st.cache_resource
def initialize_agent():

    # 1. Cargar PDF
    loader = PyPDFLoader("data/Politica_Credito_DummyBank.pdf")
    docs = loader.load()

    # 2. Chunking optimizado
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80
    )
    chunks = text_splitter.split_documents(docs)

    # 3. Embeddings ligeros (API)
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # 4. Vector store persistente (opcional)
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "lambda_mult": 0.7}
    )

    # 5. Tool
    @tool
    def buscar_manual(query: str) -> str:
        """Busca información oficial en el manual de crédito."""
        docs = retriever.invoke(query)
        if not docs:
            return "NO_CONTEXT_FOUND"
        return "\n---\n".join([d.page_content for d in docs])

    tools = [buscar_manual]

    # 6. LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Eres un auditor experto de riesgos de DummyBank.
1. Usa únicamente el contexto recuperado.
2. Si preguntan por tasas o montos, revisa tablas.
3. Si no está en el manual, responde: "La información no consta en el manual." """),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False
    )

    return agent_executor


# ---------------------------------------
# INICIAR AGENTE
# ---------------------------------------
try:
    agent_executor = initialize_agent()
except Exception as e:
    st.error(f"Error al inicializar el agente: {e}")
    st.stop()


# ---------------------------------------
# CHAT STATE
# ---------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------
# INPUT USUARIO
# ---------------------------------------
if prompt := st.chat_input("Escribe tu consulta sobre políticas de crédito..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analizando manual..."):

            try:
                response = agent_executor.invoke({"input": prompt})
                output_text = response["output"]

                st.markdown(output_text)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": output_text
                })

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")

