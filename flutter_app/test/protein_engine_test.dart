import 'package:flutter_test/flutter_test.dart';
import '../lib/models/user_profile.dart';
import '../lib/services/protein_engine_service.dart';

void main() {
  group('ProteinEngineService Unit Tests', () {
    test('Calculates male BMR accurately using Mifflin-St Jeor', () {
      // 10 * 80 + 6.25 * 180 - 5 * 30 + 5 = 800 + 1125 - 150 + 5 = 1780.0
      final bmr = ProteinEngineService.calculateBmr(
        weightKg: 80.0,
        heightCm: 180.0,
        age: 30,
        gender: Gender.male,
      );
      expect(bmr, 1780.0);
    });

    test('Calculates TDEE with activity multiplier', () {
      final tdee = ProteinEngineService.calculateTdee(1800.0, ActivityLevel.moderate);
      expect(tdee, (1800.0 * 1.55).roundToDouble());
    });

    test('Allocates high-protein fat loss deficit with leucine threshold', () {
      const profile = UserProfile(
        weightKg: 75.0,
        heightCm: 175.0,
        age: 25,
        gender: Gender.male,
        activityLevel: ActivityLevel.moderate,
        goal: FitnessGoal.fatLoss,
        proteinMultiplier: 2.2,
        mealsPerDay: 3,
      );

      final targets = ProteinEngineService.calculateMacroTargets(profile);
      expect(targets.proteinMultiplierUsed, 2.2);
      expect(targets.proteinG, (75.0 * 2.2 * 10).round() / 10.0);
      expect(targets.meals.length, 3);
      for (final m in targets.meals) {
        expect(m.targetProteinG >= 28.0, true);
        expect(m.leucineThresholdMet, true);
      }
    });

    test('Supports high protein and surplus in muscle gain', () {
      const profile = UserProfile(
        weightKg: 85.0,
        heightCm: 185.0,
        age: 24,
        gender: Gender.male,
        activityLevel: ActivityLevel.veryActive,
        goal: FitnessGoal.muscleGain,
        proteinMultiplier: 2.4,
        mealsPerDay: 4,
      );

      final targets = ProteinEngineService.calculateMacroTargets(profile);
      expect(targets.targetCalories > targets.tdee, true);
      expect(targets.proteinG, (85.0 * 2.4 * 10).round() / 10.0);
      expect(targets.meals.length, 4);
    });
  });
}
