import 'dart:math';
import '../models/meal_recipe.dart';

class MealPlannerService {
  static const Map<String, AffiliateSupplement> affiliateSupplements = {
    'whey_isolate': AffiliateSupplement(
      name: 'Ultra-Filtered Native Whey Protein Isolate',
      category: 'Protein Optimization',
      whyRecommended: 'Contains 2.7g leucine per 30g scoop to trigger maximum Muscle Protein Synthesis (mTOR).',
      suggestedDose: '1-2 scoops (30-60g) post-workout or in morning oatmeal.',
      affiliateUrl: 'https://wellness-highprotein.example.com/shop/whey-isolate?ref=flutter_pulse',
    ),
    'plant_isolate': AffiliateSupplement(
      name: 'Organic Fermented Pea & Brown Rice Isolate',
      category: 'Plant Nutrition',
      whyRecommended: 'Complete essential amino acid profile with added enzymes for bloat-free plant protein absorption.',
      suggestedDose: '1 scoop (32g) with 300ml cold almond milk or water.',
      affiliateUrl: 'https://wellness-highprotein.example.com/shop/plant-protein?ref=flutter_pulse',
    ),
    'creatine': AffiliateSupplement(
      name: 'Creapure® Micronized Creatine Monohydrate',
      category: 'Cellular Energy & Hypertrophy',
      whyRecommended: 'Clinically proven to maximize phosphocreatine stores, cellular hydration, and lean power output.',
      suggestedDose: '5g daily, consistent timing, no loading phase needed.',
      affiliateUrl: 'https://wellness-highprotein.example.com/shop/creatine?ref=flutter_pulse',
    ),
    'electrolytes': AffiliateSupplement(
      name: 'Raw Unflavored Electrolyte Complex (1000mg Na)',
      category: 'Hydration Science',
      whyRecommended: 'Replaces sodium and potassium lost during training and supports kidney filtration on high-protein diets.',
      suggestedDose: '1 packet in 750ml water during exercise.',
      affiliateUrl: 'https://wellness-highprotein.example.com/shop/electrolytes?ref=flutter_pulse',
    ),
    'omega3': AffiliateSupplement(
      name: 'High-DHA/EPA Molecularly Distilled Fish Oil',
      category: 'Cellular Recovery & Longevity',
      whyRecommended: 'Reduces delayed-onset muscle soreness (DOMS) and supports endothelial flexibility.',
      suggestedDose: '2 softgels (2000mg EPA/DHA) with your largest meal.',
      affiliateUrl: 'https://wellness-highprotein.example.com/shop/omega3?ref=flutter_pulse',
    ),
  };

