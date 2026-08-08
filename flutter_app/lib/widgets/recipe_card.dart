import 'package:flutter/material.dart';
import '../models/meal_recipe.dart';
import '../theme/app_theme.dart';
import 'glass_card.dart';
import 'metric_badge.dart';

class RecipeCardWidget extends StatelessWidget {
  final MealRecipe recipe;
  final VoidCallback onLogMeal;

  const RecipeCardWidget({
    super.key,
    required this.recipe,
    required this.onLogMeal,
  });

  @override
  Widget build(BuildContext context) {
    return GlassCard(
      padding: const EdgeInsets.all(22),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Wrap(
                      spacing: 8,
                      runSpacing: 6,
                      children: [
                        MetricBadge(
                          label: '⏱️ ${recipe.prepTimeMinutes}m prep • ${recipe.cookTimeMinutes}m cook',
                          type: MetricBadgeType.green,
                        ),
                        MetricBadge(
                          label: '🧬 Longevity Score: ${recipe.longevityScore}/100',
                          type: MetricBadgeType.purple,
                        ),
                        MetricBadge(
                          label: '🔥 ${recipe.proteinToCaloriePct.round()}% Protein Density',
                          type: MetricBadgeType.cyan,
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    Text(
                      recipe.mealName,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w700,
                        color: AppColors.textLight,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      recipe.description,
                      style: const TextStyle(
                        color: AppColors.textMuted,
                        fontSize: 13.5,
                        height: 1.4,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 16),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                decoration: BoxDecoration(
                  color: AppColors.bgDarkSecondary,
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: AppColors.cardBorder),
                ),
                child: Column(
                  children: [
                    Text(
                      '${recipe.proteinG}g',
                      style: const TextStyle(
                        fontSize: 26,
                        fontWeight: FontWeight.w800,
                        color: AppColors.softMint,
                      ),
                    ),
                    const Text(
                      'Protein',
                      style: TextStyle(
                        fontSize: 11,
                        color: AppColors.textMuted,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '${recipe.calories.round()} kcal',
                      style: const TextStyle(
                        fontSize: 13,
                        color: AppColors.textLight,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 18),
          const Divider(color: AppColors.cardBorder),
          const SizedBox(height: 14),

          // Ingredients
          const Text(
            '🛒 Ingredients & Protein Breakdown',
            style: TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.w700,
              color: AppColors.textLight,
            ),
          ),
          const SizedBox(height: 10),
          ...recipe.ingredients.map((ing) => Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      '${ing.name} (${ing.quantity})',
                      style: const TextStyle(color: AppColors.textLight, fontSize: 13.5),
                    ),
                    Text(
                      '+${ing.proteinContributionG}g P',
                      style: const TextStyle(
                        color: AppColors.softMint,
                        fontWeight: FontWeight.w600,
                        fontSize: 13.5,
                      ),
                    ),
                  ],
                ),
              )),

          const SizedBox(height: 16),

          // Pro Tip
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: AppColors.cyan.withOpacity(0.08),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: AppColors.cyan.withOpacity(0.3)),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('💡 ', style: TextStyle(fontSize: 16)),
                Expanded(
                  child: Text(
                    recipe.proCookingTip,
                    style: const TextStyle(
                      color: AppColors.iceCyan,
                      fontSize: 12.5,
                      height: 1.4,
                    ),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 18),

          // Action Button
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: onLogMeal,
              icon: const Icon(Icons.bookmark_add_outlined, size: 18),
              label: Text('Log ${recipe.proteinG}g Protein Meal to Daily Tracker'),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.emerald,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 14),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
