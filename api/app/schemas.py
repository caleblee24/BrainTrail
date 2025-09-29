from pydantic import BaseModel, EmailStr
from typing import List, Any

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class GoalCreate(BaseModel):
    topic: str
    level: str
    timeline_days: int

class ModuleOut(BaseModel):
    id: int
    title: str
    objectives: Any
    order_index: int
    est_minutes: int

class GoalOut(BaseModel):
    id: int
    topic: str
    level: str
    timeline_days: int
    modules: List[ModuleOut] | None = None

class TutorRequest(BaseModel):
    goal_id: int
    question: str
