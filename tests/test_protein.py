"""
Unit tests for core/protein_engine.py
Verifies BMR, TDEE, goal caloric adjustments, and high-protein (1.6 - 2.2g/kg) distributions.
"""

import pytest
from core.protein_engine import (
    Gender,
    ActivityLevel,
    FitnessGoal,
    UserProfileInput,
    calculate_bmr,
    calculate_tdee,
    calculate_macro_targets,
)


def test_bmr_calculation():
    # Male: 10 * 80 + 6.25 * 180 - 5 * 30 + 5 = 800 + 1125 - 150 + 5 = 1780.0
    bmr_male = calculate_bmr(80.0, 180.0, 30, Gender.MALE)
    assert bmr_male == 1780.0

    # Female: 10 * 65 + 6.25 * 165 - 5 * 28 - 161 = 650 + 1031.25 - 140 - 161 = 1380.25 -> 1380.2
    bmr_female = calculate_bmr(65.0, 165.0, 28, Gender.FEMALE)
    assert bmr_female == pytest.approx(1380.2, abs=0.2)


def test_tdee_calculation():
    bmr = 1800.0
    tdee_sedentary = calculate_tdee(bmr, ActivityLevel.SEDENTARY)
    assert tdee_sedentary == 1800.0 * 1.2

    tdee_moderate = calculate_tdee(bmr, ActivityLevel.MODERATE)
    assert tdee_moderate == 1800.0 * 1.55

    tdee_extra = calculate_tdee(bmr, ActivityLevel.EXTRA_ACTIVE)
    assert tdee_extra == 1800.0 * 1.9


def test_fat_loss_high_protein_distribution():
    profile = UserProfileInput(
        weight_kg=75.0,
        height_cm=175.0,
        age=25,
        gender=Gender.MALE,
        activity_level=ActivityLevel.MODERATE,
        goal=FitnessGoal.FAT_LOSS,
        meals_per_day=3,
    )
    targets = calculate_macro_targets(profile)

    # Fat loss defaults to 2.2g/kg protein
    assert targets.protein_multiplier_used == 2.2
    assert targets.protein_g == pytest.approx(75.0 * 2.2, abs=0.1)
    
    # Protein should make up significant calorie percentage
    assert targets.protein_calories_pct > 25.0
    assert targets.target_calories < targets.tdee  # Deficit confirmed
    assert len(targets.meals) == 3

    # Check leucine threshold per meal
    for meal in targets.meals:
        assert meal.target_protein_g >= 28.0
        assert meal.leucine_threshold_met is True


def test_muscle_gain_surplus_and_protein():
    profile = UserProfileInput(
        weight_kg=85.0,
        height_cm=185.0,
        age=24,
        gender=Gender.MALE,
        activity_level=ActivityLevel.VERY_ACTIVE,
        goal=FitnessGoal.MUSCLE_GAIN,
        protein_multiplier=2.0,
        meals_per_day=4,
    )
    targets = calculate_macro_targets(profile)

    assert targets.target_calories > targets.tdee  # Surplus confirmed
    assert targets.protein_g == 85.0 * 2.0
    assert len(targets.meals) == 4


def test_custom_protein_multiplier_bounds():
    profile = UserProfileInput(
        weight_kg=70.0,
        height_cm=170.0,
        age=30,
        gender=Gender.FEMALE,
        activity_level=ActivityLevel.LIGHT,
        goal=FitnessGoal.MAINTENANCE,
        protein_multiplier=1.8,
        meals_per_day=3,
    )
    targets = calculate_macro_targets(profile)
    assert targets.protein_g == pytest.approx(70.0 * 1.8, abs=0.1)
    assert targets.target_calories == pytest.approx(targets.tdee, abs=15.0)


def test_high_protein_and_calorie_intake():
    profile = UserProfileInput(
        weight_kg=105.0,
        height_cm=190.0,
        age=28,
        gender=Gender.MALE,
        activity_level=ActivityLevel.EXTRA_ACTIVE,
        goal=FitnessGoal.MUSCLE_GAIN,
        protein_multiplier=2.6,
        meals_per_day=5,
    )
    targets = calculate_macro_targets(profile)
    assert targets.protein_g == pytest.approx(105.0 * 2.6, abs=0.5)
    assert targets.target_calories > 3000.0
    assert targets.fats_g > 40.0
    assert targets.carbs_g > 100.0
    assert len(targets.meals) == 5
