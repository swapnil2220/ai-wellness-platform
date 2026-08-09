"""
Unit tests for database/db.py
Verifies SQLite ORM CRUD operations, meal logging, and macro aggregation.
"""

import os
import pytest
from database.db import (
    get_session,
    save_or_update_profile,
    get_latest_profile,
    authenticate_user,
    log_meal,
    get_today_progress,
    save_favorite_insight,
    get_favorite_insights,
)

TEST_DB_PATH = "sqlite:///:memory:"


@pytest.fixture
def db_session():
    session = get_session(TEST_DB_PATH)
    yield session
    session.close()


def test_profile_crud(db_session):
    prof = save_or_update_profile(
        session=db_session,
        weight_kg=78.5,
        height_cm=182.0,
        age=29,
        gender="male",
        activity_level="very_active",
        goal="fat_loss",
        protein_multiplier=2.2,
        bmr=1780.0,
        tdee=2800.0,
        target_calories=2240.0,
        target_protein_g=172.7,
        target_carbs_g=210.0,
        target_fats_g=62.0,
    )
    assert prof.id is not None
    assert prof.weight_kg == 78.5

    fetched = get_latest_profile(db_session)
    assert fetched is not None
    assert fetched.target_protein_g == 172.7


def test_meal_logging_and_today_progress(db_session):
    # Log 2 meals
    m1 = log_meal(
        session=db_session,
        meal_name="Greek Yogurt Protein Fluff",
        meal_type="breakfast",
        protein_g=45.0,
        carbs_g=25.0,
        fat_g=8.0,
        calories=352.0,
    )
    assert m1.id is not None

    m2 = log_meal(
        session=db_session,
        meal_name="Grilled Salmon & Quinoa",
        meal_type="lunch",
        protein_g=50.0,
        carbs_g=40.0,
        fat_g=14.0,
        calories=486.0,
    )
    assert m2.id is not None

    summary = get_today_progress(db_session)
    assert summary["meals_count"] == 2
    assert summary["total_protein_g"] == 95.0
    assert summary["total_calories"] == 838.0


def test_user_authentication_and_password(db_session):
    save_or_update_profile(
        session=db_session,
        user_id="swapnil",
        password="mysecretpassword",
        name="Swapnil Shrivastava",
        weight_kg=75.0,
        height_cm=178.0,
        age=28,
        gender="male",
        activity_level="moderate",
        goal="fat_loss",
        protein_multiplier=2.0,
        bmr=1700.0,
        tdee=2400.0,
        target_calories=1920.0,
        target_protein_g=150.0,
        target_carbs_g=180.0,
        target_fats_g=50.0,
    )
    
    # Test successful login
    ok, prof, msg = authenticate_user(db_session, "swapnil", "mysecretpassword")
    assert ok is True
    assert prof is not None
    assert prof.name == "Swapnil Shrivastava"
    
    # Test wrong password
    ok_fail, prof_fail, msg_fail = authenticate_user(db_session, "swapnil", "wrongpassword")
    assert ok_fail is False
    assert prof_fail is None
    assert "Incorrect password" in msg_fail

    # Test non-existent user
    ok_no_user, _, _ = authenticate_user(db_session, "non_existent_user", "password")
    assert ok_no_user is False


def test_save_favorite_insight(db_session):
    saved = save_favorite_insight(
        session=db_session,
        insight_id="atomic_habits_identity",
        book_title="Atomic Habits",
        author="James Clear",
        concept_title="Identity-Based Habits",
        quote="Every action is a vote for your future self.",
        actionable_protocol="Scale habit to 2 minutes."
    )
    assert saved.id is not None

    all_saved = get_favorite_insights(db_session)
    assert len(all_saved) == 1
    assert all_saved[0].book_title == "Atomic Habits"
