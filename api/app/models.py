from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Goal(Base):
    __tablename__ = "goals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    topic: Mapped[str] = mapped_column(String(255), index=True)
    level: Mapped[str] = mapped_column(String(50))
    timeline_days: Mapped[int] = mapped_column(Integer)
    roadmap_json: Mapped[dict | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Module(Base):
    __tablename__ = "modules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    goal_id: Mapped[int] = mapped_column(ForeignKey("goals.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    objectives: Mapped[dict] = mapped_column(JSONB)
    order_index: Mapped[int] = mapped_column(Integer)
    est_minutes: Mapped[int] = mapped_column(Integer)

class Resource(Base):
    __tablename__ = "resources"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    module_id: Mapped[int | None] = mapped_column(ForeignKey("modules.id", ondelete="SET NULL"))
    url: Mapped[str] = mapped_column(Text, unique=True)
    title: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(50))
    content_text: Mapped[str | None] = mapped_column(Text)
    quality_score: Mapped[float | None] = mapped_column(Float)

class Embedding(Base):
    __tablename__ = "embeddings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id", ondelete="CASCADE"))
    # 384 dims for MiniLM-L6-v2; adjust if you switch models
    vector = mapped_column("embedding", type_="vector(384)")

class Progress(Base):
    __tablename__ = "progress"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    percent: Mapped[float] = mapped_column(Float, default=0.0)

class Quiz(Base):
    __tablename__ = "quizzes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"))
    items: Mapped[dict] = mapped_column(JSONB)

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"))
    score: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
