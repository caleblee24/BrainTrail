from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import Progress

router = APIRouter(prefix="/progress", tags=["progress"])

@router.post("/tick")
def tick(module_id: int, percent: float, db: Session = Depends(get_db), user=Depends(get_current_user)):
    row = db.query(Progress).filter_by(user_id=user.id, module_id=module_id).first()
    if not row:
        row = Progress(user_id=user.id, module_id=module_id, percent=percent, completed=percent>=100)
        db.add(row)
    else:
        row.percent = percent
        row.completed = percent >= 100
    db.commit()
    return {"ok": True}
