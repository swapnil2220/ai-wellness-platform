import 'package:flutter/material.dart';
import '../models/meal_recipe.dart';
import '../state/wellness_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/glass_card.dart';
import '../widgets/recipe_card.dart';
import '../widgets/metric_badge.dart';

class MealBuilderView extends StatefulWidget {
  final WellnessProvider provider;

  const MealBuilderView({super.key, required this.provider});

  @override
  State<MealBuilderView> createState() => _MealBuilderViewState();
}

class _MealBuilderViewState extends State<MealBuilderView> {
  DietaryPreference _dietaryPref = DietaryPreference.highProtein;
  MealType _mealType = MealType.lunch;
  late double _targetProtein;
  late double _targetCalories;
  int _maxPrepTime = 20;

  @override
  void initState() {
    super.initState();
    final targets = widget.provider.macroTargets;
    final mealsCount = widget.provider.userProfile.mealsPerDay;
    _targetProtein = (targets.proteinG / mealsCount * 10).round() / 10.0;
    _targetCalories = (targets.targetCalories / mealsCount).roundToDouble();
  }

  void _generateRecipe() {
    widget.provider.generateNewRecipe(
      targetProteinG: _targetProtein,
      targetCalories: _targetCalories,
      dietaryPref: _dietaryPref,
      mealType: _mealType,
      maxPrepTimeMins: _maxPrepTime,
    );
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('🥗 High-Protein Recipe Formulated!'),
        backgroundColor: AppColors.emerald,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final recipe = widget.provider.currentRecipe;

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '🥗 AI High-Protein Meal Generator',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.w800,
              color: AppColors.textLight,
            ),
          ),
          const SizedBox(height: 4),
          const Text(
            'Formulate chef-crafted recipes tailored to your remaining macros and dietary preferences.',
            style: TextStyle(color: AppColors.textMuted, fontSize: 13.5),
          ),
          const SizedBox(height: 16),

          // Generator Controls Card
          GlassCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                LayoutBuilder(
                  builder: (context, constraints) {
                    final bool isWide = constraints.maxWidth > 650;
                    return Wrap(
                      spacing: 20,
                      runSpacing: 14,
                      children: [
                        SizedBox(
                          width: isWide ? (constraints.maxWidth - 40) / 3 : constraints.maxWidth,
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text('Meal Category', style: TextStyle(color: AppColors.textMuted, fontSize: 12.5)),
                              const SizedBox(height: 6),
                              DropdownButtonFormField<MealType>(
                                value: _mealType,
                                isExpanded: true,
                                items: const [
                                  DropdownMenuItem(value: MealType.breakfast, child: Text('🍳 High-Protein Breakfast')),
                                  DropdownMenuItem(value: MealType.lunch, child: Text('🍲 Power Lunch')),
                                  DropdownMenuItem(value: MealType.dinner, child: Text('🥩 Recovery Dinner')),
                                  DropdownMenuItem(value: MealType.postWorkout, child: Text('⚡ Post-Workout Shake')),
                                  DropdownMenuItem(value: MealType.snack, child: Text('🥑 Micro Snack')),
                                ],
                                onChanged: (v) => setState(() => _mealType = v!),
                              ),
                              const SizedBox(height: 12),
                              const Text('Dietary Framework', style: TextStyle(color: AppColors.textMuted, fontSize: 12.5)),
                              const SizedBox(height: 6),
                              DropdownButtonFormField<DietaryPreference>(
                                value: _dietaryPref,
                                isExpanded: true,
                                items: const [
                                  DropdownMenuItem(value: DietaryPreference.highProtein, child: Text('🥩 High-Protein Pure')),
                                  DropdownMenuItem(value: DietaryPreference.omnivore, child: Text('🍗 Omnivore')),
                                  DropdownMenuItem(value: DietaryPreference.vegetarian, child: Text('🧀 Vegetarian (Greek Yogurt, Whey)')),
                                  DropdownMenuItem(value: DietaryPreference.vegan, child: Text('🌱 Plant-Based (Tempeh, Pea)')),
                                  DropdownMenuItem(value: DietaryPreference.pescatarian, child: Text('🐟 Pescatarian (Salmon, Tuna)')),
                                  DropdownMenuItem(value: DietaryPreference.keto, child: Text('🥑 High-Protein Keto')),
                                ],
                                onChanged: (v) => setState(() => _dietaryPref = v!),
                              ),
                            ],
                          ),
                        ),
                        SizedBox(
                          width: isWide ? (constraints.maxWidth - 40) / 3 : constraints.maxWidth,
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              _sliderField(
                                label: 'Target Protein for Meal',
                                valueText: '${_targetProtein.toStringAsFixed(1)}g',
                                value: _targetProtein,
                                min: 10.0,
                                max: 120.0,
                                onChanged: (v) => setState(() => _targetProtein = (v * 10).round() / 10.0),
                              ),
                              _sliderField(
                                label: 'Target Calories',
                                valueText: '${_targetCalories.round()} kcal',
                                value: _targetCalories,
                                min: 150.0,
                                max: 1500.0,
                                onChanged: (v) => setState(() => _targetCalories = v.roundToDouble()),
                              ),
                            ],
                          ),
                        ),
                        SizedBox(
                          width: isWide ? (constraints.maxWidth - 40) / 3 : constraints.maxWidth,
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              _sliderField(
                                label: 'Max Prep Time',
                                valueText: '$_maxPrepTime mins',
                                value: _maxPrepTime.toDouble(),
                                min: 5.0,
                                max: 60.0,
                                onChanged: (v) => setState(() => _maxPrepTime = v.round()),
                              ),
                              const SizedBox(height: 10),
                              SizedBox(
                                width: double.infinity,
                                child: ElevatedButton.icon(
                                  onPressed: _generateRecipe,
                                  icon: const Icon(Icons.auto_awesome, size: 18),
                                  label: const Text('Generate AI Recipe'),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    );
                  },
                ),
              ],
            ),
          ),

          const SizedBox(height: 20),

          // Recipe Card Display
          if (recipe != null)
            RecipeCardWidget(
              recipe: recipe,
              onLogMeal: () {
                widget.provider.logMealFromRecipe(recipe);
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('✅ Added "${recipe.mealName}" (+${recipe.proteinG}g P) to Tracker!'),
                    backgroundColor: AppColors.emerald,
                  ),
                );
              },
            ),

          const SizedBox(height: 22),

          // Affiliate Supplements Section
          if (recipe != null && recipe.affiliateSupplements.isNotEmpty) ...[
            const Text(
              '💊 Recommended Ergogenic Supplements for this Meal',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w700,
                color: AppColors.textLight,
              ),
            ),
            const SizedBox(height: 12),
            LayoutBuilder(
              builder: (context, constraints) {
                final bool isWide = constraints.maxWidth > 700;
                final double cardWidth = isWide ? (constraints.maxWidth - 20) / 2 : constraints.maxWidth;
                return Wrap(
                  spacing: 16,
                  runSpacing: 14,
                  children: recipe.affiliateSupplements.map((supp) {
                    return Container(
                      width: cardWidth,
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: AppColors.cardSurface,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: AppColors.cardBorder),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          MetricBadge(label: supp.category, type: MetricBadgeType.cyan),
                          const SizedBox(height: 8),
                          Text(
                            supp.name,
                            style: const TextStyle(
                              fontWeight: FontWeight.w700,
                              fontSize: 14,
                              color: AppColors.textLight,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            supp.whyRecommended,
                            style: const TextStyle(color: AppColors.textMuted, fontSize: 12.5),
                          ),
                          const SizedBox(height: 6),
                          Text(
                            'Suggested Dose: ${supp.suggestedDose}',
                            style: const TextStyle(color: AppColors.softMint, fontSize: 12, fontWeight: FontWeight.w600),
                          ),
                        ],
                      ),
                    );
                  }).toList(),
                );
              },
            ),
          ],
        ],
      ),
    );
  }

  Widget _sliderField({
    required String label,
    required String valueText,
    required double value,
    required double min,
    required double max,
    required ValueChanged<double> onChanged,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: const TextStyle(color: AppColors.textMuted, fontSize: 12.5)),
            Text(valueText, style: const TextStyle(color: AppColors.brightAqua, fontWeight: FontWeight.w700, fontSize: 13)),
          ],
        ),
        Slider(
          value: value,
          min: min,
          max: max,
          activeColor: AppColors.emerald,
          inactiveColor: AppColors.bgDarkSecondary,
          onChanged: onChanged,
        ),
      ],
    );
  }
}
