import json
import pickle
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "Psychology-10K.json"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

VECTORSTORE_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

print("Loading Psychology-10K dataset...")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded {len(data)} records.")


# --------------------------------------------------
# Prepare documents
# --------------------------------------------------

documents = []

for item in data:
    user_input = item.get("input", "").strip()
    output = item.get("output", "").strip()

    if user_input and output:
        documents.append(
            {
                "input": user_input,
                "output": output
            }
        )

print(f"Prepared {len(documents)} documents.")


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# --------------------------------------------------
# Create text for embedding
# --------------------------------------------------

texts = [
    item["input"]
    for item in documents
]


# --------------------------------------------------
# Generate embeddings
# --------------------------------------------------

print("Generating embeddings...")

embeddings = embedding_model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True
)

print(f"Embedding shape: {embeddings.shape}")


# --------------------------------------------------
# Create FAISS index
# --------------------------------------------------

print("Building FAISS index...")

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings.astype("float32"))


# --------------------------------------------------
# Save FAISS index
# --------------------------------------------------

index_path = VECTORSTORE_DIR / "index.faiss"

faiss.write_index(
    index,
    str(index_path)
)


# --------------------------------------------------
# Save metadata
# --------------------------------------------------

metadata_path = VECTORSTORE_DIR / "metadata.pkl"

with open(metadata_path, "wb") as f:
    pickle.dump(documents, f)


# --------------------------------------------------
# Done
# --------------------------------------------------

print("\n========================================")
print("PsyBot vector database created!")
print("========================================")
print(f"Documents : {len(documents)}")
print(f"Dimension : {dimension}")
print(f"FAISS     : {index_path}")
print(f"Metadata  : {metadata_path}")
print("========================================")