import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
import requests
import json
import csv
import io

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama3.2:1b"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "documents"

st.set_page_config(page_title="LlamaDoc Chat", page_icon="🦙", layout="wide")

st.markdown("""
<style>
.chat-user { background: #1e1e2e; padding: 1rem; border-radius: 10px; border-left: 3px solid #7c6af7; margin: 0.5rem 0; }
.chat-bot { background: #1a1a2e; padding: 1rem; border-radius: 10px; border-left: 3px solid #f76a6a; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )

def check_ollama():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        if r.status_code == 200:
            models = [m["name"] for m in r.json().get("models", [])]
            model_ok = any(MODEL_NAME in m for m in models)
            return True, model_ok
    except:
        pass
    return False, False

def extract_text(uploaded_file):
    filename = uploaded_file.name.lower()
    if filename.endswith(".txt") or filename.endswith(".md"):
        return uploaded_file.read().decode("utf-8")
    elif filename.endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    elif filename.endswith(".docx"):
        import docx
        doc = docx.Document(uploaded_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    elif filename.endswith(".csv"):
        content = uploaded_file.read().decode("utf-8")
        reader = csv.reader(io.StringIO(content))
        rows = []
        for row in reader:
            rows.append(", ".join(row))
        return "\n".join(rows)
    return ""

def chunk_text(text, size=400, overlap=40):
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i:i+size]))
        i += size - overlap
    return chunks

def ingest_doc(collection, filename, content):
    chunks = chunk_text(content)
    existing = set(collection.get()["ids"])
    ids, docs, metas = [], [], []
    for i, chunk in enumerate(chunks):
        id_ = f"{filename}__chunk_{i}"
        if id_ not in existing:
            ids.append(id_)
            docs.append(chunk)
            metas.append({"source": filename, "chunk": i})
    if ids:
        collection.add(documents=docs, ids=ids, metadatas=metas)
    return len(ids)

def get_context(collection, query, n=3):
    if collection.count() == 0:
        return "", []
    results = collection.query(query_texts=[query], n_results=min(n, collection.count()))
    sources = list({m["source"] for m in results["metadatas"][0]})
    context = "\n\n---\n\n".join(results["documents"][0])
    return context, sources

def ask_llama(prompt, system=""):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=60)
    return r.json()["message"]["content"]

if "messages" not in st.session_state:
    st.session_state.messages = []

collection = get_collection()

with st.sidebar:
    st.title("🦙 LlamaDoc Chat")
    st.caption("Local AI · llama3.2:1b · ChromaDB")

    ollama_up, model_ok = check_ollama()
    if ollama_up:
        st.success("✅ Ollama is running")
    else:
        st.error("❌ Ollama offline — run: ollama serve")
    if model_ok:
        st.success(f"✅ {MODEL_NAME} ready")
    else:
        st.warning(f"⚠️ Run: ollama pull {MODEL_NAME}")

    st.divider()
    st.subheader("📄 Upload Document")
    st.caption("Supports: PDF, DOCX, TXT, MD, CSV")

    uploaded = st.file_uploader(
        "Upload a file",
        type=["txt", "md", "pdf", "docx", "csv"]
    )
    if uploaded:
        if st.button(f"Ingest {uploaded.name}"):
            with st.spinner("Reading file..."):
                content = extract_text(uploaded)
            if content.strip():
                n = ingest_doc(collection, uploaded.name, content)
                st.success(f"✅ Added {n} chunks from {uploaded.name}!")
            else:
                st.error("❌ Could not extract text from this file.")

    with st.expander("✏️ Or paste text"):
        name = st.text_input("Name", placeholder="my-notes.txt")
        text = st.text_area("Paste content", height=100)
        if st.button("Ingest Text") and name and text:
            n = ingest_doc(collection, name, text)
            st.success(f"✅ Added {n} chunks!")

    st.divider()
    st.subheader("📚 Knowledge Base")
    count = collection.count()
    if count > 0:
        st.info(f"{count} chunks stored in ChromaDB")
        metas = collection.get()["metadatas"]
        sources = list({m["source"] for m in metas})
        for s in sources:
            st.markdown(f"📄 {s}")
        if st.button("🗑️ Clear all"):
            chromadb.PersistentClient(path=CHROMA_PATH).delete_collection(COLLECTION_NAME)
            st.rerun()
    else:
        st.caption("No documents yet.")

    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("🦙 Chat with your Documents")
st.caption("Powered by Ollama + llama3.2:1b + ChromaDB — running 100% locally")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-user">👤 <b>You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        sources = msg.get("sources", [])
        src_text = f"<br><small>📄 Sources: {', '.join(sources)}</small>" if sources else ""
        st.markdown(f'<div class="chat-bot">🦙 <b>Llama:</b> {msg["content"]}{src_text}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
user_input = st.text_input("Ask something about your documents...", key="input")

if st.button("Send 🚀") and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    context, sources = get_context(collection, user_input)
    if context:
        system = "Answer based on the context provided. Be concise and helpful."
        prompt = f"Context:\n{context}\n\nQuestion: {user_input}"
    else:
        system = "You are a helpful assistant."
        prompt = user_input
    if not ollama_up:
        reply = "⚠️ Ollama is not running. Please start it with: ollama serve"
        sources = []
    elif not model_ok:
        reply = f"⚠️ Model not found. Run: ollama pull {MODEL_NAME}"
        sources = []
    else:
        with st.spinner("🦙 Thinking..."):
            try:
                reply = ask_llama(prompt, system)
            except Exception as e:
                reply = f"⚠️ Error: {str(e)}"
                sources = []
    st.session_state.messages.append({"role": "assistant", "content": reply, "sources": sources})
    st.rerun()
