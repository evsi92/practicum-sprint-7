import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from transformers import pipeline

class SafetyClassifier:
    def __init__(self, model_name="protectai/deberta-v3-base-prompt-injection-v2"):
        self.classifier = pipeline("text-classification", model=model_name, top_k=None)

    def classify(self, text: str):
        results = self.classifier(text)[0]
        scores = {r["label"]: r["score"] for r in results}
        # нормализуем в нижний регистр
        unsafe_labels = [
            label for label, score in scores.items()
            if score > 0.7 and label.lower() not in ("safe", "benign")
        ]
        if unsafe_labels:
            return {"status": "block", "flags": unsafe_labels, "scores": scores}
        return {"status": "pass", "flags": [], "scores": scores}