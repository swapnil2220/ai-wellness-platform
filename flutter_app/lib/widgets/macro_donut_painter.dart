import 'dart:math';
import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class MacroDonutPainter extends CustomPainter {
  final double proteinPct;
  final double carbsPct;
  final double fatsPct;
  final double strokeWidth;

  MacroDonutPainter({
    required this.proteinPct,
    required this.carbsPct,
    required this.fatsPct,
    this.strokeWidth = 18.0,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = (min(size.width, size.height) - strokeWidth) / 2;

    final backgroundPaint = Paint()
      ..color = AppColors.bgDarkSecondary
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth;

    canvas.drawCircle(center, radius, backgroundPaint);

    final double total = max(1.0, proteinPct + carbsPct + fatsPct);
    double startAngle = -pi / 2;

    // 1. Protein Arc (Emerald Green)
    final double sweepP = (proteinPct / total) * 2 * pi;
    if (sweepP > 0) {
      final paintP = Paint()
        ..color = AppColors.emerald
        ..style = PaintingStyle.stroke
        ..strokeCap = StrokeCap.round
        ..strokeWidth = strokeWidth;
      canvas.drawArc(Rect.fromCircle(center: center, radius: radius), startAngle, sweepP, false, paintP);
      startAngle += sweepP;
    }

    // 2. Carbs Arc (Cyan / Aqua)
    final double sweepC = (carbsPct / total) * 2 * pi;
    if (sweepC > 0) {
      final paintC = Paint()
        ..color = AppColors.cyan
        ..style = PaintingStyle.stroke
        ..strokeCap = StrokeCap.round
        ..strokeWidth = strokeWidth;
      canvas.drawArc(Rect.fromCircle(center: center, radius: radius), startAngle, sweepC, false, paintC);
      startAngle += sweepC;
    }

    // 3. Fats Arc (Sage Teal)
    final double sweepF = (fatsPct / total) * 2 * pi;
    if (sweepF > 0) {
      final paintF = Paint()
        ..color = const Color(0xFF14B8A6)
        ..style = PaintingStyle.stroke
        ..strokeCap = StrokeCap.round
        ..strokeWidth = strokeWidth;
      canvas.drawArc(Rect.fromCircle(center: center, radius: radius), startAngle, sweepF, false, paintF);
    }
  }

  @override
  bool shouldRepaint(covariant MacroDonutPainter oldDelegate) {
    return oldDelegate.proteinPct != proteinPct ||
        oldDelegate.carbsPct != carbsPct ||
        oldDelegate.fatsPct != fatsPct;
  }
}

class MacroDonutWidget extends StatelessWidget {
  final double proteinG;
  final double carbsG;
  final double fatsG;
  final double calories;

  const MacroDonutWidget({
    super.key,
    required this.proteinG,
    required this.carbsG,
    required this.fatsG,
    required this.calories,
  });

  @override
  Widget build(BuildContext context) {
    final double pCals = proteinG * 4.0;
    final double cCals = carbsG * 4.0;
    final double fCals = fatsG * 9.0;
    final double totalCals = max(1.0, pCals + cCals + fCals);

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        SizedBox(
          width: 170,
          height: 170,
          child: CustomPaint(
            painter: MacroDonutPainter(
              proteinPct: pCals,
              carbsPct: cCals,
              fatsPct: fCals,
            ),
            child: Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    '${calories.round()}',
                    style: const TextStyle(
                      fontSize: 26,
                      fontWeight: FontWeight.w800,
                      color: AppColors.textLight,
                    ),
                  ),
                  const Text(
                    'TARGET KCAL',
                    style: TextStyle(
                      fontSize: 10,
                      fontWeight: FontWeight.w700,
                      color: AppColors.textMuted,
                      letterSpacing: 0.8,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        const SizedBox(height: 18),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _legendItem(AppColors.emerald, 'Protein (${((pCals / totalCals) * 100).round()}%)'),
            const SizedBox(width: 14),
            _legendItem(AppColors.cyan, 'Carbs (${((cCals / totalCals) * 100).round()}%)'),
            const SizedBox(width: 14),
            _legendItem(const Color(0xFF14B8A6), 'Fats (${((fCals / totalCals) * 100).round()}%)'),
          ],
        ),
      ],
    );
  }

  Widget _legendItem(Color color, String text) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 10,
          height: 10,
          decoration: BoxDecoration(color: color, shape: BoxShape.circle),
        ),
        const SizedBox(width: 6),
        Text(
          text,
          style: const TextStyle(fontSize: 12, color: AppColors.textMuted, fontWeight: FontWeight.w500),
        ),
      ],
    );
  }
}
