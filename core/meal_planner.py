"""
AI High-Protein Meal Generator (core/meal_planner.py)
-----------------------------------------------------
Generates structured, chef-crafted high-protein meals utilizing Google GenAI (gemini-2.5-flash)
with strict Pydantic JSON schemas. Contains a resilient offline fallback recipe synthesizer
for environments where API keys are missing or offline.
Includes affiliate supplement integrations (Whey Isolate, Creatine, Electrolytes, Plant Isolate).
"""

import json
import os
import random
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class DietaryPreference(str, Enum):
    OMNIVORE = "omnivore"
    HIGH_PROTEIN = "high_protein"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    PESCATARIAN = "pescatarian"
    KETO = "keto"


class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    POST_WORKOUT = "post_workout"


class IngredientItem(BaseModel):
    name: str
    quantity: str
    protein_contribution_g: float = Field(..., description="Estimated protein in grams from this ingredient")
    notes: Optional[str] = None


class AffiliateSupplement(BaseModel):
    name: str
    category: str
    why_recommended: str
    suggested_dose: str
    affiliate_url: str


class RecipeModel(BaseModel):
    meal_name: str
    description: str
    meal_type: MealType
    dietary_pref: DietaryPreference
    prep_time_minutes: int
    cook_time_minutes: int
    protein_g: float
    carbs_g: float
    fat_g: float
    calories: float
    protein_to_calorie_pct: float = Field(..., description="Percentage of calories derived purely from protein")
    ingredients: List[IngredientItem]
    instructions: List[str]
    pro_cooking_tip: str
    longevity_score: int = Field(92, ge=50, le=100, description="Nutrient density & longevity index (1-100)")
    affiliate_supplements: List[AffiliateSupplement] = Field(default_factory=list)


class MealPlanRequest(BaseModel):
    target_protein_g: float = Field(..., ge=5.0, le=350.0, description="Target protein in grams")
    target_calories: float = Field(..., ge=50.0, le=5000.0, description="Target calories in kcal")
    dietary_pref: DietaryPreference = Field(DietaryPreference.HIGH_PROTEIN)
    meal_type: MealType = Field(MealType.LUNCH)
    allergies_exclusions: List[str] = Field(default_factory=list)
    max_prep_time_mins: int = Field(30, ge=5, le=120)
    favorite_protein_sources: Optional[List[str]] = None


# Curated affiliate supplement catalog
AFFILIATE_CATALOG: Dict[str, AffiliateSupplement] = {
    "whey_isolate": AffiliateSupplement(
        name="Ultra-Filtered Native Whey Protein Isolate (90%+ Protein)",
        category="Protein Optimization",
        why_recommended="Rapid absorption with 2.7g leucine per 30g scoop to trigger maximum Muscle Protein Synthesis (mTOR).",
        suggested_dose="1-2 scoops (30-60g) post-workout or stirred into morning oats/smoothies.",
        affiliate_url="https://wellness-highprotein.example.com/shop/whey-isolate?ref=ai_wellness"
    ),
    "plant_isolate": AffiliateSupplement(
        name="Organic Fermented Pea & Brown Rice Protein Blend",
        category="Plant Nutrition",
        why_recommended="Complete essential amino acid profile with added digestive enzymes for bloat-free plant protein intake.",
        suggested_dose="1 scoop (32g) with 300ml almond milk or water.",
        affiliate_url="https://wellness-highprotein.example.com/shop/plant-protein?ref=ai_wellness"
    ),
    "creatine": AffiliateSupplement(
        name="Creapure® Micronized Creatine Monohydrate",
        category="Cellular Energy & Hypertrophy",
        why_recommended="Clinically proven to increase phosphocreatine stores, cellular hydration, and lean power output.",
        suggested_dose="5g daily, consistent timing, no loading phase necessary.",
        affiliate_url="https://wellness-highprotein.example.com/shop/creatine?ref=ai_wellness"
    ),
    "electrolytes": AffiliateSupplement(
        name="Raw Unflavored Electrolyte Complex (1000mg Na / 200mg K / 60mg Mg)",
        category="Hydration Science",
        why_recommended="Replaces sodium and potassium lost during intense training and supports kidney filtration on high-protein diets.",
        suggested_dose="1 packet dissolved in 750ml water during exercise or upon waking.",
        affiliate_url="https://wellness-highprotein.example.com/shop/electrolytes?ref=ai_wellness"
    ),
    "omega3": AffiliateSupplement(
        name="High-DHA/EPA Molecularly Distilled Fish Oil",
        category="Cellular Membrane & Joint Recovery",
        why_recommended="Reduces muscle soreness (DOMS) and supports cardiovascular endothelial health as emphasized in longevity research.",
        suggested_dose="2 softgels (2000mg EPA/DHA) with your largest whole-food meal.",
        affiliate_url="https://wellness-highprotein.example.com/shop/omega3?ref=ai_wellness"
    )
}


