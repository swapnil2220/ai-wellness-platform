"""
Database Schema & SQLite ORM Layer (database/db.py)
--------------------------------------------------
Uses SQLAlchemy to manage local SQLite storage for:
- UserProfileRecord: User body metrics, goals, and target macros
- DailyMacroLogRecord: Daily macro tracking totals (Calories, Protein, Carbs, Fats, Water)
- LoggedMealRecord: Individual logged meals and recipes
- SavedInsightRecord: Bookmarked mindset & book takeaways
"""

import datetime
import json
import os
from typing import Any, Dict, List, Optional
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session

Base = declarative_base()


def _get_utc_now():
    return datetime.datetime.now(datetime.timezone.utc)


class UserProfileRecord(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    weight_kg = Column(Float, nullable=False)
    height_cm = Column(Float, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False, default="male")
    activity_level = Column(String(50), nullable=False, default="moderate")
    goal = Column(String(50), nullable=False, default="fat_loss")
    protein_multiplier = Column(Float, nullable=False, default=2.0)
    bmr = Column(Float, nullable=True)
    tdee = Column(Float, nullable=True)
    target_calories = Column(Float, nullable=False)
    target_protein_g = Column(Float, nullable=False)
    target_carbs_g = Column(Float, nullable=False)
    target_fats_g = Column(Float, nullable=False)
    created_at = Column(DateTime, default=_get_utc_now)
    updated_at = Column(DateTime, default=_get_utc_now, onupdate=_get_utc_now)


class DailyMacroLogRecord(Base):
    __tablename__ = "daily_macro_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    log_date = Column(Date, nullable=False, unique=True, default=datetime.date.today)
    total_calories = Column(Float, default=0.0)
    total_protein_g = Column(Float, default=0.0)
    total_carbs_g = Column(Float, default=0.0)
    total_fats_g = Column(Float, default=0.0)
    water_ml = Column(Integer, default=0)
    step_count = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=_get_utc_now)

    meals = relationship("LoggedMealRecord", back_populates="daily_log", cascade="all, delete-orphan")


class LoggedMealRecord(Base):
    __tablename__ = "logged_meals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    daily_log_id = Column(Integer, ForeignKey("daily_macro_logs.id"), nullable=False)
    meal_name = Column(String(200), nullable=False)
    meal_type = Column(String(50), nullable=False, default="lunch")
    protein_g = Column(Float, nullable=False)
    carbs_g = Column(Float, nullable=False)
    fat_g = Column(Float, nullable=False)
    calories = Column(Float, nullable=False)
    ingredients_json = Column(Text, nullable=True)
    logged_time = Column(DateTime, default=_get_utc_now)

    daily_log = relationship("DailyMacroLogRecord", back_populates="meals")


class SavedInsightRecord(Base):
    __tablename__ = "saved_insights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    insight_id = Column(String(100), nullable=False)
    book_title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    concept_title = Column(String(200), nullable=False)
    quote = Column(Text, nullable=False)
    actionable_protocol = Column(Text, nullable=False)
    created_at = Column(DateTime, default=_get_utc_now)


# Database Connection Helpers
DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "wellness.db")
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

_ENGINE_CACHE: Dict[str, Any] = {}
_SESSION_CACHE: Dict[str, Any] = {}


def get_engine(db_url: Optional[str] = None):
    url = db_url or DATABASE_URL
    if url not in _ENGINE_CACHE:
        _ENGINE_CACHE[url] = create_engine(
            url,
            connect_args={"check_same_thread": False} if "sqlite" in url else {}
        )
    return _ENGINE_CACHE[url]


def init_db(db_url: Optional[str] = None):
    """Create all tables in the database."""
    engine = get_engine(db_url)
    Base.metadata.create_all(bind=engine)
    return engine


def get_session(db_url: Optional[str] = None) -> Session:
    """Return a new SQLAlchemy database session."""
    url = db_url or DATABASE_URL
    engine = get_engine(url)
    init_db(url)
    if url not in _SESSION_CACHE:
        _SESSION_CACHE[url] = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SESSION_CACHE[url]()


# CRUD Operations
def save_or_update_profile(
    session: Session,
    weight_kg: float,
    height_cm: float,
    age: int,
    gender: str,
    activity_level: str,
    goal: str,
    protein_multiplier: float,
    bmr: float,
    tdee: float,
    target_calories: float,
    target_protein_g: float,
    target_carbs_g: float,
    target_fats_g: float,
) -> UserProfileRecord:
    """Save or update the latest user profile and targets."""
    profile = session.query(UserProfileRecord).order_by(UserProfileRecord.id.desc()).first()
    if not profile:
        profile = UserProfileRecord()
        session.add(profile)

    profile.weight_kg = weight_kg
    profile.height_cm = height_cm
    profile.age = age
    profile.gender = gender
    profile.activity_level = activity_level
    profile.goal = goal
    profile.protein_multiplier = protein_multiplier
    profile.bmr = bmr
    profile.tdee = tdee
    profile.target_calories = target_calories
    profile.target_protein_g = target_protein_g
    profile.target_carbs_g = target_carbs_g
    profile.target_fats_g = target_fats_g
    profile.updated_at = _get_utc_now()

    session.commit()
    session.refresh(profile)
    return profile


