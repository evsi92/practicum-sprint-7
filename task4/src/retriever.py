from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from settings import (
    CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL_NAME,
    TOP_N_RETRIEVE, DISTANCE_THRESHOLD
)

class Retriever:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.client = PersistentClient(path=CHROMA_DIR)
        self.collection = self.client.get_collection(name=COLLECTION_NAME)

    def embed(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

    def search(self, query: str) -> Dict[str, Any]:
        q_emb = self.embed(query)
        res = self.collection.query(
            query_embeddings=[q_emb],
            n_results=TOP_N_RETRIEVE,
            include=["documents", "metadatas", "distances"]
        )
        return res

    def filter_and_rerank(self, res: Dict[str, Any]) -> List[Dict[str, Any]]:
        docs = res["documents"][0]
        metas = res["metadatas"][0]
        dists = res["distances"][0]
        items = []

        for doc, meta, dist in zip(docs, metas, dists):
            items.append({"doc": doc, "meta": meta, "dist": dist})
        items.sort(key=lambda x: x["dist"])
        return items

    def is_confident(self, items: List[Dict[str, Any]]) -> bool:
        if not items:
            return False
        top3 = items[:3]
        avg_dist = sum(x["dist"] for x in top3) / len(top3)
        return avg_dist <= DISTANCE_THRESHOLD