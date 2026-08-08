"""
Unit tests for core/meal_planner.py
Validates schema formatting, recipe scaling, dietary preference compliance, and supplement links.
"""

import pytest
from core.meal_planner import (
    DietaryPreference,
    MealType,
    MealPlanRequest,
    RecipeModel,
    generate_high_protein_meal,
    AFFILIATE_CATALOG,
)


def test_offline_meal_generation_structure():
    req = MealPlanRequest(
        target_protein_g=45.0,
        target_calories=450.0,
        dietary_pref=DietaryPreference.HIGH_PROTEIN,
        meal_type=MealType.LUNCH,
        max_prep_time_mins=20,
    )
    # Force offline fallback by passing None or invalid key
    recipe = generate_high_protein_meal(req, api_key="dummy_key_not_real")

    assert isinstance(recipe, RecipeModel)
    assert recipe.protein_g > 30.0
    assert recipe.calories > 250.0
    assert len(recipe.ingredients) > 0
    assert len(recipe.instructions) > 0
    assert recipe.prep_time_minutes <= 25
    assert len(recipe.affiliate_supplements) > 0


def test_vegan_dietary_preference_fallback():
    req = MealPlanRequest(
        target_protein_g=40.0,
        target_calories=400.0,
        dietary_pref=DietaryPreference.VEGAN,
        meal_type=MealType.LUNCH,
        max_prep_time_mins=25,
    )
    recipe = generate_high_protein_meal(req, api_key="")
    assert isinstance(recipe, RecipeModel)
    assert recipe.protein_g >= 30.0


def test_affiliate_supplement_catalog():
    assert "creatine" in AFFILIATE_CATALOG
    assert "whey_isolate" in AFFILIATE_CATALOG
    assert "electrolytes" in AFFILIATE_CATALOG
    assert "omega3" in AFFILIATE_CATALOG

    creatine = AFFILIATE_CATALOG["creatine"]
    assert "Monohydrate" in creatine.name
    assert "5g" in creatine.suggested_dose