  static final List<Map<String, dynamic>> _catalog = [
    {
      'mealName': 'Seared Lemon-Herb Chicken Breast with Garlic Quinoa & Charred Asparagus',
      'description': 'Golden pan-seared chicken breast basted in lemon zest and fresh rosemary, paired with fluffy quinoa and charred asparagus.',
      'mealType': MealType.lunch,
      'dietaryPref': DietaryPreference.highProtein,
      'prepTimeMinutes': 10,
      'cookTimeMinutes': 18,
      'baseProtein': 52.0,
      'baseCarbs': 38.0,
      'baseFat': 11.0,
      'baseCals': 460.0,
      'ingredients': [
        {'name': 'Skinless Chicken Breast', 'quantity': '220g', 'protein_contribution_g': 46.0},
        {'name': 'Cooked Tricolor Quinoa', 'quantity': '100g', 'protein_contribution_g': 4.5},
        {'name': 'Tender Asparagus Spears', 'quantity': '120g', 'protein_contribution_g': 2.5},
        {'name': 'Extra Virgin Olive Oil', 'quantity': '1 tsp', 'protein_contribution_g': 0.0},
      ],
      'instructions': [
        'Pat chicken dry, season with sea salt, cracked black pepper, garlic powder, and fresh rosemary.',
        'Heat skillet over medium-high with olive oil. Sear chicken 6-7 minutes per side until golden (74°C / 165°F).',
        'Toss asparagus into the pan during the last 4 minutes with fresh lemon juice.',
        'Serve sliced chicken over warm fluffy quinoa with pan drippings.'
      ],
      'proCookingTip': 'Rest chicken for 5 minutes before slicing to lock in intracellular juices and maintain maximum tenderness.',
      'supplements': ['whey_isolate', 'creatine'],
    },
    {
      'mealName': 'Wild Atlantic Salmon with Crispy Edamame & Roasted Sweet Potato Hash',
      'description': 'Pan-crisped wild salmon fillet rich in astaxanthin and omega-3s, served with a roasted sweet potato and high-protein edamame hash.',
      'mealType': MealType.dinner,
      'dietaryPref': DietaryPreference.pescatarian,
      'prepTimeMinutes': 12,
      'cookTimeMinutes': 15,
      'baseProtein': 46.0,
      'baseCarbs': 42.0,
      'baseFat': 16.0,
      'baseCals': 495.0,
      'ingredients': [
        {'name': 'Wild-Caught Salmon Fillet', 'quantity': '190g', 'protein_contribution_g': 38.0},
        {'name': 'Shelled Organic Edamame', 'quantity': '80g', 'protein_contribution_g': 9.0},
        {'name': 'Diced Sweet Potato', 'quantity': '140g', 'protein_contribution_g': 2.0},
      ],
      'instructions': [
        'Air-fry diced sweet potato cubes at 200°C for 15 minutes until crispy on the edges.',
        'Toss edamame in during the final 4 minutes of roasting with smoked paprika and sea salt.',
        'Sear salmon skin-side down in a hot skillet for 4 minutes until skin is crisp, flip for 2 minutes.',
        'Assemble sweet potato-edamame hash as base and crown with crispy salmon.'
      ],
      'proCookingTip': 'Wild salmon cooks 30% faster than farmed salmon due to lower intramuscular fat. Keep center slightly translucent.',
      'supplements': ['omega3', 'electrolytes'],
    },
    {
      'mealName': 'High-Protein Greek Yogurt & Chia Superberry Power Parfait',
      'description': 'Thick 0% Greek yogurt layered with organic vanilla whey isolate, wild blueberries, sprouted chia, and roasted almond slivers.',
      'mealType': MealType.breakfast,
      'dietaryPref': DietaryPreference.vegetarian,
      'prepTimeMinutes': 5,
      'cookTimeMinutes': 0,
      'baseProtein': 48.0,
      'baseCarbs': 32.0,
      'baseFat': 9.0,
      'baseCals': 400.0,
      'ingredients': [
        {'name': '0% Authentic Greek Yogurt', 'quantity': '250g', 'protein_contribution_g': 26.0},
        {'name': 'Vanilla Whey Isolate', 'quantity': '25g (1 scoop)', 'protein_contribution_g': 22.5},
        {'name': 'Wild Nordic Blueberries', 'quantity': '80g', 'protein_contribution_g': 1.0},
        {'name': 'Sprouted Chia Seeds', 'quantity': '1 tbsp', 'protein_contribution_g': 2.0},
      ],
      'instructions': [
        'Whisk whey isolate directly into cold Greek yogurt with a fork until velvety and mousse-like.',
        'Fold in wild blueberries and Ceylon cinnamon.',
        'Top with chia seeds and roasted sliced almonds for texture.'
      ],
      'proCookingTip': 'Add 2 tbsp of cold unsweetened almond milk if you prefer a silkier parfait texture over thick mousse.',
      'supplements': ['whey_isolate', 'creatine'],
    },
    {
      'mealName': 'Crispy Pan-Blackened Tempeh & Hempseed Macro Power Bowl',
      'description': 'Marinated organic tempeh triangles seared in tamari aminos, paired with edamame, steamed broccoli florets, and raw shelled hemp hearts.',
      'mealType': MealType.lunch,
      'dietaryPref': DietaryPreference.vegan,
      'prepTimeMinutes': 10,
      'cookTimeMinutes': 12,
      'baseProtein': 44.0,
      'baseCarbs': 26.0,
      'baseFat': 16.0,
      'baseCals': 420.0,
      'ingredients': [
        {'name': 'Organic Soy Tempeh', 'quantity': '180g', 'protein_contribution_g': 34.0},
        {'name': 'Raw Shelled Hemp Hearts', 'quantity': '2 tbsp (20g)', 'protein_contribution_g': 7.0},
        {'name': 'Steamed Broccoli Florets', 'quantity': '150g', 'protein_contribution_g': 4.5},
      ],
      'instructions': [
        'Slice tempeh into triangles and steam for 3 minutes to open the pores.',
        'Toss in coconut tamari, grated ginger, and garlic.',
        'Pan-sear on medium-high until edges are deeply caramelized and crispy.',
        'Serve over steamed broccoli and sprinkle generously with raw hemp hearts.'
      ],
      'proCookingTip': 'Steaming tempeh before searing allows the savory marinade to penetrate directly into the core.',
      'supplements': ['plant_isolate', 'electrolytes'],
    },
  ];

