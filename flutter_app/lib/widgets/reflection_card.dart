import 'package:flutter/material.dart';
import '../models/book_insight.dart';
import '../theme/app_theme.dart';
import 'glass_card.dart';
import 'metric_badge.dart';

class ReflectionCardWidget extends StatelessWidget {
  final ReflectionResponse reflection;

  const ReflectionCardWidget({super.key, required this.reflection});

  @override
  Widget build(BuildContext context) {
    return GlassCard(
      borderColor: AppColors.softMint.withOpacity(0.4),
      backgroundGradient: LinearGradient(
        colors: [
          AppColors.emerald.withOpacity(0.12),
          AppColors.bgDarkSecondary.withOpacity(0.9),
        ],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const MetricBadge(
                label: '🧠 Cognitive Reframing',
                type: MetricBadgeType.green,
              ),
              Text(
                reflection.sourceCitation,
                style: const TextStyle(
                  color: AppColors.textMuted,
                  fontSize: 11.5,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            reflection.reflectionSummary,
            style: const TextStyle(
              fontSize: 14.5,
              fontWeight: FontWeight.w500,
              color: AppColors.textLight,
              height: 1.45,
            ),
          ),
          const SizedBox(height: 16),
          const Text(
            '🚀 3-Step Immediate Action Protocol:',
            style: TextStyle(
              color: AppColors.softMint,
              fontWeight: FontWeight.w700,
              fontSize: 14,
            ),
          ),
          const SizedBox(height: 8),
          ...reflection.threeStepActionPlan.map((step) => Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('➔ ', style: TextStyle(color: AppColors.softMint, fontWeight: FontWeight.bold)),
                    Expanded(
                      child: Text(
                        step,
                        style: const TextStyle(
                          color: AppColors.textLight,
                          fontSize: 13,
                          height: 1.35,
                        ),
                      ),
                    ),
                  ],
                ),
              )),
          const SizedBox(height: 14),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            decoration: BoxDecoration(
              color: AppColors.cyan.withOpacity(0.08),
              border: const Border(left: BorderSide(color: AppColors.cyan, width: 3)),
              borderRadius: const BorderRadius.horizontal(right: Radius.circular(8)),
            ),
            child: Text(
              'Daily Mantra: "${reflection.motivationalMantra}"',
              style: const TextStyle(
                color: AppColors.iceCyan,
                fontStyle: FontStyle.italic,
                fontSize: 12.5,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
