import 'package:flutter_test/flutter_test.dart';
import '../lib/models/meal_recipe.dart';
import '../lib/services/meal_planner_service.dart';

void main() {
  group('MealPlannerService Unit Tests', () {
    test('Synthesizes structured high-protein meal recipe', () {
      final recipe = MealPlannerService.generateRecipe(
        targetProteinG: 45.0,
        targetCalories: 450.0,
        dietaryPref: DietaryPreference.highProtein,
        mealType: MealType.lunch,
      );

      expect(recipe.proteinG >= 30.0, true);
      expect(recipe.calories >= 250.0, true);
      expect(recipe.ingredients.isNotEmpty, true);
      expect(recipe.instructions.isNotEmpty, true);
      expect(recipe.affiliateSupplements.isNotEmpty, true);
    });

    test('Contains affiliate supplements catalog with creatine and whey', () {
      final catalog = MealPlannerService.affiliateSupplements;
      expect(catalog.containsKey('creatine'), true);
      expect(catalog.containsKey('whey_isolate'), true);
      expect(catalog.containsKey('electrolytes'), true);
      expect(catalog['creatine']!.name.contains('Creatine'), true);
    });
  });
}
