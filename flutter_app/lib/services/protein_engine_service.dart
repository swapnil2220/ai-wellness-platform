import 'dart:math';
import '../models/user_profile.dart';

class ProteinEngineService {
  static const Map<ActivityLevel, double> activityMultipliers = {
    ActivityLevel.sedentary: 1.2,
    ActivityLevel.light: 1.375,
    ActivityLevel.moderate: 1.55,
    ActivityLevel.veryActive: 1.725,
    ActivityLevel.extraActive: 1.9,
  };

  static double calculateBmr({
    required double weightKg,
    required double heightCm,
    required int age,
    required Gender gender,
  }) {
    final double base = (10.0 * weightKg) + (6.25 * heightCm) - (5.0 * age);
    if (gender == Gender.male) {
      return (base + 5.0).roundToDouble();
    } else if (gender == Gender.female) {
      return (base - 161.0).roundToDouble();
    } else {
      return (base - 78.0).roundToDouble();
    }
  }

  static double calculateTdee(double bmr, ActivityLevel activityLevel) {
    final double mult = activityMultipliers[activityLevel] ?? 1.2;
    return (bmr * mult).roundToDouble();
  }

  static MacroTargets calculateMacroTargets(UserProfile profile) {
    final double bmr = calculateBmr(
      weightKg: profile.weightKg,
      heightCm: profile.heightCm,
      age: profile.age,
      gender: profile.gender,
    );
    final double tdee = calculateTdee(bmr, profile.activityLevel);

    double targetCalories;
    double defaultProteinMult;

    switch (profile.goal) {
      case FitnessGoal.fatLoss:
        targetCalories = tdee * 0.80; // 20% deficit
        defaultProteinMult = 2.2;
        break;
      case FitnessGoal.muscleGain:
        targetCalories = tdee * 1.10; // 10% surplus
        defaultProteinMult = 2.0;
        break;
      case FitnessGoal.maintenance:
        targetCalories = tdee;
        defaultProteinMult = 1.8;
        break;
    }

    final double proteinMult = profile.proteinMultiplier > 0 ? profile.proteinMultiplier : defaultProteinMult;
    double proteinG = (profile.weightKg * proteinMult * 10).round() / 10.0;
    double proteinCals = proteinG * 4.0;

    // Minimum essential fats (0.5g/kg or 15% cals)
    final double minFatCals = min(targetCalories * 0.35, max(profile.weightKg * 0.5 * 9.0, targetCalories * 0.15));
    final double maxProteinCals = max(0.0, targetCalories - minFatCals);
    if (proteinCals > maxProteinCals && maxProteinCals > 0) {
      proteinCals = maxProteinCals;
      proteinG = (proteinCals / 4.0 * 10).round() / 10.0;
    }

    // Fats ~25%
    final double fatsCals = min(max(0.0, targetCalories - proteinCals), max(profile.weightKg * 0.6 * 9.0, targetCalories * 0.25));
    final double fatsG = (fatsCals / 9.0 * 10).round() / 10.0;

    // Carbohydrates: Remainder
    final double carbsCals = max(0.0, targetCalories - proteinCals - (fatsG * 9.0));
    final double carbsG = (carbsCals / 4.0 * 10).round() / 10.0;

    final double totalCalculatedCals = (proteinCals + (fatsG * 9.0) + (carbsG * 4.0)).roundToDouble();

    final double pPct = totalCalculatedCals > 0 ? ((proteinCals / totalCalculatedCals) * 100).roundToDouble() : 0;
    final double fPct = totalCalculatedCals > 0 ? (((fatsG * 9.0) / totalCalculatedCals) * 100).roundToDouble() : 0;
    final double cPct = totalCalculatedCals > 0 ? (((carbsG * 4.0) / totalCalculatedCals) * 100).roundToDouble() : 0;

    final int mealsCount = max(1, profile.mealsPerDay);
    final double perMealP = (proteinG / mealsCount * 10).round() / 10.0;
    final double perMealC = (carbsG / mealsCount * 10).round() / 10.0;
    final double perMealF = (fatsG / mealsCount * 10).round() / 10.0;
    final double perMealCal = (totalCalculatedCals / mealsCount * 10).round() / 10.0;

    final List<String> mealNames = [
      "Breakfast / Meal 1",
      "Power Lunch / Meal 2",
      "Recovery Dinner / Meal 3",
      "Post-Workout Shake",
      "Evening Snack",
      "Early Fuel"
    ];

    final List<MealTargetDistribution> meals = [];
    for (int i = 0; i < mealsCount; i++) {
      final String name = i < mealNames.length ? mealNames[i] : "Meal ${i + 1}";
      meals.add(MealTargetDistribution(
        mealIndex: i + 1,
        name: name,
        targetProteinG: perMealP,
        targetCarbsG: perMealC,
        targetFatsG: perMealF,
        targetCalories: perMealCal,
        leucineThresholdMet: perMealP >= 28.0,
      ));
    }

    final List<String> longevityNotes = [
      "High-protein intake (${proteinMult.toStringAsFixed(1)}g/kg) elevates Diet-Induced Thermogenesis (TEF) and shields against sarcopenia.",
      "Per-meal distribution (~${perMealP.toStringAsFixed(0)}g protein) crosses the ~2.5g–3.5g leucine trigger threshold for mTOR/MPS activation.",
      "Hydration protocol: Consume 35–45ml water per kg body weight plus 500mg sodium pre-workout."
    ];

    return MacroTargets(
      bmr: bmr,
      tdee: tdee,
      targetCalories: totalCalculatedCals,
      proteinG: proteinG,
      carbsG: carbsG,
      fatsG: fatsG,
      proteinMultiplierUsed: proteinMult,
      proteinPct: pPct,
      carbsPct: cPct,
      fatsPct: fPct,
      meals: meals,
      longevityNotes: longevityNotes,
    );
  }
}
