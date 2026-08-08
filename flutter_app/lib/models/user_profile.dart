enum Gender { male, female, other }

enum ActivityLevel {
  sedentary, // 1.2
  light, // 1.375
  moderate, // 1.55
  veryActive, // 1.725
  extraActive, // 1.9
}

enum FitnessGoal {
  fatLoss,
  muscleGain,
  maintenance,
}

class UserProfile {
  final double weightKg;
  final double heightCm;
  final int age;
  final Gender gender;
  final ActivityLevel activityLevel;
  final FitnessGoal goal;
  final double proteinMultiplier;
  final int mealsPerDay;

  const UserProfile({
    required this.weightKg,
    required this.heightCm,
    required this.age,
    this.gender = Gender.male,
    this.activityLevel = ActivityLevel.moderate,
    this.goal = FitnessGoal.fatLoss,
    this.proteinMultiplier = 2.0,
    this.mealsPerDay = 3,
  });

  UserProfile copyWith({
    double? weightKg,
    double? heightCm,
    int? age,
    Gender? gender,
    ActivityLevel? activityLevel,
    FitnessGoal? goal,
    double? proteinMultiplier,
    int? mealsPerDay,
  }) {
    return UserProfile(
      weightKg: weightKg ?? this.weightKg,
      heightCm: heightCm ?? this.heightCm,
      age: age ?? this.age,
      gender: gender ?? this.gender,
      activityLevel: activityLevel ?? this.activityLevel,
      goal: goal ?? this.goal,
      proteinMultiplier: proteinMultiplier ?? this.proteinMultiplier,
      mealsPerDay: mealsPerDay ?? this.mealsPerDay,
    );
  }
}

class MealTargetDistribution {
  final int mealIndex;
  final String name;
  final double targetProteinG;
  final double targetCarbsG;
  final double targetFatsG;
  final double targetCalories;
  final bool leucineThresholdMet;

  const MealTargetDistribution({
    required this.mealIndex,
    required this.name,
    required this.targetProteinG,
    required this.targetCarbsG,
    required this.targetFatsG,
    required this.targetCalories,
    required this.leucineThresholdMet,
  });
}

class MacroTargets {
  final double bmr;
  final double tdee;
  final double targetCalories;
  final double proteinG;
  final double carbsG;
  final double fatsG;
  final double proteinMultiplierUsed;
  final double proteinPct;
  final double carbsPct;
  final double fatsPct;
  final List<MealTargetDistribution> meals;
  final List<String> longevityNotes;

  const MacroTargets({
    required this.bmr,
    required this.tdee,
    required this.targetCalories,
    required this.proteinG,
    required this.carbsG,
    required this.fatsG,
    required this.proteinMultiplierUsed,
    required this.proteinPct,
    required this.carbsPct,
    required this.fatsPct,
    required this.meals,
    required this.longevityNotes,
  });
}
