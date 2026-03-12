from typing import List, Optional, Dict, Any
import structlog

logger = structlog.get_logger()

_client = None


def _get_client():
    global _client
    if _client is None:
        import chromadb
        from app.core.config import settings
        _client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)
        logger.info("chromadb client initialized")
    return _client


def add_documents(
    collection_name: str,
    documents: List[str],
    embeddings: List[List[float]],
    metadatas: List[Dict[str, Any]],
    ids: List[str],
) -> None:
    client = _get_client()
    collection = client.get_or_create_collection(name=collection_name)
    collection.add(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)
    logger.info("documents added to vector store", collection=collection_name, count=len(documents))


def query_similar(
    collection_name: str,
    query_embedding: List[float],
    top_k: int = 5,
    where_filter: Optional[Dict] = None,
) -> Dict[str, Any]:
    client = _get_client()
    try:
        collection = client.get_collection(name=collection_name)
    except Exception:
        return {"ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]}
    kwargs: Dict[str, Any] = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"],
    }
    if where_filter:
        kwargs["where"] = where_filter
    return collection.query(**kwargs)
