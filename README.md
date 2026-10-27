
# 🧠 PsyBot — AI-Powered Psychology Support Chatbot

PsyBot is an AI-powered psychology support chatbot that uses **Retrieval-Augmented Generation (RAG)** to provide context-aware, psychology-focused conversational responses. It combines semantic search, vector retrieval, and language generation to deliver relevant and informative responses.

## ✨ Features

- 🧠 **RAG Pipeline:** Combines information retrieval with generative AI.
- 🔍 **Semantic Search:** Uses Sentence-BERT to identify relevant psychological content.
- ⚡ **Vector Search:** Uses FAISS for efficient similarity-based retrieval.
- 💬 **Context-Aware Responses:** Uses retrieved context to guide response generation.
- 📚 **Psychology Knowledge Base:** Uses the Psychology-10K dataset.
- 🛡️ **Responsible AI:** Designed for informational support, not professional diagnosis or treatment.

## 🏗️ Architecture

```text
User Query
    |
    v
React Frontend
    |
    v
FastAPI Backend
    |
    v
Sentence-BERT Embeddings
    |
    v
FAISS Vector Search
    |
    v
Relevant Context Retrieval
    |
    v
Google FLAN-T5 Base
    |
    v
Generated Response
    |
    v
User
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| React.js | Frontend |
| FastAPI | Backend API |
| Sentence-BERT | Text embeddings |
| FAISS | Vector similarity search |
| Google FLAN-T5 Base | Response generation |
| Psychology-10K | Psychology-focused dataset |
| Git & GitHub | Version control |

## ⚙️ How It Works

1. Preprocess psychology-related conversational data.
2. Generate text embeddings using Sentence-BERT.
3. Store embeddings in a FAISS vector index.
4. Convert user queries into embeddings.
5. Retrieve semantically relevant information.
6. Provide the retrieved context and query to the language model.
7. Return the generated response to the user.

## 🚀 Getting Started

### Prerequisites

- Python
- Node.js and npm
- Git

### Clone the Repository

```bash
git clone https://github.com/siddhuparasa/PsyBot.git
cd PsyBot
```

### Set Up the Python Environment

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Backend

If your FastAPI entry point is `main.py`:

```bash
uvicorn main:app --reload
```

API documentation:
`http://127.0.0.1:8000/docs`

### Run the Frontend

Navigate to your frontend directory:

```bash
cd frontend
npm install
npm start
```

Use the startup command defined in your `package.json` if it differs.

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/chat` | Processes a user message |
| GET | `/health` | Checks backend health |

*Confirm that these endpoints exist in your implementation.*

## 🔐 Responsible AI

- PsyBot is an experimental informational support tool.
- It does not replace qualified mental health professionals.
- AI-generated responses may contain inaccurate or incomplete information.
- Sensitive user data should be handled with appropriate privacy safeguards.

## 🔮 Future Improvements

- Improve retrieval quality with reranking.
- Evaluate answer relevance and faithfulness.
- Strengthen safety checks and input validation.
- Add privacy-conscious conversation history.
- Deploy the application with monitoring and secure configuration.

## 👨‍💻 Author

**Siddhu Parasa**

- GitHub: [@siddhuparasa](https://github.com/siddhuparasa)
- Portfolio: [siddhuparasa.github.io/My_Portfolio](https://siddhuparasa.github.io/My_Portfolio/)

---

*Exploring NLP, Retrieval-Augmented Generation, and responsible AI for psychology-focused conversational systems.*