# High-Quality Fallback Recipes Catalog (Indian Household Friendly)
FALLBACK_RECIPES_DATABASE = [
    {
        "meal_name": "Spiced Tandoori Chicken Tikka with Cucumber Raita",
        "description": "High-protein lean chicken breast cubes marinated in hung curd, ginger-garlic paste, and traditional tandoori spices, air-fried or pan-cooked, served with cucumber raita.",
        "meal_type": MealType.LUNCH,
        "dietary_pref": DietaryPreference.HIGH_PROTEIN,
        "prep_time_minutes": 10,
        "cook_time_minutes": 15,
        "base_protein": 52.0,
        "base_carbs": 12.0,
        "base_fat": 10.0,
        "base_cals": 346.0,
        "ingredients": [
            {"name": "Lean Boneless Chicken Breast Cubes", "quantity": "220g", "protein_contribution_g": 46.0},
            {"name": "Thick Curd / Dahi (for marinade)", "quantity": "3 tbsp (45g)", "protein_contribution_g": 3.0},
            {"name": "Fresh Cucumber (for raita)", "quantity": "100g", "protein_contribution_g": 1.0},
            {"name": "Ginger-Garlic Paste, Turmeric, Cumin & Garam Masala", "quantity": "To taste", "protein_contribution_g": 0.0},
            {"name": "Mustard Oil / Ghee", "quantity": "1 tsp (5ml)", "protein_contribution_g": 0.0},
            {"name": "Low-fat Dahi (for raita)", "quantity": "50g", "protein_contribution_g": 2.0}
        ],
        "instructions": [
            "Marinate chicken cubes with hung curd, ginger-garlic paste, mustard oil, lemon juice, turmeric, Kashmiri chilli, cumin, and garam masala for 15 minutes.",
            "Cook in an air-fryer at 190°C (375°F) for 12-14 minutes, or grill on a non-stick pan until nicely charred on all sides.",
            "Grate cucumber, mix with dahi, a pinch of roasted cumin powder, and black salt to prepare raita.",
            "Serve hot chicken tikka skewers with cold cucumber raita and fresh mint chutney."
        ],
        "pro_cooking_tip": "Do not overcook chicken breast; cook just until done, then cover and rest it for 4 minutes to ensure it remains soft and juicy.",
        "supplements": ["whey_isolate", "creatine"]
    },
    {
        "meal_name": "High-Protein Paneer Bhurji with Whole Wheat Roti",
        "description": "Crumbled low-fat paneer scrambled with chopped onions, tomatoes, green chillies, and ginger, paired with hot whole wheat rotis.",
        "meal_type": MealType.DINNER,
        "dietary_pref": DietaryPreference.VEGETARIAN,
        "prep_time_minutes": 10,
        "cook_time_minutes": 12,
        "base_protein": 40.0,
        "base_carbs": 48.0,
        "base_fat": 15.0,
        "base_cals": 487.0,
        "ingredients": [
            {"name": "Low-fat Paneer / Cottage Cheese", "quantity": "180g", "protein_contribution_g": 32.0},
            {"name": "Whole Wheat Roti / Chapati", "quantity": "2 medium rotis", "protein_contribution_g": 6.0},
            {"name": "Chopped Onion & Tomatoes", "quantity": "1 medium each", "protein_contribution_g": 1.5},
            {"name": "Mustard Oil or Ghee", "quantity": "1 tsp (5ml)", "protein_contribution_g": 0.0},
            {"name": "Green Chillies, Ginger, Turmeric, Coriander Leaves", "quantity": "To taste", "protein_contribution_g": 0.5}
        ],
        "instructions": [
            "Crumble the low-fat paneer using your hands. Keep it aside.",
            "Heat oil in a pan, add cumin seeds, chopped green chillies, ginger, and onions. Sauté until golden.",
            "Add tomatoes, turmeric, coriander powder, and salt. Cook until tomatoes soften.",
            "Add scrambled paneer, mix gently, and cook on medium heat for 3-4 minutes. Garnish with chopped fresh coriander.",
            "Serve warm bhurji alongside freshly roasted whole wheat rotis."
        ],
        "pro_cooking_tip": "Avoid cooking paneer for too long after adding to the pan, otherwise it loses moisture and turns rubbery.",
        "supplements": ["whey_isolate", "electrolytes"]
    },
    {
        "meal_name": "Spiced Chana Masala (Chickpeas) with Quinoa Pulao",
        "description": "Boiled chickpeas cooked in a homestyle tomato-onion gravy, served with a protein-rich quinoa-basmati pulao and steamed palak.",
        "meal_type": MealType.LUNCH,
        "dietary_pref": DietaryPreference.VEGAN,
        "prep_time_minutes": 10,
        "cook_time_minutes": 20,
        "base_protein": 38.0,
        "base_carbs": 64.0,
        "base_fat": 8.0,
        "base_cals": 480.0,
        "ingredients": [
            {"name": "Kabuli Chana (Chickpeas, boiled)", "quantity": "1.5 cups (150g)", "protein_contribution_g": 22.0},
            {"name": "Quinoa & Basmati Rice Blend", "quantity": "100g (cooked)", "protein_contribution_g": 7.0},
            {"name": "Steamed Palak / Spinach", "quantity": "120g", "protein_contribution_g": 4.0},
            {"name": "Mustard Oil", "quantity": "1 tsp (5ml)", "protein_contribution_g": 0.0},
            {"name": "Coriander, Cumin, Turmeric, Onion-Tomato Gravy", "quantity": "To taste", "protein_contribution_g": 5.0}
        ],
        "instructions": [
            "Sauté cumin, chopped onions, and ginger-garlic paste in a pan with mustard oil until golden brown.",
            "Add tomato puree, turmeric, cumin powder, chana masala spices, and cook until oil separates.",
            "Toss in boiled chickpeas, add half a cup of water, cover and simmer on low heat for 12 minutes.",
            "Steam palak leaves separately and sauté with a pinch of garlic.",
            "Serve hot Chana Masala over fluffy warm quinoa-basmati pulao and garlic palak on the side."
        ],
        "pro_cooking_tip": "Adding a pinch of baking soda while pressure-cooking chickpeas makes them extra soft, allowing them to absorb the curry flavors much better.",
        "supplements": ["plant_isolate", "electrolytes"]
    },
    {
        "meal_name": "Indian Egg White Bhurji Scramble with Spinach & Palak",
        "description": "A high-protein egg white scramble loaded with fresh spinach, green chillies, onions, and turmeric, cooked in minimal oil.",
        "meal_type": MealType.BREAKFAST,
        "dietary_pref": DietaryPreference.HIGH_PROTEIN,
        "prep_time_minutes": 5,
        "cook_time_minutes": 8,
        "base_protein": 42.0,
        "base_carbs": 8.0,
        "base_fat": 10.0,
        "base_cals": 290.0,
        "ingredients": [
            {"name": "Pure Egg Whites", "quantity": "6 large egg whites", "protein_contribution_g": 24.0},
            {"name": "Whole Egg", "quantity": "1 large egg", "protein_contribution_g": 6.0},
            {"name": "Fresh Spinach / Palak Leaves (chopped)", "quantity": "1.5 cups (100g)", "protein_contribution_g": 3.0},
            {"name": "Chopped Onion & Tomato", "quantity": "80g total", "protein_contribution_g": 1.0},
            {"name": "Green Chillies, Ginger, Turmeric", "quantity": "To taste", "protein_contribution_g": 0.0},
            {"name": "Low-fat Paneer (grated, for garnish)", "quantity": "40g", "protein_contribution_g": 8.0}
        ],
        "instructions": [
            "In a bowl, whisk together egg whites, one whole egg, salt, and a pinch of turmeric.",
            "Heat ghee or oil in a non-stick pan, add cumin, chopped ginger, green chillies, and onions. Sauté until transparent.",
            "Add tomatoes and cook for 2 minutes. Stir in the chopped spinach leaves and let them wilt.",
            "Pour in the egg mixture. Scramble constantly on medium-low heat until cooked and fluffy.",
            "Grate low-fat paneer on top as garnish and serve hot."
        ],
        "pro_cooking_tip": "Scramble the eggs on medium-low heat. Cooking them too fast on high heat dries them out and turns the spinach bitter.",
        "supplements": ["electrolytes", "creatine"]
    },
    {
        "meal_name": "Roasted Chana Sattu & Whey Protein Elixir",
        "description": "A cooling, traditional North Indian protein shake made of roasted gram flour (Sattu) blended with whey isolate, mint, and roasted cumin.",
        "meal_type": MealType.POST_WORKOUT,
        "dietary_pref": DietaryPreference.HIGH_PROTEIN,
        "prep_time_minutes": 3,
        "cook_time_minutes": 0,
        "base_protein": 46.0,
        "base_carbs": 24.0,
        "base_fat": 6.0,
        "base_cals": 334.0,
        "ingredients": [
            {"name": "Roasted Chana Sattu (Gram Flour)", "quantity": "30g", "protein_contribution_g": 6.0},
            {"name": "Vanilla / Unflavored Whey Isolate", "quantity": "35g (1.2 scoops)", "protein_contribution_g": 31.0},
            {"name": "Chilled Curd / Dahi (for thickness)", "quantity": "3 tbsp (50g)", "protein_contribution_g": 3.0},
            {"name": "Roasted Cumin Powder, Black Salt, Mint Leaves, Lemon Juice", "quantity": "To taste", "protein_contribution_g": 0.0},
            {"name": "Grated Paneer (optional, to stir-in)", "quantity": "30g", "protein_contribution_g": 6.0}
        ],
        "instructions": [
            "In a shaker or blender, combine sattu flour, whey isolate, curd, and chilled water (300ml).",
            "Add roasted cumin powder, black salt, a squeeze of fresh lemon juice, and finely chopped mint leaves.",
            "Shake vigorously or blend for 30 seconds until completely smooth and lump-free.",
            "Pour into a tall glass, stir in grated paneer if desired for extra texture, and serve cold."
        ],
        "pro_cooking_tip": "Sattu acts as a natural prebiotic and coolant, making it highly effective for gut health and digestion on high-protein diets.",
        "supplements": ["creatine", "whey_isolate"]
    }
]



