import streamlit as st
from agents.orchestrator import Orchestrator

st.set_page_config(page_title="Vigenère-Squad", page_icon="🔐", layout="wide")
st.title("🔐 Vigenère-Squad — Cryptanalyse Multi-Agents")

mode = st.sidebar.selectbox(
    "Configuration des agents",
    ["Déterministe (sans LLM)", "Ollama : llama3.2:3b", "Ollama : qwen3:0.6b"],
)
model_map = {
    "Déterministe (sans LLM)": None,
    "Ollama : llama3.2:3b": "llama3.2:3b",
    "Ollama : qwen3:0.6b": "qwen3:0.6b",
}

ciphertext = st.text_area(
    "Texte chiffré à analyser :",
    value="ERQMRXU WRXW OH PRQGH",
    height=140,
)

if st.button("Lancer l'analyse multi-agents"):
    with st.spinner("Analyse en cours par les 4 agents..."):
        orch = Orchestrator(model_name=model_map[mode])
        state = orch.run(ciphertext)

    col1, col2, col3 = st.columns(3)
    col1.metric("Procédé détecté", state.cipher_type)
    col2.metric("Clé candidate", str(state.candidate_key))
    col3.metric("Itérations", state.iteration_count)

    st.subheader("Texte clair retrouvé")
    st.success(state.plaintext or "Aucun texte clair plausible trouvé.")

    st.subheader("Journal des agents et explication pédagogique")
    for res in state.results:
        with st.expander(f"{res.agent_name} — {res.status}"):
            st.write(res.message)
            st.json(res.data)
