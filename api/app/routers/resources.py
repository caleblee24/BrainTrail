from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import Resource
from ..services.embeddings import embed_texts
from ..services.ranking import quality_score
from sqlalchemy import text

router = APIRouter(prefix="/resources", tags=["resources"])

@router.post("/ingest")
def ingest(url: str, title: str, content_text: str = "", source: str = "manual", module_id: int | None = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = quality_score(source, len(content_text or title))
    r = Resource(module_id=module_id, url=url, title=title, source=source, content_text=content_text, quality_score=q)
    db.add(r); db.commit(); db.refresh(r)
    vec = embed_texts([content_text or title])[0]
    db.execute(text("INSERT INTO embeddings(resource_id, embedding) VALUES (:rid, :vec)"), {"rid": r.id, "vec": vec})
    db.commit()
    return {"resource_id": r.id, "quality_score": q}
