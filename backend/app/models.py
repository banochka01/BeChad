import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

def now(): return datetime.now(timezone.utc)
def uid(): return str(uuid.uuid4())
class User(Base):
    __tablename__="users"
    id: Mapped[str]=mapped_column(String, primary_key=True, default=uid)
    email: Mapped[str]=mapped_column(String(320), unique=True, index=True)
    username: Mapped[str]=mapped_column(String(40), unique=True, index=True)
    display_name: Mapped[str]=mapped_column(String(80), default="BeChad")
    password_hash: Mapped[str]=mapped_column(String(255))
    timezone: Mapped[str]=mapped_column(String(80), default="UTC")
    xp: Mapped[int]=mapped_column(Integer, default=0)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now, onupdate=now)
class RefreshToken(Base):
    __tablename__="refresh_tokens"
    id: Mapped[str]=mapped_column(String, primary_key=True, default=uid)
    user_id: Mapped[str]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str]=mapped_column(String(255), unique=True)
    revoked: Mapped[bool]=mapped_column(Boolean, default=False)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
class DailyQuest(Base):
    __tablename__="daily_quests"
    id: Mapped[str]=mapped_column(String, primary_key=True, default=uid)
    user_id: Mapped[str]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    day: Mapped[str]=mapped_column(String(10), index=True)
    title: Mapped[str]=mapped_column(String(120))
    category: Mapped[str]=mapped_column(String(40), index=True)
    difficulty: Mapped[str]=mapped_column(String(16))
    base_xp: Mapped[int]=mapped_column(Integer)
    is_main: Mapped[bool]=mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
    __table_args__=(Index("ix_daily_user_day", "user_id", "day"),)
class QuestCompletion(Base):
    __tablename__="quest_completions"
    id: Mapped[str]=mapped_column(String, primary_key=True, default=uid)
    user_id: Mapped[str]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    quest_id: Mapped[str]=mapped_column(ForeignKey("daily_quests.id", ondelete="CASCADE"), index=True)
    idempotency_key: Mapped[str]=mapped_column(String(80))
    xp_awarded: Mapped[int]=mapped_column(Integer)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
    __table_args__=(UniqueConstraint("user_id","idempotency_key", name="uq_completion_idem"),)
class XpEvent(Base):
    __tablename__="xp_events"
    id: Mapped[str]=mapped_column(String, primary_key=True, default=uid)
    user_id: Mapped[str]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    amount: Mapped[int]=mapped_column(Integer)
    reason: Mapped[str]=mapped_column(String(80))
    ref_id: Mapped[str]=mapped_column(String, index=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
class Streak(Base):
    __tablename__="streaks"
    user_id: Mapped[str]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    current: Mapped[int]=mapped_column(Integer, default=0); best: Mapped[int]=mapped_column(Integer, default=0)
    last_day: Mapped[str|None]=mapped_column(String(10), nullable=True); freezes: Mapped[int]=mapped_column(Integer, default=1)
class Achievement(Base):
    __tablename__="achievements"
    code: Mapped[str]=mapped_column(String(40), primary_key=True)
    title: Mapped[str]=mapped_column(String(100)); description: Mapped[str]=mapped_column(String(200))
class UserAchievement(Base):
    __tablename__="user_achievements"
    user_id: Mapped[str]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    achievement_code: Mapped[str]=mapped_column(ForeignKey("achievements.code"), primary_key=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
class FriendRequest(Base):
    __tablename__="friend_requests"
    id: Mapped[str]=mapped_column(String, primary_key=True, default=uid)
    from_user_id: Mapped[str]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    to_user_id: Mapped[str]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    status: Mapped[str]=mapped_column(String(16), default="pending")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
class Friendship(Base):
    __tablename__="friendships"
    user_id: Mapped[str]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    friend_id: Mapped[str]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
class CoachMessage(Base):
    __tablename__="coach_messages"
    id: Mapped[str]=mapped_column(String, primary_key=True, default=uid)
    user_id: Mapped[str]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role: Mapped[str]=mapped_column(String(20)); content: Mapped[str]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
