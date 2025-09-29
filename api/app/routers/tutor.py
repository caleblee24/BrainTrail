from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..schemas import TutorRequest
from ..services.rag import search_similar
from ..services.llm import stream_answer
from ..services.cache import r, key_for

router = APIRouter(prefix="/tutor", tags=["tutor"])

@router.post("/ask/contexts")
def ask_contexts(req: TutorRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    hits = search_similar(db, req.question, k=5)
    return {"contexts": hits}

@router.post("/ask/stream")
def ask_stream(req: TutorRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    contexts = search_similar(db, req.question, k=5)
    cache_key = key_for(req.question, contexts)
    cached = r.get(cache_key)
    if cached:
        def gen_cached():
            yield f"data: {cached.decode()}\n\n"
        return StreamingResponse(gen_cached(), media_type="text/event-stream")

    def gen():
        buf = []
        for chunk in stream_answer(req.question, contexts):
            buf.append(chunk)
            yield f"data: {chunk}\n\n"
        r.setex(cache_key, 60*60, "".join(buf))
    return StreamingResponse(gen(), media_type="text/event-stream")
