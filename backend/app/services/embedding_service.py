from typing import List
import structlog

logger = structlog.get_logger()

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        from app.core.config import settings
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
        logger.info("embedding model loaded", model=settings.EMBEDDING_MODEL)
    return _model


def embed_text(text: str) -> List[float]:
    model = _get_model()
    return model.encode(text).tolist()


def embed_batch(texts: List[str]) -> List[List[float]]:
    model = _get_model()
    return model.encode(texts).tolist()
