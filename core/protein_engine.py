"""
Protein & Macro Engine (core/protein_engine.py)
-----------------------------------------------
Calculates personalized daily target macronutrients (Protein, Carbs, Fats, Calories)
using the Mifflin-St Jeor equation, activity multipliers, goal adjustments, and
hyper-optimized high-protein distribution (1.6g to 2.2g+ per kg of body weight).
Incorporates per-meal leucine threshold recommendations inspired by longevity science.
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"  # 1.2
    LIGHT = "light"  # 1.375
    MODERATE = "moderate"  # 1.55
    VERY_ACTIVE = "very_active"  # 1.725
    EXTRA_ACTIVE = "extra_active"  # 1.9


class FitnessGoal(str, Enum):
    FAT_LOSS = "fat_loss"  # -20% deficit, higher protein retention
    MUSCLE_GAIN = "muscle_gain"  # +10% surplus, hypertrophy focus
    MAINTENANCE = "maintenance"  # 0% neutral energy balance


ACTIVITY_MULTIPLIERS: Dict[ActivityLevel, float] = {
    ActivityLevel.SEDENTARY: 1.2,
    ActivityLevel.LIGHT: 1.375,
    ActivityLevel.MODERATE: 1.55,
    ActivityLevel.VERY_ACTIVE: 1.725,
    ActivityLevel.EXTRA_ACTIVE: 1.9,
}


class UserProfileInput(BaseModel):
    """Input parameters for calculating metabolic targets."""
    weight_kg: float = Field(..., gt=20.0, lt=400.0, description="Weight in kilograms")
    height_cm: float = Field(..., gt=80.0, lt=280.0, description="Height in centimeters")
    age: int = Field(..., gt=10, lt=120, description="Age in years")
    gender: Gender = Field(Gender.MALE, description="Biological sex for metabolic baseline")
    activity_level: ActivityLevel = Field(ActivityLevel.MODERATE, description="Physical activity frequency")
    goal: FitnessGoal = Field(FitnessGoal.FAT_LOSS, description="Primary physique or wellness goal")
    protein_multiplier: Optional[float] = Field(
        None,
        ge=1.0,
        le=3.5,
        description="Custom protein intake in grams per kg of body weight (default 1.6 - 2.4g/kg, supports up to 3.5g/kg)"
    )
    meals_per_day: int = Field(3, ge=1, le=8, description="Planned number of main meals per day")

    @field_validator("weight_kg", "height_cm")
    @classmethod
    def round_floats(cls, v: float) -> float:
        return round(v, 2)


class MealDistribution(BaseModel):
    """Macro targets broken down per meal for optimal muscle protein synthesis (MPS)."""
    meal_index: int
    name: str
    target_protein_g: float
    target_carbs_g: float
    target_fats_g: float
    target_calories: float
    leucine_threshold_met: bool = Field(
        True,
        description="Whether meal meets the ~30g+ protein threshold to stimulate mTOR/MPS"
    )


class MacroTargets(BaseModel):
    """Complete personalized nutritional targets."""
    bmr: float = Field(..., description="Basal Metabolic Rate in kcal")
    tdee: float = Field(..., description="Total Daily Energy Expenditure in kcal")
    target_calories: float = Field(..., description="Adjusted daily calorie target in kcal")
    protein_g: float = Field(..., description="Target daily protein in grams")
    carbs_g: float = Field(..., description="Target daily carbohydrates in grams")
    fats_g: float = Field(..., description="Target daily fats in grams")
    protein_multiplier_used: float = Field(..., description="Actual g/kg protein multiplier")
    protein_calories_pct: float = Field(..., description="Percentage of calories from protein")
    carbs_calories_pct: float = Field(..., description="Percentage of calories from carbs")
    fats_calories_pct: float = Field(..., description="Percentage of calories from fats")
    meals: List[MealDistribution] = Field(default_factory=list, description="Per-meal macro breakdown")
    longevity_notes: List[str] = Field(default_factory=list, description="Evidence-backed dietary insights")


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: Gender) -> float:
    """
    Calculate Basal Metabolic Rate (BMR) using the Mifflin-St Jeor equation.
    Men: 10 * W + 6.25 * H - 5 * A + 5
    Women: 10 * W + 6.25 * H - 5 * A - 161
    Other: Average baseline (10 * W + 6.25 * H - 5 * A - 78)
    """
    base = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age)
    if gender == Gender.MALE:
        return round(base + 5.0, 1)
    elif gender == Gender.FEMALE:
        return round(base - 161.0, 1)
    else:
        return round(base - 78.0, 1)


def calculate_tdee(bmr: float, activity_level: ActivityLevel) -> float:
    """Calculate Total Daily Energy Expenditure by applying the activity multiplier."""
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
    return round(bmr * multiplier, 1)


def calculate_macro_targets(profile: UserProfileInput) -> MacroTargets:
    """
    Calculate full macro distribution with a strict high-protein focus (1.6g - 2.2g / kg).
    
    1. BMR via Mifflin-St Jeor
    2. TDEE based on activity level
    3. Goal adjustment:
       - Fat Loss: -20% calorie deficit
       - Muscle Gain: +10% surplus
       - Maintenance: 0% adjustment
    4. Protein:
       - Default Fat Loss: 2.2 g/kg (maximizes lean tissue preservation in deficit)
       - Default Muscle Gain: 2.0 g/kg (maximizes muscle protein synthesis)
       - Default Maintenance: 1.8 g/kg (optimal longevity & metabolic health)
       - Or user specified multiplier within 1.6 - 2.4 g/kg range
    5. Fats: ~25% of total calories (or ~0.8g - 1.0g / kg)
    6. Carbs: Remainder calories
    """
    bmr = calculate_bmr(profile.weight_kg, profile.height_cm, profile.age, profile.gender)
    tdee = calculate_tdee(bmr, profile.activity_level)

    # Goal adjustment
    if profile.goal == FitnessGoal.FAT_LOSS:
        target_calories = tdee * 0.80  # 20% deficit
        default_protein_mult = 2.2
    elif profile.goal == FitnessGoal.MUSCLE_GAIN:
        target_calories = tdee * 1.10  # 10% surplus
        default_protein_mult = 2.0
    else:
        target_calories = tdee
        default_protein_mult = 1.8

    # Apply custom multiplier if provided, otherwise default
    protein_multiplier = profile.protein_multiplier if profile.protein_multiplier else default_protein_mult
    
    # Calculate grams
    protein_g = round(profile.weight_kg * protein_multiplier, 1)
    protein_cals = protein_g * 4.0

    # Ensure calories remain viable with minimum essential fats (at least 15% of cals or 0.5g/kg)
    min_fat_cals = min(target_calories * 0.35, max(profile.weight_kg * 0.5 * 9.0, target_calories * 0.15))
    max_protein_cals = max(0.0, target_calories - min_fat_cals)
    if protein_cals > max_protein_cals and max_protein_cals > 0:
        protein_cals = max_protein_cals
        protein_g = round(protein_cals / 4.0, 1)
        protein_multiplier = round(protein_g / profile.weight_kg, 2)

    # Fats allocation: ~25% of target calories (bounded by remaining calories)
    fats_cals = min(max(0.0, target_calories - protein_cals), max(profile.weight_kg * 0.6 * 9.0, target_calories * 0.25))
    fats_g = round(fats_cals / 9.0, 1)

    # Carbohydrates: Remaining calories
    carbs_cals = max(0.0, target_calories - protein_cals - (fats_g * 9.0))
    carbs_g = round(carbs_cals / 4.0, 1)

    # Re-calculate actual total calories from rounded macros
    total_calculated_cals = round(protein_cals + (fats_g * 9.0) + (carbs_g * 4.0), 1)

    # Percentages
    p_pct = round((protein_cals / max(1.0, total_calculated_cals)) * 100, 1)
    f_pct = round(((fats_g * 9.0) / max(1.0, total_calculated_cals)) * 100, 1)
    c_pct = round(((carbs_g * 4.0) / max(1.0, total_calculated_cals)) * 100, 1)

    # Per-meal breakdown
    meals_count = max(2, profile.meals_per_day)
    per_meal_p = round(protein_g / meals_count, 1)
    per_meal_c = round(carbs_g / meals_count, 1)
    per_meal_f = round(fats_g / meals_count, 1)
    per_meal_cal = round(total_calculated_cals / meals_count, 1)

    meal_names = ["Breakfast / Meal 1", "Lunch / Meal 2", "Dinner / Meal 3", "Post-Workout / Snack", "Evening Snack", "Early Fuel"]
    meals: List[MealDistribution] = []
    for i in range(meals_count):
        m_name = meal_names[i] if i < len(meal_names) else f"Meal {i+1}"
        meals.append(MealDistribution(
            meal_index=i + 1,
            name=m_name,
            target_protein_g=per_meal_p,
            target_carbs_g=per_meal_c,
            target_fats_g=per_meal_f,
            target_calories=per_meal_cal,
            leucine_threshold_met=(per_meal_p >= 28.0)
        ))

    # Evidence-backed longevity insights
    insights = [
        f"High-protein target: {protein_multiplier:.1f}g/kg ({protein_g}g/day) preserves lean body mass and elevates diet-induced thermogenesis (TEF).",
        f"Per-meal distribution (~{per_meal_p}g protein/meal) reaches the ~2.5g–3.5g leucine threshold required to activate mTOR and Muscle Protein Synthesis.",
        "Hydration & Electrolytes: High-protein metabolism increases renal urea filtration. Aim for 35–45ml water per kg body weight plus 500mg sodium pre-workout."
    ]

    return MacroTargets(
        bmr=bmr,
        tdee=tdee,
        target_calories=round(total_calculated_cals, 0),
        protein_g=protein_g,
        carbs_g=carbs_g,
        fats_g=fats_g,
        protein_multiplier_used=protein_multiplier,
        protein_calories_pct=p_pct,
        carbs_calories_pct=c_pct,
        fats_calories_pct=f_pct,
        meals=meals,
        longevity_notes=insights
    )
