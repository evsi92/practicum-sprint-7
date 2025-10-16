from rag_bot import RAGBot
from safety_classifier import SafetyClassifier

if __name__ == "__main__":
    bot = RAGBot()
    safety = SafetyClassifier()
    print("RAG REPL — введите вопрос. 'exit' для выхода.")
    while True:
        q = input("\n🧠 Вопрос: ").strip()
        if q.lower() in ("exit", "quit"):
            break

        # Safety‑проверка
        check = safety.classify(q)
        if check["status"] == "block":
            print("❌ Запрос заблокирован:", check["flags"])
            continue
        elif check["status"] == "flag":
            print("⚠️ Запрос помечен:", check["flags"])

        result = bot.answer(q)
        print("\n📘 Ответ:\n", result["answer"])
        if "evidence" in result:
            print("\n📎 Источники (top-3):")
            for m in result["evidence"]:
                print(f"- {m.get('title')} ({m.get('source')})")