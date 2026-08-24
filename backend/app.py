from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag import answer
from safety import check_safety


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="PsyBot API",
    description="AI-powered psychology support assistant",
    version="2.0.0"
)


# ============================================================
# CORS
# ============================================================

ALLOWED_ORIGINS = [
    # Local development
    "http://localhost:5173",
    "http://127.0.0.1:5173",

    # Vercel production
    "https://psy-bot-livid.vercel.app"
]


app.add_middleware(
    CORSMiddleware,

    allow_origins=ALLOWED_ORIGINS,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):
    message: str


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "service": "PsyBot API",
        "status": "online",
        "message": "PsyBot backend is running."
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "PsyBot API",
        "version": "2.0.0"
    }


# ============================================================
# CHAT ENDPOINT
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    message = request.message.strip()


    # --------------------------------------------------------
    # EMPTY MESSAGE
    # --------------------------------------------------------

    if not message:

        return {
            "response": "Please enter a message.",
            "safety_triggered": False
        }


    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    safety_response = check_safety(message)

    if safety_response:

        return {
            "response": safety_response,
            "safety_triggered": True
        }


    # --------------------------------------------------------
    # RAG + GEMINI
    # --------------------------------------------------------

    try:

        result = answer(message)

        return {
            "response": result["response"],
            "safety_triggered": False
        }


    except Exception as error:

        print(
            "PsyBot error:",
            repr(error)
        )

        return {
            "response": (
                "I'm unable to respond right now. "
                "Please try again in a moment."
            ),
            "safety_triggered": False
        }