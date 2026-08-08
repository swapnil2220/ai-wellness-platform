class LoggedMeal {
  final int id;
  final String mealName;
  final String mealType;
  final double proteinG;
  final double carbsG;
  final double fatG;
  final double calories;
  final DateTime loggedTime;

  const LoggedMeal({
    required this.id,
    required this.mealName,
    required this.mealType,
    required this.proteinG,
    required this.carbsG,
    required this.fatG,
    required this.calories,
    required this.loggedTime,
  });
}
