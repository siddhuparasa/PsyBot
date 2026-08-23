import os
import pickle
from pathlib import Path

import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

INDEX_PATH = (
    BASE_DIR
    / "vectorstore"
    / "index.faiss"
)

METADATA_PATH = (
    BASE_DIR
    / "vectorstore"
    / "metadata.pkl"
)


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(
    BASE_DIR / ".env"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

if not GEMINI_API_KEY:

    raise RuntimeError(
        "GEMINI_API_KEY was not found."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# Keep the model in one variable so it can
# easily be changed later.

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


# ============================================================
# LOAD FAISS INDEX
# ============================================================

print(
    "Loading PsyBot vector database..."
)

if not INDEX_PATH.exists():

    raise FileNotFoundError(
        f"FAISS index not found: {INDEX_PATH}"
    )


index = faiss.read_index(
    str(INDEX_PATH)
)

print(
    f"FAISS index loaded: "
    f"{index.ntotal} documents"
)


# ============================================================
# LOAD METADATA
# ============================================================

if not METADATA_PATH.exists():

    raise FileNotFoundError(
        f"Metadata file not found: "
        f"{METADATA_PATH}"
    )


with open(
    METADATA_PATH,
    "rb"
) as f:

    documents = pickle.load(f)


print(
    f"Metadata loaded: "
    f"{len(documents)} documents"
)


# ============================================================
# LOAD SENTENCE TRANSFORMER
# ============================================================

print(
    "Loading embedding model..."
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print(
    "Embedding model loaded."
)


# ============================================================
# RETRIEVE RELEVANT DATASET EXAMPLES
# ============================================================

def retrieve_context(
    question: str,
    top_k: int = 2
):

    question_embedding = (
        embedding_model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True
        )
    )


    scores, indices = index.search(
        question_embedding.astype(
            "float32"
        ),
        top_k
    )


    results = []


    for score, idx in zip(
        scores[0],
        indices[0]
    ):

        if idx == -1:
            continue


        results.append(
            {
                "score": float(score),
                "input": documents[idx]["input"],
                "output": documents[idx]["output"]
            }
        )


    return results


# ============================================================
# GENERATE RESPONSE
# ============================================================

def generate_response(
    question: str,
    contexts: list
):

    context_text = ""


    for i, item in enumerate(
        contexts,
        start=1
    ):

        context_text += f"""
Example {i}

User concern:
{item["input"]}

Reference response:
{item["output"]}

"""


    prompt = f"""
You are PsyBot, a psychology-focused support chatbot.

Use the retrieved psychology examples as your
PRIMARY reference for answering the user.

RULES:

1. Keep the response SHORT.

2. Write only 2 to 4 sentences.

3. Stay close to the information,
   tone and style of the retrieved
   reference responses.

4. Use the retrieved responses as
   the main source for your answer.

5. Do not copy any reference response
   word-for-word.

6. Make the response natural and
   relevant to the user's message.

7. Do not add unnecessary explanations.

8. Do not introduce unrelated information.

9. Never mention:
   - Psychology-10K
   - FAISS
   - RAG
   - embeddings
   - Gemini
   - retrieved examples
   - internal system details

10. Do not diagnose the user.

11. Do not claim to be a psychologist,
    therapist or doctor.

12. If appropriate, gently suggest
    speaking with a qualified professional.

13. Do not repeat the user's question.

14. Do not use headings or bullet points
    unless they are genuinely necessary.

15. Give a concise, supportive response.

RETRIEVED EXAMPLES:

{context_text}

USER MESSAGE:

{question}

Write ONLY the final response.
"""


    # ========================================================
    # GEMINI
    # ========================================================

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )


    generated_text = (
        response.text.strip()
        if response.text
        else ""
    )


    # ========================================================
    # FALLBACK
    # ========================================================

    if not generated_text:

        if contexts:

            generated_text = (
                contexts[0]["output"]
            )

        else:

            generated_text = (
                "I’m here to help you reflect "
                "on what you're experiencing."
            )


    # ========================================================
    # CLEAN RESPONSE
    # ========================================================

    prefixes = [
        "Response:",
        "response:",
        "Final response:",
        "final response:",
        "Supportive response:",
        "supportive response:"
    ]


    for prefix in prefixes:

        if generated_text.startswith(prefix):

            generated_text = (
                generated_text[
                    len(prefix):
                ].strip()
            )


    return generated_text


# ============================================================
# MAIN RAG PIPELINE
# ============================================================

def answer(
    question: str
):

    contexts = retrieve_context(
        question,
        top_k=2
    )


    response = generate_response(
        question,
        contexts
    )


    return {
        "response": response,
        "contexts": contexts
    }