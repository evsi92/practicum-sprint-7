import os
import uuid
from pathlib import Path
from tqdm import tqdm

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from sentence_transformers import SentenceTransformer
from datetime import datetime
import chromadb
from chromadb.config import Settings

# === Настройки ===
SOURCE_DIR = "./data"  # Папка с текстовыми файлами (MD, PDF, TXT)
CHUNK_SIZE = 500       # Размер чанка в токенах
CHUNK_OVERLAP = 100     # Перекрытие между чанками
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DIR = "./chroma_index"

# === Шаг 1: Загрузка документов ===
def load_documents(source_dir):
    documents = []
    for filepath in Path(source_dir).rglob("*.*"):
        if filepath.suffix.lower() in [".md", ".txt"]:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
                documents.append(Document(page_content=text, metadata={
                    "source": str(filepath),
                    "title": filepath.stem
                }))
    return documents

# === Шаг 2: Разбиение на чанки ===
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[".", "!", "?", " "]
    )
    return splitter.split_documents(documents)

# === Шаг 3: Генерация эмбеддингов ===
def embed_chunks(chunks, model):
    texts = [chunk.page_content for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings

# === Шаг 4: Сохранение в ChromaDB ===
def save_to_chroma(chunks, embeddings, persist_dir, batch_size=5000):
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection(name="quantumforge_docs")

    ids = []
    metadatas = []
    documents = []

    for i, chunk in enumerate(chunks):
        chunk_id = str(uuid.uuid4())
        ids.append(chunk_id)
        metadatas.append({
            "source": chunk.metadata.get("source", ""),
            "title": chunk.metadata.get("title", ""),
            "chunk_index": i
        })
        documents.append(chunk.page_content)

    total = len(chunks)
    print(f"📦 Загружаем {total} чанков в ChromaDB по {batch_size} в батче...")

    for i in tqdm(range(0, total, batch_size), desc="🔄 Загрузка батчей"):
        batch_ids = ids[i:i+batch_size]
        batch_docs = documents[i:i+batch_size]
        batch_embeds = embeddings[i:i+batch_size]
        batch_meta = metadatas[i:i+batch_size]

        assert len(batch_ids) == len(batch_docs) == len(batch_embeds) == len(batch_meta), "❌ Несовпадение размеров батча"

        collection.add(
            ids=batch_ids,
            documents=batch_docs,
            embeddings=batch_embeds,
            metadatas=batch_meta
        )

    print(f"✅ Успешно загружено {total} чанков в ChromaDB")


# === Основной пайплайн ===
def main():
    now = datetime.now()
    print("Время начала (HH:MM:SS):", now.strftime("%H:%M:%S"))

    print("📥 Загружаем документы...")
    documents = load_documents(SOURCE_DIR)
    print(f"🔍 Найдено документов: {len(documents)}")

    print("✂️ Разбиваем на чанки...")
    chunks = chunk_documents(documents)
    print(f"📦 Получено чанков: {len(chunks)}")

    print("🧠 Загружаем модель эмбеддингов...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("⚙️ Генерируем эмбеддинги...")
    embeddings = embed_chunks(chunks, model)

    print("🗃️ Сохраняем в ChromaDB...")
    save_to_chroma(chunks, embeddings, CHROMA_DIR)

    now = datetime.now()
    print("Время окончания (HH:MM:SS):", now.strftime("%H:%M:%S"))

if __name__ == "__main__":
    main()