def get_latest_profile(session: Session) -> Optional[UserProfileRecord]:
    """Retrieve the most recent user profile."""
    return session.query(UserProfileRecord).order_by(UserProfileRecord.id.desc()).first()


def get_or_create_daily_log(session: Session, target_date: Optional[datetime.date] = None) -> DailyMacroLogRecord:
    """Fetch or initialize the daily macro log record for a given date."""
    d = target_date or datetime.date.today()
    log = session.query(DailyMacroLogRecord).filter(DailyMacroLogRecord.log_date == d).first()
    if not log:
        log = DailyMacroLogRecord(log_date=d)
        session.add(log)
        session.commit()
        session.refresh(log)
    return log


def log_meal(
    session: Session,
    meal_name: str,
    meal_type: str,
    protein_g: float,
    carbs_g: float,
    fat_g: float,
    calories: float,
    ingredients_list: Optional[List[Dict[str, Any]]] = None,
    target_date: Optional[datetime.date] = None
) -> LoggedMealRecord:
    """Log a meal and update today's macro aggregates."""
    daily_log = get_or_create_daily_log(session, target_date)

    ingredients_json = json.dumps(ingredients_list) if ingredients_list else None
    meal = LoggedMealRecord(
        daily_log_id=daily_log.id,
        meal_name=meal_name,
        meal_type=meal_type,
        protein_g=round(protein_g, 1),
        carbs_g=round(carbs_g, 1),
        fat_g=round(fat_g, 1),
        calories=round(calories, 1),
        ingredients_json=ingredients_json,
    )
    session.add(meal)

    # Update daily log totals
    daily_log.total_calories = round(daily_log.total_calories + calories, 1)
    daily_log.total_protein_g = round(daily_log.total_protein_g + protein_g, 1)
    daily_log.total_carbs_g = round(daily_log.total_carbs_g + carbs_g, 1)
    daily_log.total_fats_g = round(daily_log.total_fats_g + fat_g, 1)

    session.commit()
    session.refresh(meal)
    return meal


def get_today_progress(session: Session, target_date: Optional[datetime.date] = None) -> Dict[str, Any]:
    """Retrieve today's aggregate calories, macros, and logged meals list."""
    daily_log = get_or_create_daily_log(session, target_date)
    meals = (
        session.query(LoggedMealRecord)
        .filter(LoggedMealRecord.daily_log_id == daily_log.id)
        .order_by(LoggedMealRecord.logged_time.desc())
        .all()
    )

    return {
        "date": str(daily_log.log_date),
        "total_calories": daily_log.total_calories,
        "total_protein_g": daily_log.total_protein_g,
        "total_carbs_g": daily_log.total_carbs_g,
        "total_fats_g": daily_log.total_fats_g,
        "water_ml": daily_log.water_ml,
        "meals_count": len(meals),
        "meals": [
            {
                "id": m.id,
                "meal_name": m.meal_name,
                "meal_type": m.meal_type,
                "protein_g": m.protein_g,
                "carbs_g": m.carbs_g,
                "fat_g": m.fat_g,
                "calories": m.calories,
                "time": m.logged_time.strftime("%H:%M") if m.logged_time else ""
            }
            for m in meals
        ]
    }


def get_all_logged_meals(session: Session, limit: int = 20) -> List[LoggedMealRecord]:
    """Get the recent logged meals."""
    return session.query(LoggedMealRecord).order_by(LoggedMealRecord.logged_time.desc()).limit(limit).all()


def save_favorite_insight(
    session: Session,
    insight_id: str,
    book_title: str,
    author: str,
    concept_title: str,
    quote: str,
    actionable_protocol: str
) -> SavedInsightRecord:
    """Save an insight to favorites."""
    existing = session.query(SavedInsightRecord).filter(SavedInsightRecord.insight_id == insight_id).first()
    if existing:
        return existing

    record = SavedInsightRecord(
        insight_id=insight_id,
        book_title=book_title,
        author=author,
        concept_title=concept_title,
        quote=quote,
        actionable_protocol=actionable_protocol
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


def get_favorite_insights(session: Session) -> List[SavedInsightRecord]:
    """Get all saved favorite insights."""
    return session.query(SavedInsightRecord).order_by(SavedInsightRecord.created_at.desc()).all()


def update_water(session: Session, delta_ml: int, target_date: Optional[datetime.date] = None) -> DailyMacroLogRecord:
    """Add/subtract water intake in mL for the daily log."""
    log = get_or_create_daily_log(session, target_date)
    log.water_ml = max(0, log.water_ml + delta_ml)
    session.commit()
    session.refresh(log)
    return log
