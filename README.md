# HR Assistant RAG Chatbot

An HR Assistant chatbot built with **Retrieval-Augmented Generation (RAG)** using FastAPI, LangChain, ChromaDB, and **Google Gemini** (free tier).

---

## 📌 Overview

This chatbot lets employees ask HR-related questions and get accurate, context-aware answers grounded in your own HR policy documents. It retrieves the most relevant document chunks with ChromaDB and passes them to Gemini to generate a natural-language answer, along with a list of source documents and similarity scores.

---

## 🚀 Features

- Upload and delete HR policy documents (`.txt`)
- Auto-indexes existing documents in `data/` on startup
- Semantic search using ChromaDB with cosine similarity
- Multi-turn conversation with chat history
- Source documents shown with similarity scores
- Runs entirely on Google Gemini's free tier — no Azure or paid API required

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| LLM | Google Gemini (`ChatGoogleGenerativeAI`) |
| Embeddings | Google Gemini (`GoogleGenerativeAIEmbeddings`) |
| Vector Store | ChromaDB (cosine similarity) |
| RAG Pipeline | LangChain |
| Chunking | RecursiveCharacterTextSplitter |
| Templating | Jinja2 |
| Server | Uvicorn |

---

## 📦 Requirements

- Python 3.10+
- A free Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## ⚙️ Installation

\`\`\`bash
git clone https://github.com/marutirajmane/hr-rag-chatbot.git
cd hr-rag-chatbot

python -m venv venv

# Windows
venv\\Scripts\\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
\`\`\`

---

## 🔑 Configuration

1. Copy `.env.example` to `.env`
2. Get a free API key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) (attach it to a Google Cloud project — AI Studio will prompt you to create one if needed)
3. Fill in `.env`:
   \`\`\`ini
   GOOGLE_API_KEY=your-real-key-here
   GEMINI_CHAT_MODEL=gemini-3.6-flash
   GEMINI_EMBEDDING_MODEL=models/gemini-embedding-001
   INDEX_STORE=vector_db
   UPLOAD_FOLDER=data
   \`\`\`

**Never commit your real `.env` file** — it's already excluded via `.gitignore`.

---

## ▶️ Running the app

\`\`\`bash
python main.py
\`\`\`

Then open:
- **http://localhost:8000** — chat interface
- **http://localhost:8000/manage** — upload/delete HR documents

---

## ⚠️ Notes

- Only `.txt` files are supported for HR documents.
- If you change the embedding model, delete the `vector_db/` folder and restart so documents get re-indexed with the new embedding dimensions.
- Gemini's free tier has rate limits — if you hit a quota error, wait a minute and retry.