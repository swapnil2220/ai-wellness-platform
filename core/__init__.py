"""Core logic package for AI Wellness & High-Protein Platform."""
from core.protein_engine import (
    Gender,
    ActivityLevel,
    FitnessGoal,
    UserProfileInput,
    MacroTargets,
    calculate_bmr,
    calculate_tdee,
    calculate_macro_targets,
)
from core.meal_planner import (
    DietaryPreference,
    MealType,
    MealPlanRequest,
    RecipeModel,
    generate_high_protein_meal,
)
from core.book_rag import (
    BookRAGSystem,
    BookInsight,
    ReflectionResponse,
)

__all__ = [
    "Gender",
    "ActivityLevel",
    "FitnessGoal",
    "UserProfileInput",
    "MacroTargets",
    "calculate_bmr",
    "calculate_tdee",
    "calculate_macro_targets",
    "DietaryPreference",
    "MealType",
    "MealPlanRequest",
    "RecipeModel",
    "generate_high_protein_meal",
    "BookRAGSystem",
    "BookInsight",
    "ReflectionResponse",
]