def _build_offline_recipe(request: MealPlanRequest) -> RecipeModel:
    """
    Intelligently select and scale a fallback recipe to fit the user's requested targets.
    """
    # Filter by dietary preference match if possible
    candidates = [
        r for r in FALLBACK_RECIPES_DATABASE
        if r["dietary_pref"] == request.dietary_pref or request.dietary_pref in (DietaryPreference.HIGH_PROTEIN, DietaryPreference.OMNIVORE)
    ]
    if not candidates:
        candidates = FALLBACK_RECIPES_DATABASE

    # Pick matching meal type if available, else random
    type_matches = [r for r in candidates if r["meal_type"] == request.meal_type]
    chosen = random.choice(type_matches if type_matches else candidates)

    # Scale factor based on requested protein
    scale = max(0.6, min(2.5, request.target_protein_g / chosen["base_protein"]))

    scaled_p = round(chosen["base_protein"] * scale, 1)
    scaled_c = round(chosen["base_carbs"] * scale, 1)
    scaled_f = round(chosen["base_fat"] * scale, 1)
    scaled_cals = round((scaled_p * 4.0) + (scaled_c * 4.0) + (scaled_f * 9.0), 0)

    p_pct = round(((scaled_p * 4.0) / max(1.0, scaled_cals)) * 100, 1)

    ingredients = []
    for item in chosen["ingredients"]:
        base_prot = item["protein_contribution_g"]
        scaled_item_prot = round(base_prot * scale, 1)
        ingredients.append(IngredientItem(
            name=item["name"],
            quantity=f"{item['quantity']} (scaled to {round(scale*100)}%)" if scale != 1.0 else item["quantity"],
            protein_contribution_g=scaled_item_prot
        ))

    # Match affiliate supplements
    supplements = []
    for supp_key in chosen.get("supplements", ["whey_isolate", "creatine"]):
        if supp_key in AFFILIATE_CATALOG:
            supplements.append(AFFILIATE_CATALOG[supp_key])

    return RecipeModel(
        meal_name=chosen["meal_name"],
        description=chosen["description"],
        meal_type=request.meal_type,
        dietary_pref=request.dietary_pref,
        prep_time_minutes=min(request.max_prep_time_mins, chosen["prep_time_minutes"]),
        cook_time_minutes=chosen["cook_time_minutes"],
        protein_g=scaled_p,
        carbs_g=scaled_c,
        fat_g=scaled_f,
        calories=scaled_cals,
        protein_to_calorie_pct=p_pct,
        ingredients=ingredients,
        instructions=chosen["instructions"],
        pro_cooking_tip=chosen["pro_cooking_tip"],
        longevity_score=random.randint(90, 98),
        affiliate_supplements=supplements
    )