  static MealRecipe generateRecipe({
    required double targetProteinG,
    required double targetCalories,
    required DietaryPreference dietaryPref,
    required MealType mealType,
    int maxPrepTimeMins = 30,
  }) {
    List<Map<String, dynamic>> matches = _catalog.where((r) {
      return r['dietaryPref'] == dietaryPref ||
          dietaryPref == DietaryPreference.highProtein ||
          dietaryPref == DietaryPreference.omnivore;
    }).toList();

    if (matches.isEmpty) matches = _catalog;

    final typeMatches = matches.where((r) => r['mealType'] == mealType).toList();
    final chosen = typeMatches.isNotEmpty ? typeMatches.first : matches.first;

    final double baseP = chosen['baseProtein'] as double;
    final double scale = max(0.6, min(2.5, targetProteinG / baseP));

    final double scaledP = (baseP * scale * 10).round() / 10.0;
    final double scaledC = ((chosen['baseCarbs'] as double) * scale * 10).round() / 10.0;
    final double scaledF = ((chosen['baseFat'] as double) * scale * 10).round() / 10.0;
    final double scaledCals = ((scaledP * 4.0) + (scaledC * 4.0) + (scaledF * 9.0)).roundToDouble();

    final double pPct = scaledCals > 0 ? ((scaledP * 4.0 / scaledCals) * 100 * 10).round() / 10.0 : 0.0;

    final List<IngredientItem> ingredients = [];
    for (final ing in chosen['ingredients']) {
      final double baseProt = ing['protein_contribution_g'] as double;
      ingredients.add(IngredientItem(
        name: ing['name'] as String,
        quantity: scale != 1.0 ? "${ing['quantity']} (${(scale * 100).round()}%)" : ing['quantity'] as String,
        proteinContributionG: (baseProt * scale * 10).round() / 10.0,
      ));
    }

    final List<AffiliateSupplement> supplements = [];
    for (final sKey in (chosen['supplements'] as List<String>? ?? ['whey_isolate', 'creatine'])) {
      if (affiliateSupplements.containsKey(sKey)) {
        supplements.add(affiliateSupplements[sKey]!);
      }
    }

    return MealRecipe(
      mealName: chosen['mealName'] as String,
      description: chosen['description'] as String,
      mealType: mealType,
      dietaryPref: dietaryPref,
      prepTimeMinutes: min(maxPrepTimeMins, chosen['prepTimeMinutes'] as int),
      cookTimeMinutes: chosen['cookTimeMinutes'] as int,
      proteinG: scaledP,
      carbsG: scaledC,
      fatG: scaledF,
      calories: scaledCals,
      proteinToCaloriePct: pPct,
      ingredients: ingredients,
      instructions: List<String>.from(chosen['instructions'] as List),
      proCookingTip: chosen['proCookingTip'] as String,
      longevityScore: 94,
      affiliateSupplements: supplements,
    );
  }
}
