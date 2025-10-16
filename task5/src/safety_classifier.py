import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from transformers import pipeline

class SafetyClassifier:
    def __init__(self, model_name="protectai/deberta-v3-base-prompt-injection-v2"):
        self.classifier = pipeline("text-classification", model=model_name, top_k=None)

    def classify(self, text):
        if isinstance(text, str):
            inputs = [text]
        elif isinstance(text, (list, tuple)):
            inputs = [str(x) for x in text]
        else:
            inputs = [str(text)]

        results = self.classifier(inputs)

        if len(inputs) == 1:
            scores = {r["label"]: r["score"] for r in results[0]}
            unsafe_labels = [
                label for label, score in scores.items()
                if score > 0.7 and label.lower() not in ("safe", "benign")
            ]
            return {"status": "block" if unsafe_labels else "pass",
                    "flags": unsafe_labels,
                    "scores": scores}

        output = []
        for res in results:
            scores = {r["label"]: r["score"] for r in res}
            unsafe_labels = [
                label for label, score in scores.items()
                if score > 0.7 and label.lower() not in ("safe", "benign")
            ]
            output.append({"status": "block" if unsafe_labels else "pass",
                           "flags": unsafe_labels,
                           "scores": scores})
        return output