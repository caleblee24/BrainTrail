from .config import settings
from typing import List

_embedder = None

def startup():
    global _embedder
    if settings.USE_LOCAL_EMBEDDINGS:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer(settings.MODEL_NAME)
    else:
        import openai  # type: ignore
        openai.api_key = settings.OPENAI_API_KEY

def embed_texts(texts: List[str]) -> List[List[float]]:
    if settings.USE_LOCAL_EMBEDDINGS:
        return _embedder.encode(texts, normalize_embeddings=True).tolist()
    else:
        raise NotImplementedError("OpenAI embeddings path not wired in MVP")
