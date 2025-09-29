from sqlalchemy import text
from sqlalchemy.orm import Session
from .embeddings import embed_texts

def search_similar(db: Session, query: str, k: int = 5):
    qvec = embed_texts([query])[0]
    sql = text(
        """
        SELECT r.id, r.title, r.url, r.content_text
        FROM embeddings e
        JOIN resources r ON r.id = e.resource_id
        ORDER BY e.embedding <#> (:qvec)::vector
        LIMIT :k
        """
    )
    rows = db.execute(sql, {"qvec": qvec, "k": k}).mappings().all()
    return [dict(row) for row in rows]
