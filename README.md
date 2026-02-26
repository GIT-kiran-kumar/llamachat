# llamachat
Local AI chat app using Ollama + Llama + ChromaDB + Streamlit

# 🦙 LlamaDoc Chat

A fully local, private AI-powered document chat application built with **Ollama + Llama 3.2 + ChromaDB + Streamlit**.

Ask questions about your documents using a local AI model — no internet required, no API costs, 100% private.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-green)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-orange)

---

## 🚀 What This App Does

Upload any document and chat with it using a local Llama AI model. The app reads your document, stores it in a vector database, and uses Llama to answer your questions — all running privately on your own computer.

---

## ✨ Features

- 🦙 **100% Local AI** — Runs llama3.2:1b via Ollama, completely offline
- 📄 **Multiple File Types** — Supports PDF, DOCX, TXT, MD, and CSV
- 🔍 **RAG Search** — ChromaDB vector search finds the most relevant content
- 💬 **Chat Interface** — Clean Streamlit UI with source attribution
- 🟢 **Status Panel** — Real-time Ollama and model health checks
- 🪁 **Antigravity** — Python Easter egg included!
- 🔒 **Private** — Your documents never leave your computer

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| UI Framework | Streamlit |
| AI Model | Llama 3.2:1b via Ollama |
| Vector Database | ChromaDB |
| Embeddings | sentence-transformers |
| PDF Reading | pypdf |
| Word Reading | python-docx |
| HTTP Client | requests |

---

## 📋 Prerequisites

- Windows 10/11
- Python 3.11
- Ollama installed

---

## ⚙️ Installation & Setup

### Step 1 — Install Ollama
Download from 👉 https://ollama.com/download

### Step 2 — Pull Llama Model
```bash
ollama pull llama3.2:1b
```

### Step 3 — Clone This Repository
```bash
git clone https://github.com/GIT-kiran-kumar/llamachat.git
cd llamachat
```

### Step 4 — Install Python Dependencies
```bash
py -3.11 -m pip install streamlit chromadb sentence-transformers requests antigravity pypdf python-docx
```

### Step 5 — Run the App
```bash
py -3.11 -m streamlit run app.py
```

Open your browser at **http://localhost:xxxx** 🎉

---

## 📖 How to Use

1. **Start the app** using the command above
2. **Upload a document** using the sidebar (PDF, DOCX, TXT, MD, or CSV)
3. **Click Ingest** to store it in the vector database
4. **Type your question** in the chat box
5. **Get answers** from Llama based on your document!

---

## 🗂️ Project Structure

```
llamachat/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── chroma_db/          # Auto-created when you ingest documents
```

---

## 🏗️ Architecture

```
Your Question
      │
      ▼
 Streamlit UI
      │
      ├──► ChromaDB ──► Top 3 relevant chunks
      │         ▲
      │    (sentence-transformers embeddings)
      │
      └──► Ollama API ──► llama3.2:1b
                │
                ▼
          Answer + Sources
```

---

## 💡 How to Run Again

Every time you want to use the app:

```bash
cd C:\Users\xxxxx\xxxxx\Desktop\llamachat
py -3.11 -m streamlit run app.py
```

---

## 🙏 Built With

- [Ollama](https://ollama.com) — Local LLM runner
- [Streamlit](https://streamlit.io) — Python web UI framework
- [ChromaDB](https://www.trychroma.com) — Local vector database
- [Llama 3.2](https://ai.meta.com/llama/) — Open source AI model by Meta
- [sentence-transformers](https://www.sbert.net) — Text embeddings

---

## 👨‍💻 Author

Built by **Kiran**
