import os
import chromadb
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF

PERSIST_DIR = "app/db/chroma_db"

# ✅ мультиязычная модель (казахский + русский)
model = SentenceTransformer("intfloat/multilingual-e5-base", token=os.getenv("HF_TOKEN"))

db = chromadb.PersistentClient(path=PERSIST_DIR)
collection = db.get_or_create_collection("lectures")


# ----------------------------
# 📄 PDF TEXT EXTRACTION
# ----------------------------
def extract_text(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        page_text = page.get_text()
        if page_text:
            text += page_text + "\n"

    return text


# ----------------------------
# ✂️ SMART CHUNKING
# ----------------------------
def split_text(text: str, chunk_size: int = 400):
    text = text.replace("\n", " ")
    words = text.split()

    chunks = []
    current = []

    for word in words:
        current.append(word)

        if len(current) >= chunk_size:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


# ----------------------------
# 🧠 BUILD VECTOR DB
# ----------------------------
def build_index():
    folder = "data/lectures"

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if not file.endswith(".pdf"):
            continue

        text = extract_text(path)

        if not text.strip():
            print(f"⚠️ EMPTY FILE: {file}")
            continue

        chunks = split_text(text)

        for i, chunk in enumerate(chunks):
            chunk = chunk.strip()

            if len(chunk) < 30:
                continue

            # ✅ embedding
            embedding = model.encode("passage: " + chunk).tolist()

            collection.add(
                documents=[chunk],
                embeddings=[embedding],
                ids=[f"{file}_{i}"],
                metadatas=[{"source": file}]
            )

    print("✅ PDF база создана")


# ----------------------------
# 🔎 SEARCH FUNCTION
# ----------------------------
def search(query: str):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    texts = []
    sources = []

    for doc, meta in zip(docs, metas):
        texts.append(doc)

        if meta and isinstance(meta, dict):
            sources.append(meta.get("source", "unknown"))
        else:
            sources.append("unknown")

    return texts, sources