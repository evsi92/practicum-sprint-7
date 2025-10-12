SYSTEM_PROMPT = (
    "You are an assistant who answers strictly based on the provided context. "
    "First, give a short factual answer. Then list 2–3 reasoning steps with references "
    "to titles/sections from the context. If the context is insufficient, answer: 'I don’t know'."
)

# Use examples that actually exist in your KB domain
FEW_SHOT = """\
Q: What is the Diadem of Bluehouse?
A: It is a Bluehouse artifact; later used as a Horcrux.
— Based on context: art.txt (artifacts section), bluehouse.

Q: How many Horcruxes did Ravenorel create?
A: Seven.
— Based on context: Eldrin.txt (list of Horcruxes), Ravenorel.txt.
"""

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