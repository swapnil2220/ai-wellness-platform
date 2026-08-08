enum DietaryPreference {
  highProtein,
  omnivore,
  vegetarian,
  vegan,
  pescatarian,
  keto,
}

enum MealType {
  breakfast,
  lunch,
  dinner,
  snack,
  postWorkout,
}

class IngredientItem {
  final String name;
  final String quantity;
  final double proteinContributionG;

  const IngredientItem({
    required this.name,
    required this.quantity,
    required this.proteinContributionG,
  });

  Map<String, dynamic> toJson() => {
    'name': name,
    'quantity': quantity,
    'protein_contribution_g': proteinContributionG,
  };
}

class AffiliateSupplement {
  final String name;
  final String category;
  final String whyRecommended;
  final String suggestedDose;
  final String affiliateUrl;

  const AffiliateSupplement({
    required this.name,
    required this.category,
    required this.whyRecommended,
    required this.suggestedDose,
    required this.affiliateUrl,
  });
}

class MealRecipe {
  final String mealName;
  final String description;
  final MealType mealType;
  final DietaryPreference dietaryPref;
  final int prepTimeMinutes;
  final int cookTimeMinutes;
  final double proteinG;
  final double carbsG;
  final double fatG;
  final double calories;
  final double proteinToCaloriePct;
  final List<IngredientItem> ingredients;
  final List<String> instructions;
  final String proCookingTip;
  final int longevityScore;
  final List<AffiliateSupplement> affiliateSupplements;

  const MealRecipe({
    required this.mealName,
    required this.description,
    required this.mealType,
    required this.dietaryPref,
    required this.prepTimeMinutes,
    required this.cookTimeMinutes,
    required this.proteinG,
    required this.carbsG,
    required this.fatG,
    required this.calories,
    required this.proteinToCaloriePct,
    required this.ingredients,
    required this.instructions,
    required this.proCookingTip,
    required this.longevityScore,
    this.affiliateSupplements = const [],
  });
}
