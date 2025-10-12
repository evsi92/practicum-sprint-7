from rag_bot import RAGBot

if __name__ == "__main__":
    bot = RAGBot()
    print("RAG REPL — введите вопрос. 'exit' для выхода.")
    while True:
        q = input("\n🧠 Вопрос: ").strip()
        if q.lower() in ("exit", "quit"):
            break
        result = bot.answer(q)
        print("\n📘 Ответ:\n", result["answer"])
        if "evidence" in result:
            print("\n📎 Источники (top-3):")
            for m in result["evidence"]:
                print(f"- {m.get('title')} ({m.get('source')})")