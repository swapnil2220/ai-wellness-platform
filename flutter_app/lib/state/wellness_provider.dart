import 'package:flutter/foundation.dart';
import '../models/user_profile.dart';
import '../models/meal_recipe.dart';
import '../models/book_insight.dart';
import '../models/logged_meal.dart';
import '../services/protein_engine_service.dart';
import '../services/meal_planner_service.dart';
import '../services/book_rag_service.dart';

class WellnessProvider extends ChangeNotifier {
  int _currentTabIndex = 0;
  int get currentTabIndex => _currentTabIndex;

  UserProfile _userProfile = const UserProfile(
    weightKg: 75.0,
    heightCm: 178.0,
    age: 28,
    gender: Gender.male,
    activityLevel: ActivityLevel.moderate,
    goal: FitnessGoal.fatLoss,
    proteinMultiplier: 2.0,
    mealsPerDay: 3,
  );
  UserProfile get userProfile => _userProfile;

  late MacroTargets _macroTargets;
  MacroTargets get macroTargets => _macroTargets;

  final List<LoggedMeal> _loggedMeals = [];
  List<LoggedMeal> get loggedMeals => List.unmodifiable(_loggedMeals);

  int _waterMl = 750;
  int get waterMl => _waterMl;

  MealRecipe? _currentRecipe;
  MealRecipe? get currentRecipe => _currentRecipe;

  final List<BookInsight> _savedBookmarks = [];
  List<BookInsight> get savedBookmarks => List.unmodifiable(_savedBookmarks);

  String _ragSearchQuery = '';
  String get ragSearchQuery => _ragSearchQuery;

  String _selectedCategory = 'All';
  String get selectedCategory => _selectedCategory;

  String _selectedBook = 'All';
  String get selectedBook => _selectedBook;

  ReflectionResponse? _latestReflection;
  ReflectionResponse? get latestReflection => _latestReflection;

  bool _isAnnualBilling = false;
  bool get isAnnualBilling => _isAnnualBilling;

  WellnessProvider() {
    _recalculateMacros();
    _generateDefaultRecipe();
  }

  void setTabIndex(int index) {
    _currentTabIndex = index;
    notifyListeners();
  }

  void updateProfile({
    double? weightKg,
    double? heightCm,
    int? age,
    Gender? gender,
    ActivityLevel? activityLevel,
    FitnessGoal? goal,
    double? proteinMultiplier,
    int? mealsPerDay,
  }) {
    _userProfile = _userProfile.copyWith(
      weightKg: weightKg,
      heightCm: heightCm,
      age: age,
      gender: gender,
      activityLevel: activityLevel,
      goal: goal,
      proteinMultiplier: proteinMultiplier,
      mealsPerDay: mealsPerDay,
    );
    _recalculateMacros();
    notifyListeners();
  }

  void _recalculateMacros() {
    _macroTargets = ProteinEngineService.calculateMacroTargets(_userProfile);
  }

  void _generateDefaultRecipe() {
    _currentRecipe = MealPlannerService.generateRecipe(
      targetProteinG: _macroTargets.proteinG / _userProfile.mealsPerDay,
      targetCalories: _macroTargets.targetCalories / _userProfile.mealsPerDay,
      dietaryPref: DietaryPreference.highProtein,
      mealType: MealType.lunch,
    );
  }

  void generateNewRecipe({
    required double targetProteinG,
    required double targetCalories,
    required DietaryPreference dietaryPref,
    required MealType mealType,
    int maxPrepTimeMins = 30,
  }) {
    _currentRecipe = MealPlannerService.generateRecipe(
      targetProteinG: targetProteinG,
      targetCalories: targetCalories,
      dietaryPref: dietaryPref,
      mealType: mealType,
      maxPrepTimeMins: maxPrepTimeMins,
    );
    notifyListeners();
  }

  void logMealFromRecipe(MealRecipe recipe) {
    final meal = LoggedMeal(
      id: DateTime.now().millisecondsSinceEpoch,
      mealName: recipe.mealName,
      mealType: recipe.mealType.name,
      proteinG: recipe.proteinG,
      carbsG: recipe.carbsG,
      fatG: recipe.fatG,
      calories: recipe.calories,
      loggedTime: DateTime.now(),
    );
    _loggedMeals.insert(0, meal);
    notifyListeners();
  }

  void addQuickMeal({
    required String name,
    required String type,
    required double proteinG,
    required double carbsG,
    required double fatG,
    required double calories,
  }) {
    final meal = LoggedMeal(
      id: DateTime.now().millisecondsSinceEpoch,
      mealName: name,
      mealType: type,
      proteinG: proteinG,
      carbsG: carbsG,
      fatG: fatG,
      calories: calories,
      loggedTime: DateTime.now(),
    );
    _loggedMeals.insert(0, meal);
    notifyListeners();
  }

  void addWater(int ml) {
    _waterMl += ml;
    notifyListeners();
  }

  double get consumedProteinG => _loggedMeals.fold(0.0, (sum, m) => sum + m.proteinG);
  double get consumedCalories => _loggedMeals.fold(0.0, (sum, m) => sum + m.calories);

  double get remainingProteinG => (_macroTargets.proteinG - consumedProteinG).clamp(0.0, 999.0);
  double get remainingCalories => (_macroTargets.targetCalories - consumedCalories).clamp(0.0, 9999.0);

  void setRagSearch(String q) {
    _ragSearchQuery = q;
    notifyListeners();
  }

  void setCategoryFilter(String cat) {
    _selectedCategory = cat;
    notifyListeners();
  }

  void setBookFilter(String book) {
    _selectedBook = book;
    notifyListeners();
  }

  void toggleBookmark(BookInsight insight) {
    final exists = _savedBookmarks.any((b) => b.id == insight.id);
    if (exists) {
      _savedBookmarks.removeWhere((b) => b.id == insight.id);
    } else {
      _savedBookmarks.add(insight);
    }
    notifyListeners();
  }

  bool isBookmarked(String insightId) {
    return _savedBookmarks.any((b) => b.id == insightId);
  }

  void generateMicroReflection(String prompt) {
    _latestReflection = BookRagService.generateReflection(prompt);
    notifyListeners();
  }

  void toggleBillingCycle(bool isAnnual) {
    _isAnnualBilling = isAnnual;
    notifyListeners();
  }
}
