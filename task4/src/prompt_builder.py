from typing import List

from task4.src.settings import MAX_CONTEXT_CHARS

SYSTEM_PROMPT = (
    "You are an assistant who answers strictly based on the provided context. "
    "First, give a short factual answer. Then list 2–3 reasoning steps with references "
    "to titles/sections from the context. If the context is insufficient, answer: 'I don’t know'."
)

FEW_SHOT = """\
Q: What is the Diadem of Bluehouse
A: The Diadem of Bluehouse is an artifact that was later used as a Horcrux.
— Based on context: art.txt (artifacts section), bluehouse.

Q: How many Horcruxes did Ravenorel create?
A: Ravenorel created seven Horcruxes.
— Based on context: book6.txt (list of Horcruxes), Ravenorel.txt.
"""

def build_context(items: List[dict]) -> str:
    picked = items[:3]
    blocks = []
    total = 0
    for it in picked:
        title = it["meta"].get("title", "")
        source = it["meta"].get("source", "")
        text = it["doc"].strip()
        header = f"[{title}] ({source})"
        chunk = f"{header}\n{text}\n"
        if total + len(chunk) > MAX_CONTEXT_CHARS:
            break
        blocks.append(chunk)
        total += len(chunk)
    return "\n\n".join(blocks)

def build_messages(user_query: str, context: str):
    user_content = (
        f"{FEW_SHOT}\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {user_query}\n"
        f"Answer instructions:\n"
        f"- A brief factual answer.\n"
        f"- Then 2–3 reasoning steps with references to titles/sections.\n"
        f"- If the context is insufficient — 'I don’t know'.\n"
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]