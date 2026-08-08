import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

enum MetricBadgeType { green, cyan, purple, amber }

class MetricBadge extends StatelessWidget {
  final String label;
  final MetricBadgeType type;

  const MetricBadge({
    super.key,
    required this.label,
    this.type = MetricBadgeType.green,
  });

  @override
  Widget build(BuildContext context) {
    Color bg;
    Color border;
    Color text;

    switch (type) {
      case MetricBadgeType.green:
        bg = AppColors.emerald.withOpacity(0.18);
        border = AppColors.emerald.withOpacity(0.45);
        text = AppColors.softMint;
        break;
      case MetricBadgeType.cyan:
        bg = AppColors.cyan.withOpacity(0.18);
        border = AppColors.cyan.withOpacity(0.45);
        text = AppColors.brightAqua;
        break;
      case MetricBadgeType.purple:
        bg = const Color(0xFF0D9488).withOpacity(0.22);
        border = const Color(0xFF5EEAD4).withOpacity(0.45);
        text = const Color(0xFF5EEAD4);
        break;
      case MetricBadgeType.amber:
        bg = const Color(0xFF14B8A6).withOpacity(0.25);
        border = const Color(0xFFA7F3D0).withOpacity(0.45);
        text = const Color(0xFFA7F3D0);
        break;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: border, width: 1),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: text,
          fontSize: 11.5,
          fontWeight: FontWeight.w600,
          letterSpacing: 0.4,
        ),
      ),
    );
  }
}
