# query_index.py

from chromadb import PersistentClient

# === Настройки ===
CHROMA_DIR = "./chroma_index"
COLLECTION_NAME = "quantumforge_docs"
QUERY1 = "Horcruxes"
QUERY2 = "Zarlona Rivenel"
QUERY3 = "Puma"

# === Подключение к индексу ===
client = PersistentClient(path=CHROMA_DIR)
collection = client.get_collection(name=COLLECTION_NAME)

def runQuery(query):
    # === Выполнение запроса ===
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    # === Вывод результатов ===
    for i, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        print(f"\n🔎 Результат {i+1}")
        print(f"📄 Заголовок: {meta['title']}")
        print(f"📁 Источник: {meta['source']}")
        print(f"📍 Чанк #{meta['chunk_index']}")
        print(f"📝 Текст:\n{doc[:500]}...")

runQuery(QUERY1)
runQuery(QUERY2)
runQuery(QUERY3)