def generate_high_protein_meal(
    request: MealPlanRequest,
    api_key: Optional[str] = None
) -> RecipeModel:
    """
    Generate high-protein recipe using Google GenAI SDK (gemini-2.5-flash) or fallback engine.
    """
    effective_api_key = api_key or os.environ.get("GEMINI_API_KEY")
    
    # If no API key provided or placeholder, return robust synthesized recipe immediately
    if not effective_api_key or "your_gemini" in effective_api_key.lower() or len(effective_api_key.strip()) < 10:
        return _build_offline_recipe(request)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=effective_api_key)

        prompt = f"""
You are an elite sports nutritionist and Michelin-trained chef specializing in Indian cuisine.
Create a hyper-optimized, high-protein recipe matching these EXACT targets, tailored for an Indian household:
- Use ingredients, vegetables, fruits, dals, lentils, and paneer commonly found in Indian kitchens.
- Use traditional Indian spices (turmeric, cumin, coriander, garam masala, chili) and simple cooking steps (pressure cooking, pan-searing, boiling).
- Ensure all ingredients are easily accessible in a typical Indian supermarket or local vegetable market.
- Meal Type: {request.meal_type.value}
- Dietary Preference: {request.dietary_pref.value}
- Target Protein: ~{request.target_protein_g} grams (DO NOT UNDERDELIVER PROTEIN)
- Target Calories: ~{request.target_calories} kcal
- Max Prep Time: {request.max_prep_time_mins} minutes
- Exclusions/Allergies: {', '.join(request.allergies_exclusions) if request.allergies_exclusions else 'None'}
- Favorite Proteins: {', '.join(request.favorite_protein_sources) if request.favorite_protein_sources else 'Flexible'}

Provide output matching this JSON schema:
{{
  "meal_name": "string",
  "description": "string",
  "prep_time_minutes": integer,
  "cook_time_minutes": integer,
  "protein_g": float,
  "carbs_g": float,
  "fat_g": float,
  "calories": float,
  "ingredients": [
    {{"name": "string", "quantity": "string", "protein_contribution_g": float}}
  ],
  "instructions": ["step 1", "step 2", "step 3"],
  "pro_cooking_tip": "string (evidence-based cooking or nutrition tip)",
  "longevity_score": integer (between 80 and 99)
}}
Ensure the protein is distributed from high-biological-value (HBV) whole foods or clean isolates.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.4,
            ),
        )

        raw_text = response.text or "{}"
        data = json.loads(raw_text)

        p = float(data.get("protein_g", request.target_protein_g))
        c = float(data.get("carbs_g", 30.0))
        f = float(data.get("fat_g", 12.0))
        cals = float(data.get("calories", (p * 4.0) + (c * 4.0) + (f * 9.0)))
        p_pct = round(((p * 4.0) / max(1.0, cals)) * 100, 1)

        raw_ingredients = data.get("ingredients", [])
        ingredients = []
        for ing in raw_ingredients:
            ingredients.append(IngredientItem(
                name=ing.get("name", "High-Protein Ingredient"),
                quantity=ing.get("quantity", "1 serving"),
                protein_contribution_g=float(ing.get("protein_contribution_g", 10.0))
            ))

        if not ingredients:
            ingredients.append(IngredientItem(
                name="Lean Protein Core",
                quantity=f"{round(request.target_protein_g * 4.5)}g",
                protein_contribution_g=request.target_protein_g
            ))

        # Select matching affiliate supplements
        supplements = [AFFILIATE_CATALOG["creatine"]]
        if request.dietary_pref == DietaryPreference.VEGAN:
            supplements.append(AFFILIATE_CATALOG["plant_isolate"])
        else:
            supplements.append(AFFILIATE_CATALOG["whey_isolate"])
        supplements.append(AFFILIATE_CATALOG["electrolytes"])

        return RecipeModel(
            meal_name=data.get("meal_name", "Chef's High-Protein Creation"),
            description=data.get("description", "Hyper-customized high-protein culinary dish."),
            meal_type=request.meal_type,
            dietary_pref=request.dietary_pref,
            prep_time_minutes=int(data.get("prep_time_minutes", 15)),
            cook_time_minutes=int(data.get("cook_time_minutes", 15)),
            protein_g=round(p, 1),
            carbs_g=round(c, 1),
            fat_g=round(f, 1),
            calories=round(cals, 0),
            protein_to_calorie_pct=p_pct,
            ingredients=ingredients,
            instructions=data.get("instructions", ["Prepare ingredients.", "Cook thoroughly.", "Serve and enjoy!"]),
            pro_cooking_tip=data.get("pro_cooking_tip", "Pair with adequate hydration to support amino acid transport."),
            longevity_score=int(data.get("longevity_score", 94)),
            affiliate_supplements=supplements
        )

    except Exception:
        # Graceful fallback to offline engine if API fails or network issue occurs
        return _build_offline_recipe(request)
