import os
from typing import Dict, Any, List
from retriever import Retriever
from prompt_builder import build_messages, build_context
from huggingface_hub import InferenceClient
from hf_token import HF_TOKEN
from settings import HF_MODEL_NAME, MAX_CONTEXT_CHARS

class RAGBot:
    def __init__(self):
        self.retriever = Retriever()
        if not HF_TOKEN:
            raise ValueError("HF_TOKEN must be set in task4/src/hf_token.py")
        self.llm = InferenceClient(model=HF_MODEL_NAME, token=HF_TOKEN)
        print(f"Using Hugging Face model: {HF_MODEL_NAME}")

    def call_llm(self, messages: List[Dict[str, str]]) -> str:
        chat_messages = []
        for m in messages:
            role = "assistant" if m["role"] == "system" else m["role"]
            chat_messages.append({"role": role, "content": m["content"]})

        resp = self.llm.chat_completion(
            messages=chat_messages,
            max_tokens=512,
            temperature=0.2,
            top_p=0.9
        )

        return resp.choices[0].message["content"].strip()

    def answer(self, query: str) -> Dict[str, Any]:
        res = self.retriever.search(query)
        items = self.retriever.filter_and_rerank(res)

        if not self.retriever.is_confident(items):
            return {
                "answer": "I don't know the answer",
                "reason": "The context is not full",
                "evidence": [i["meta"] for i in items[:3]]
            }

        context = build_context(items)
        messages = build_messages(query, context)
        content = self.call_llm(messages)

        return {
            "answer": content,
            "evidence": [i["meta"] for i in items[:3]],
        }