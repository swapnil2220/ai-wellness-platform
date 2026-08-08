import 'package:flutter/material.dart';
import '../models/user_profile.dart';
import '../state/wellness_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/glass_card.dart';
import '../widgets/macro_donut_painter.dart';
import '../widgets/metric_badge.dart';

class MacroTrackerView extends StatefulWidget {
  final WellnessProvider provider;

  const MacroTrackerView({super.key, required this.provider});

  @override
  State<MacroTrackerView> createState() => _MacroTrackerViewState();
}

class _MacroTrackerViewState extends State<MacroTrackerView> {
  late double _weight;
  late double _height;
  late int _age;
  late Gender _gender;
  late ActivityLevel _activity;
  late FitnessGoal _goal;
  late double _proteinMult;
  late int _mealsCount;

  @override
  void initState() {
    super.initState();
    final p = widget.provider.userProfile;
    _weight = p.weightKg;
    _height = p.heightCm;
    _age = p.age;
    _gender = p.gender;
    _activity = p.activityLevel;
    _goal = p.goal;
    _proteinMult = p.proteinMultiplier;
    _mealsCount = p.mealsPerDay;
  }

  void _saveProfile() {
    widget.provider.updateProfile(
      weightKg: _weight,
      heightCm: _height,
      age: _age,
      gender: _gender,
      activityLevel: _activity,
      goal: _goal,
      proteinMultiplier: _proteinMult,
      mealsPerDay: _mealsCount,
    );
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('🎯 Profile and High-Protein Targets Calculated!'),
        backgroundColor: AppColors.emerald,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final targets = widget.provider.macroTargets;

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '🎯 Calculate Your Daily Metabolic Targets',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.w800,
              color: AppColors.textLight,
            ),
          ),
          const SizedBox(height: 16),

          // Profile Inputs Form Card
          GlassCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                LayoutBuilder(
                  builder: (context, constraints) {
                    final bool isWide = constraints.maxWidth > 650;
                    return Wrap(
                      spacing: 20,
                      runSpacing: 16,
                      children: [
                        SizedBox(
                          width: isWide ? (constraints.maxWidth - 40) / 3 : constraints.maxWidth,
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              _sliderField(
                                label: 'Body Weight',
                                valueText: '${_weight.toStringAsFixed(1)} kg',
                                value: _weight,
                                min: 35.0,
                                max: 250.0,
                                onChanged: (v) => setState(() => _weight = v),
                              ),
                              _sliderField(
                                label: 'Height',
                                valueText: '${_height.round()} cm',
                                value: _height,
                                min: 120.0,
                                max: 240.0,
                                onChanged: (v) => setState(() => _height = v),
                              ),
                            ],
                          ),
                        ),
                        SizedBox(
                          width: isWide ? (constraints.maxWidth - 40) / 3 : constraints.maxWidth,
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text('Biological Sex', style: TextStyle(color: AppColors.textMuted, fontSize: 12.5)),
                              const SizedBox(height: 6),
                              DropdownButtonFormField<Gender>(
                                value: _gender,
                                items: const [
                                  DropdownMenuItem(value: Gender.male, child: Text('Male')),
                                  DropdownMenuItem(value: Gender.female, child: Text('Female')),
                                  DropdownMenuItem(value: Gender.other, child: Text('Other')),
                                ],
                                onChanged: (v) => setState(() => _gender = v!),
                              ),
                              const SizedBox(height: 12),
                              const Text('Activity Level', style: TextStyle(color: AppColors.textMuted, fontSize: 12.5)),
                              const SizedBox(height: 6),
                              DropdownButtonFormField<ActivityLevel>(
                                value: _activity,
                                isExpanded: true,
                                items: const [
                                  DropdownMenuItem(value: ActivityLevel.sedentary, child: Text('Sedentary (1.2x)')),
                                  DropdownMenuItem(value: ActivityLevel.light, child: Text('Light Activity (1.375x)')),
                                  DropdownMenuItem(value: ActivityLevel.moderate, child: Text('Moderate Exercise (1.55x)')),
                                  DropdownMenuItem(value: ActivityLevel.veryActive, child: Text('Very Active (1.725x)')),
                                  DropdownMenuItem(value: ActivityLevel.extraActive, child: Text('Heavy Athlete (1.9x)')),
                                ],
                                onChanged: (v) => setState(() => _activity = v!),
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
                                label: 'Protein Multiplier',
                                valueText: '${_proteinMult.toStringAsFixed(1)} g/kg',
                                value: _proteinMult,
                                min: 1.6,
                                max: 2.4,
                                onChanged: (v) => setState(() => _proteinMult = (v * 10).round() / 10.0),
                              ),
                              const SizedBox(height: 6),
                              SizedBox(
                                width: double.infinity,
                                child: ElevatedButton.icon(
                                  onPressed: _saveProfile,
                                  icon: const Icon(Icons.check_circle_outline, size: 18),
                                  label: const Text('Update Targets'),
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

          // KPI Target Stat Cards
          LayoutBuilder(
            builder: (context, constraints) {
              final double cardWidth = constraints.maxWidth > 800 ? (constraints.maxWidth - 36) / 4 : (constraints.maxWidth - 12) / 2;
              return Wrap(
                spacing: 12,
                runSpacing: 12,
                children: [
                  _statCard(
                    width: cardWidth,
                    title: '🎯 Daily Calories',
                    value: '${targets.targetCalories.round()} kcal',
                    subtitle: 'TDEE: ${targets.tdee.round()}',
                    badgeColor: MetricBadgeType.cyan,
                  ),
                  _statCard(
                    width: cardWidth,
                    title: '🥩 Target Protein',
                    value: '${targets.proteinG}g',
                    subtitle: '${targets.proteinMultiplierUsed} g/kg bodyweight',
                    badgeColor: MetricBadgeType.green,
                  ),
                  _statCard(
                    width: cardWidth,
                    title: '🍞 Carbohydrates',
                    value: '${targets.carbsG}g',
                    subtitle: '${targets.carbsPct.round()}% of calories',
                    badgeColor: MetricBadgeType.cyan,
                  ),
                  _statCard(
                    width: cardWidth,
                    title: '🥑 Healthy Fats',
                    value: '${targets.fatsG}g',
                    subtitle: '${targets.fatsPct.round()}% of calories',
                    badgeColor: MetricBadgeType.purple,
                  ),
                ],
              );
            },
          ),

          const SizedBox(height: 22),

          // Donut Chart & Per-Meal Distribution Row
          LayoutBuilder(
            builder: (context, constraints) {
              final bool isWide = constraints.maxWidth > 750;
              return isWide
                  ? Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(
                          flex: 5,
                          child: GlassCard(
                            child: Column(
                              children: [
                                const Text(
                                  'Daily Macronutrient Breakdown',
                                  style: TextStyle(fontWeight: FontWeight.w700, fontSize: 16, color: AppColors.textLight),
                                ),
                                const SizedBox(height: 14),
                                MacroDonutWidget(
                                  proteinG: targets.proteinG,
                                  carbsG: targets.carbsG,
                                  fatsG: targets.fatsG,
                                  calories: targets.targetCalories,
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          flex: 6,
                          child: GlassCard(
                            child: _mealDistributionList(targets),
                          ),
                        ),
                      ],
                    )
                  : Column(
                      children: [
                        GlassCard(
                          child: MacroDonutWidget(
                            proteinG: targets.proteinG,
                            carbsG: targets.carbsG,
                            fatsG: targets.fatsG,
                            calories: targets.targetCalories,
                          ),
                        ),
                        const SizedBox(height: 16),
                        GlassCard(
                          child: _mealDistributionList(targets),
                        ),
                      ],
                    );
            },
          ),

          const SizedBox(height: 22),

          // Today's Logged Meals
          GlassCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      '📋 Today\'s Logged Nutrition',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: AppColors.textLight),
                    ),
                    Text(
                      '${widget.provider.consumedProteinG.toStringAsFixed(1)}g / ${targets.proteinG}g P',
                      style: const TextStyle(color: AppColors.softMint, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                const SizedBox(height: 14),
                if (widget.provider.loggedMeals.isEmpty)
                  const Padding(
                    padding: EdgeInsets.symmetric(vertical: 16),
                    child: Center(
                      child: Text(
                        'No meals logged yet today. Use the AI Meal Builder to generate and log chef-crafted recipes!',
                        style: TextStyle(color: AppColors.textMuted, fontSize: 13),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  )
                else
                  ...widget.provider.loggedMeals.map((m) => Container(
                        margin: const EdgeInsets.only(bottom: 8),
                        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                        decoration: BoxDecoration(
                          color: AppColors.bgDarkSecondary,
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(color: AppColors.cardBorder),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(m.mealName, style: const TextStyle(fontWeight: FontWeight.w600, color: AppColors.textLight)),
                                Text('${m.mealType.toUpperCase()} • ${m.calories.round()} kcal', style: const TextStyle(color: AppColors.textMuted, fontSize: 11.5)),
                              ],
                            ),
                            Text(
                              '+${m.proteinG}g Protein',
                              style: const TextStyle(color: AppColors.softMint, fontWeight: FontWeight.w700),
                            ),
                          ],
                        ),
                      )),
              ],
            ),
          ),
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

  Widget _statCard({
    required double width,
    required String title,
    required String value,
    required String subtitle,
    required MetricBadgeType badgeColor,
  }) {
    return Container(
      width: width,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.cardSurface,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.cardBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(color: AppColors.textMuted, fontSize: 12)),
          const SizedBox(height: 6),
          Text(value, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: AppColors.textLight)),
          const SizedBox(height: 4),
          Text(subtitle, style: const TextStyle(color: AppColors.softMint, fontSize: 11.5, fontWeight: FontWeight.w500)),
        ],
      ),
    );
  }

  Widget _mealDistributionList(MacroTargets targets) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          '🧬 Per-Meal Leucine & Protein Distribution',
          style: TextStyle(fontWeight: FontWeight.w700, fontSize: 16, color: AppColors.textLight),
        ),
        const SizedBox(height: 12),
        ...targets.meals.map((m) => Padding(
              padding: const EdgeInsets.symmetric(vertical: 6),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(m.name, style: const TextStyle(color: AppColors.textLight, fontSize: 13.5)),
                  Row(
                    children: [
                      Text('${m.targetProteinG}g P', style: const TextStyle(color: AppColors.softMint, fontWeight: FontWeight.w700)),
                      const SizedBox(width: 8),
                      Text('(${m.targetCalories.round()} kcal)', style: const TextStyle(color: AppColors.textMuted, fontSize: 12)),
                    ],
                  ),
                ],
              ),
            )),
      ],
    );
  }
}
