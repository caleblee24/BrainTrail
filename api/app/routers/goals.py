from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..schemas import GoalCreate, GoalOut
from ..models import Goal, Module

router = APIRouter(prefix="/goals", tags=["goals"])

@router.post("/", response_model=GoalOut)
def create_goal(payload: GoalCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    goal = Goal(user_id=user.id, topic=payload.topic, level=payload.level, timeline_days=payload.timeline_days)
    db.add(goal)
    db.commit(); db.refresh(goal)
    mods = [
        Module(goal_id=goal.id, title=f"{payload.topic} — Part {i}", objectives={"bullets": ["Learn X", "Practice Y"]}, order_index=i, est_minutes=60)
        for i in range(1,4)
    ]
    db.add_all(mods); db.commit()
    return GoalOut(id=goal.id, topic=goal.topic, level=goal.level, timeline_days=goal.timeline_days)

@router.get("/{goal_id}")
def get_goal(goal_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    goal = db.query(Goal).filter_by(id=goal_id, user_id=user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    modules = db.query(Module).filter_by(goal_id=goal.id).order_by(Module.order_index).all()
    return {
        "id": goal.id,
        "topic": goal.topic,
        "level": goal.level,
        "timeline_days": goal.timeline_days,
        "modules": [
            {"id": m.id, "title": m.title, "objectives": m.objectives, "order_index": m.order_index, "est_minutes": m.est_minutes}
            for m in modules
        ],
    }
