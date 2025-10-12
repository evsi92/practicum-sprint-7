CHROMA_DIR = "../../task3/chroma_index"
COLLECTION_NAME = "quantumforge_docs"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

TOP_N_RETRIEVE = 5       # initial recall
DISTANCE_THRESHOLD = 0.9  # tune for your embedding model (lower = stricter)
MAX_CONTEXT_CHARS = 8000   # guardrail for prompt size

HF_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"