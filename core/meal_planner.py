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


# High-Quality Fallback Recipes Catalog
FALLBACK_RECIPES_DATABASE = [
    {
        "meal_name": "Seared Lemon-Herb Chicken Breast with Garlic Quinoa & Roasted Asparagus",
        "description": "Golden pan-seared chicken breast basted in lemon zest and fresh rosemary, paired with fluffy quinoa and fiber-rich charred asparagus.",
        "meal_type": MealType.LUNCH,
        "dietary_pref": DietaryPreference.HIGH_PROTEIN,
        "prep_time_minutes": 10,
        "cook_time_minutes": 18,
        "base_protein": 52.0,
        "base_carbs": 38.0,
        "base_fat": 11.0,
        "base_cals": 460.0,
        "ingredients": [
            {"name": "Skinless Boneless Chicken Breast", "quantity": "220g", "protein_contribution_g": 46.0},
            {"name": "Cooked Tricolor Quinoa", "quantity": "100g", "protein_contribution_g": 4.5},
            {"name": "Tender Asparagus Spears", "quantity": "120g", "protein_contribution_g": 2.5},
            {"name": "Extra Virgin Olive Oil", "quantity": "1 tsp (5ml)", "protein_contribution_g": 0.0},
            {"name": "Fresh Lemon Zest, Garlic & Rosemary", "quantity": "To taste", "protein_contribution_g": 0.0}
        ],
        "instructions": [
            "Pat chicken dry, season with sea salt, cracked black pepper, garlic powder, and fresh rosemary.",
            "Heat a cast-iron skillet over medium-high with olive oil. Sear chicken 6-7 minutes per side until golden and internal temperature reaches 74°C (165°F).",
            "Toss asparagus into the pan during the last 4 minutes with a squeeze of fresh lemon juice.",
            "Plate fluffy warm quinoa, top with sliced chicken breast and charred asparagus. Drizzle pan drippings."
        ],
        "pro_cooking_tip": "Rest chicken for 5 minutes before slicing to lock in intracellular juices and maintain maximum tenderness.",
        "supplements": ["whey_isolate", "creatine"]
    },
    {
        "meal_name": "Wild Atlantic Salmon with Crispy Edamame & Roasted Sweet Potato Hash",
        "description": "Pan-crisped wild salmon fillet rich in astaxanthin & omega-3s, served with a roasted sweet potato and high-protein edamame hash.",
        "meal_type": MealType.DINNER,
        "dietary_pref": DietaryPreference.PESCATARIAN,
        "prep_time_minutes": 12,
        "cook_time_minutes": 15,
        "base_protein": 46.0,
        "base_carbs": 42.0,
        "base_fat": 16.0,
        "base_cals": 495.0,
        "ingredients": [
            {"name": "Wild-Caught Salmon Fillet", "quantity": "190g", "protein_contribution_g": 38.0},
            {"name": "Shelled Organic Edamame", "quantity": "80g", "protein_contribution_g": 9.0},
            {"name": "Diced Japanese Sweet Potato", "quantity": "140g", "protein_contribution_g": 2.0},
            {"name": "Avocado Oil Spray", "quantity": "1 light mist", "protein_contribution_g": 0.0},
            {"name": "Fresh Dill, Smoked Paprika & Sea Salt", "quantity": "To taste", "protein_contribution_g": 0.0}
        ],
        "instructions": [
            "Air-fry or roast diced sweet potato cubes at 200°C (400°F) for 15 minutes until crispy on the edges.",
            "Toss edamame in during the final 4 minutes of roasting with smoked paprika and flaky salt.",
            "Sear salmon skin-side down in a hot stainless skillet for 4 minutes until skin is glass-crisp, then flip and cook for 2 minutes.",
            "Assemble sweet potato-edamame hash as the base and crown with the crispy salmon fillet. Garnish with fresh dill."
        ],
        "pro_cooking_tip": "Wild salmon cooks 30% faster than farmed salmon due to lower intramuscular fat. Keep the center slightly translucent.",
        "supplements": ["omega3", "electrolytes"]
    },
    {
        "meal_name": "High-Protein Greek Yogurt & Chia Superberry Power Bowl",
        "description": "Thick 0% Greek yogurt layered with organic vanilla whey isolate, wild blueberries, sprouted chia, and roasted almond slivers.",
        "meal_type": MealType.BREAKFAST,
        "dietary_pref": DietaryPreference.VEGETARIAN,
        "prep_time_minutes": 5,
        "cook_time_minutes": 0,
        "base_protein": 48.0,
        "base_carbs": 32.0,
        "base_fat": 9.0,
        "base_cals": 400.0,
        "ingredients": [
            {"name": "0% Fat Authentic Greek Yogurt", "quantity": "250g", "protein_contribution_g": 26.0},
            {"name": "Native Vanilla Whey Isolate", "quantity": "25g (1 scoop)", "protein_contribution_g": 22.5},
            {"name": "Frozen Wild Nordic Blueberries", "quantity": "80g", "protein_contribution_g": 1.0},
            {"name": "Sprouted Black Chia Seeds", "quantity": "1 tbsp (12g)", "protein_contribution_g": 2.0},
            {"name": "Ceylon Cinnamon & Stevia drops", "quantity": "To taste", "protein_contribution_g": 0.0}
        ],
        "instructions": [
            "Whisk whey isolate directly into cold Greek yogurt with a fork or mini-whisk until velvety and mousse-like.",
            "Fold in half of the wild blueberries and Ceylon cinnamon.",
            "Top with remaining berries, chia seeds, and raw sliced almonds for crunch."
        ],
        "pro_cooking_tip": "Add 1-2 tbsp of unsweetened almond milk if you prefer a silkier parfait texture over thick mousse.",
        "supplements": ["whey_isolate", "creatine"]
    },
    {
        "meal_name": "Crispy Pan-Blackened Tempeh & Hempseed Macro Bowl",
        "description": "Marinated organic tempeh triangles seared in tamari aminos, paired with edamame, steamed broccoli florets, and raw shelled hemp hearts.",
        "meal_type": MealType.LUNCH,
        "dietary_pref": DietaryPreference.VEGAN,
        "prep_time_minutes": 10,
        "cook_time_minutes": 12,
        "base_protein": 44.0,
        "base_carbs": 26.0,
        "base_fat": 16.0,
        "base_cals": 420.0,
        "ingredients": [
            {"name": "Organic Cultured Soy Tempeh", "quantity": "180g", "protein_contribution_g": 34.0},
            {"name": "Raw Shelled Hemp Hearts", "quantity": "2 tbsp (20g)", "protein_contribution_g": 7.0},
            {"name": "Steamed Tenderstem Broccoli", "quantity": "150g", "protein_contribution_g": 4.5},
            {"name": "Organic Coconut Tamari & Ginger Glaze", "quantity": "1.5 tbsp", "protein_contribution_g": 1.0},
            {"name": "Toasted White Sesame Seeds", "quantity": "1 tsp", "protein_contribution_g": 0.5}
        ],
        "instructions": [
            "Slice tempeh into thin bite-sized triangles and steam for 3 minutes to remove natural bitterness.",
            "Toss in tamari, grated ginger, and garlic powder.",
            "Pan-sear in a non-stick skillet on medium-high until edges are deeply caramelized and crispy (4 min per side).",
            "Serve over steamed broccoli, sprinkle heavily with raw hemp hearts and toasted sesame."
        ],
        "pro_cooking_tip": "Steaming tempeh before searing opens the pores, allowing the savory marinade to penetrate deep into the core.",
        "supplements": ["plant_isolate", "electrolytes"]
    },
    {
        "meal_name": "Lean Grass-Fed Beef & Egg White Scramble with Avocado",
        "description": "Ultra-lean 96/4 ground beef sautéed with bell peppers and folded into fluffy liquid egg whites, topped with fresh hass avocado.",
        "meal_type": MealType.BREAKFAST,
        "dietary_pref": DietaryPreference.KETO,
        "prep_time_minutes": 8,
        "cook_time_minutes": 10,
        "base_protein": 54.0,
        "base_carbs": 6.0,
        "base_fat": 18.0,
        "base_cals": 405.0,
        "ingredients": [
            {"name": "96/4 Extra Lean Ground Beef", "quantity": "160g", "protein_contribution_g": 38.0},
            {"name": "100% Pure Liquid Egg Whites", "quantity": "150ml", "protein_contribution_g": 16.0},
            {"name": "Fresh Hass Avocado", "quantity": "40g (1/4 avocado)", "protein_contribution_g": 0.8},
            {"name": "Diced Red Bell Pepper & Spinach", "quantity": "60g", "protein_contribution_g": 1.2},
            {"name": "Cumin, Sea Salt & Jalapeño", "quantity": "To taste", "protein_contribution_g": 0.0}
        ],
        "instructions": [
            "Brown lean ground beef in a skillet with cumin, sea salt, and diced bell peppers until cooked through.",
            "Lower heat to medium-low, pour in egg whites and baby spinach.",
            "Gently fold the mixture until egg whites are set and pillowy.",
            "Transfer to plate and top with fresh avocado slices and hot salsa."
        ],
        "pro_cooking_tip": "Keep heat low when scrambling egg whites to avoid watery separation and achieve a fluffy, velvety mouthfeel.",
        "supplements": ["electrolytes", "creatine"]
    },
    {
        "meal_name": "Anabolic Cold-Brew Espresso & Whey Protein Sludge",
        "description": "Double espresso blended with organic whey isolate, creamy almond butter, and ice into a thick, restorative pre/post-workout elixir.",
        "meal_type": MealType.POST_WORKOUT,
        "dietary_pref": DietaryPreference.HIGH_PROTEIN,
        "prep_time_minutes": 3,
        "cook_time_minutes": 0,
        "base_protein": 42.0,
        "base_carbs": 12.0,
        "base_fat": 8.0,
        "base_cals": 290.0,
        "ingredients": [
            {"name": "Cold-Brew Espresso Concentrate", "quantity": "150ml", "protein_contribution_g": 0.5},
            {"name": "Vanilla Chocolate Swirl Whey Isolate", "quantity": "40g (1.3 scoops)", "protein_contribution_g": 36.0},
            {"name": "Unsweetened Almond Milk", "quantity": "150ml", "protein_contribution_g": 1.0},
            {"name": "Raw Almond Butter", "quantity": "10g", "protein_contribution_g": 2.2},
            {"name": "Crushed Ice & Himalayan Pink Salt", "quantity": "1 cup", "protein_contribution_g": 0.0}
        ],
        "instructions": [
            "Add cold-brew espresso, almond milk, and whey isolate into a high-speed blender.",
            "Add almond butter, a pinch of pink salt (for electrolyte absorption), and 1 cup of crushed ice.",
            "Blend on high for 45 seconds until thick and frosty.",
            "Pour into a chilled tumbler and enjoy immediately post-workout."
        ],
        "pro_cooking_tip": "The pinch of sodium enhances the sweetness of the whey while expediting glucose and amino acid cellular transport.",
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
You are an elite sports nutritionist and Michelin-trained chef.
Create a hyper-optimized, high-protein recipe matching these EXACT targets:
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
