import 'package:flutter/material.dart';
import '../state/wellness_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/glass_card.dart';
import '../widgets/metric_badge.dart';

class ProTierView extends StatefulWidget {
  final WellnessProvider provider;

  const ProTierView({super.key, required this.provider});

  @override
  State<ProTierView> createState() => _ProTierViewState();
}

class _ProTierViewState extends State<ProTierView> {
  final TextEditingController _promoController = TextEditingController();

  void _applyPromo() {
    final code = _promoController.text.trim().toUpperCase();
    if (['ATTIA20', 'GOGGINS', 'ATOMIC', 'PULSE'].contains(code)) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('🎉 Promo Code "$code" Applied! Extra 20% discount activated.'),
          backgroundColor: AppColors.emerald,
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('❌ Invalid or expired promo code.'),
          backgroundColor: Colors.redAccent,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final bool isAnnual = widget.provider.isAnnualBilling;
    final String proPrice = isAnnual ? '\$11.25' : '\$14.99';
    final String proSubtext = isAnnual ? 'per month, billed annually (\$135/yr)' : 'per month, billed monthly';
    final String elitePrice = isAnnual ? '\$29.99' : '\$39.99';
    final String eliteSubtext = isAnnual ? 'per month, billed annually (\$359/yr)' : 'per month, billed monthly';

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '💎 Unlock Full Potential with PULSE Pro & Elite',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.w800,
              color: AppColors.textLight,
            ),
          ),
          const SizedBox(height: 4),
          const Text(
            'Scale your physical transformation with continuous biomarker telemetry and automated grocery delivery.',
            style: TextStyle(color: AppColors.textMuted, fontSize: 13.5),
          ),
          const SizedBox(height: 16),

          // Billing Interval Toggle
          Row(
            children: [
              ChoiceChip(
                label: const Text('Monthly Billing'),
                selected: !isAnnual,
                selectedColor: AppColors.emerald.withOpacity(0.3),
                backgroundColor: AppColors.bgDarkSecondary,
                labelStyle: TextStyle(
                  color: !isAnnual ? AppColors.softMint : AppColors.textMuted,
                  fontWeight: !isAnnual ? FontWeight.w700 : FontWeight.w500,
                ),
                side: BorderSide(color: !isAnnual ? AppColors.emerald : AppColors.cardBorder),
                onSelected: (_) => widget.provider.toggleBillingCycle(false),
              ),
              const SizedBox(width: 12),
              ChoiceChip(
                label: const Text('Annual Billing (Save 25%)'),
                selected: isAnnual,
                selectedColor: AppColors.emerald.withOpacity(0.3),
                backgroundColor: AppColors.bgDarkSecondary,
                labelStyle: TextStyle(
                  color: isAnnual ? AppColors.softMint : AppColors.textMuted,
                  fontWeight: isAnnual ? FontWeight.w700 : FontWeight.w500,
                ),
                side: BorderSide(color: isAnnual ? AppColors.emerald : AppColors.cardBorder),
                onSelected: (_) => widget.provider.toggleBillingCycle(true),
              ),
            ],
          ),

          const SizedBox(height: 18),

          // Pricing Grid
          LayoutBuilder(
            builder: (context, constraints) {
              final bool isWide = constraints.maxWidth > 850;
              final double cardWidth = isWide ? (constraints.maxWidth - 32) / 3 : constraints.maxWidth;

              return Wrap(
                spacing: 16,
                runSpacing: 16,
                children: [
                  // 1. Starter Free Tier
                  SizedBox(
                    width: cardWidth,
                    child: GlassCard(
                      padding: const EdgeInsets.all(22),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              MetricBadge(label: 'STARTER', type: MetricBadgeType.cyan),
                              Text('Forever Free', style: TextStyle(color: AppColors.textMuted, fontSize: 12)),
                            ],
                          ),
                          const SizedBox(height: 12),
                          const Text(
                            '\$0',
                            style: TextStyle(fontSize: 32, fontWeight: FontWeight.w800, color: AppColors.textLight),
                          ),
                          const Text('Free lifetime access', style: TextStyle(color: AppColors.textMuted, fontSize: 12)),
                          const SizedBox(height: 16),
                          const Divider(color: AppColors.cardBorder),
                          const SizedBox(height: 12),
                          _featureLine('✅ Scientific Mifflin-St Jeor TDEE'),
                          _featureLine('✅ 1.6–2.2g/kg Protein Targeter'),
                          _featureLine('✅ 5 AI Meal Generations / Day'),
                          _featureLine('✅ Basic Mindset Book Quotes'),
                          _featureLine('❌ AI Voice Bio-Coach', isDimmed: true),
                          _featureLine('❌ Auto-Grocery Delivery Export', isDimmed: true),
                          const SizedBox(height: 24),
                          SizedBox(
                            width: double.infinity,
                            child: ElevatedButton(
                              onPressed: null,
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AppColors.bgDarkSecondary,
                                disabledBackgroundColor: AppColors.bgDarkSecondary,
                                disabledForegroundColor: AppColors.textMuted,
                              ),
                              child: const Text('Current Active Plan'),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),

                  // 2. PULSE Pro Tier (Central Column)
                  SizedBox(
                    width: cardWidth,
                    child: GlassCard(
                      borderColor: AppColors.emerald,
                      backgroundGradient: AppGradients.proCardGradient,
                      padding: const EdgeInsets.all(22),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              const MetricBadge(label: 'MOST POPULAR', type: MetricBadgeType.green),
                              if (isAnnual)
                                const MetricBadge(label: '25% OFF', type: MetricBadgeType.amber)
                              else
                                const Text('Flexible Monthly', style: TextStyle(color: AppColors.textMuted, fontSize: 12)),
                            ],
                          ),
                          const SizedBox(height: 12),
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.baseline,
                            textBaseline: TextBaseline.alphabetic,
                            children: [
                              Text(
                                proPrice,
                                style: const TextStyle(fontSize: 32, fontWeight: FontWeight.w800, color: AppColors.softMint),
                              ),
                              const Text(' / mo', style: TextStyle(fontSize: 14, color: AppColors.textMuted)),
                            ],
                          ),
                          Text(proSubtext, style: const TextStyle(color: AppColors.softMint, fontSize: 12, fontWeight: FontWeight.w500)),
                          const SizedBox(height: 16),
                          const Divider(color: AppColors.cardBorder),
                          const SizedBox(height: 12),
                          _featureLine('✅ Unlimited Gemini 2.5 Flash Chef'),
                          _featureLine('✅ Full Book RAG Semantic Retrieval'),
                          _featureLine('✅ 🛒 1-Click Instacart / Amazon Fresh'),
                          _featureLine('✅ 🧬 Biomarker & Bloodwork Sync'),
                          _featureLine('✅ Custom Supplement Stacking Engine'),
                          const SizedBox(height: 24),
                          SizedBox(
                            width: double.infinity,
                            child: ElevatedButton(
                              onPressed: () {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(
                                    content: Text('🎉 Redirecting to Stripe Checkout (Simulation)...'),
                                    backgroundColor: AppColors.emerald,
                                  ),
                                );
                              },
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AppColors.emerald,
                                foregroundColor: Colors.white,
                              ),
                              child: const Text('🚀 Upgrade to PULSE Pro'),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),

                  // 3. Longevity Elite Tier
                  SizedBox(
                    width: cardWidth,
                    child: GlassCard(
                      borderColor: AppColors.brightAqua,
                      backgroundGradient: AppGradients.eliteCardGradient,
                      padding: const EdgeInsets.all(22),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              const MetricBadge(label: 'LONGEVITY ELITE', type: MetricBadgeType.cyan),
                              if (isAnnual)
                                const MetricBadge(label: '25% OFF', type: MetricBadgeType.amber)
                              else
                                const Text('All-Inclusive', style: TextStyle(color: AppColors.textMuted, fontSize: 12)),
                            ],
                          ),
                          const SizedBox(height: 12),
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.baseline,
                            textBaseline: TextBaseline.alphabetic,
                            children: [
                              Text(
                                elitePrice,
                                style: const TextStyle(fontSize: 32, fontWeight: FontWeight.w800, color: AppColors.brightAqua),
                              ),
                              const Text(' / mo', style: TextStyle(fontSize: 14, color: AppColors.textMuted)),
                            ],
                          ),
                          Text(eliteSubtext, style: const TextStyle(color: AppColors.brightAqua, fontSize: 12, fontWeight: FontWeight.w500)),
                          const SizedBox(height: 16),
                          const Divider(color: AppColors.cardBorder),
                          const SizedBox(height: 12),
                          _featureLine('✅ Everything in PULSE Pro'),
                          _featureLine('✅ 🎙️ 24/7 AI Voice Bio-Coach'),
                          _featureLine('✅ 🩺 Continuous Glucose (CGM) Sync'),
                          _featureLine('✅ 👨‍⚕️ Monthly 1-on-1 Nutritionist Review'),
                          _featureLine('✅ Priority VIP Concierge Support'),
                          const SizedBox(height: 24),
                          SizedBox(
                            width: double.infinity,
                            child: ElevatedButton(
                              onPressed: () {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(
                                    content: Text('⚡ Elite Concierge Onboarding Activated!'),
                                    backgroundColor: AppColors.cyan,
                                  ),
                                );
                              },
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AppColors.oceanCyan,
                                foregroundColor: Colors.white,
                              ),
                              child: const Text('👑 Join Longevity Elite'),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              );
            },
          ),

          const SizedBox(height: 24),

          // Promo Code Tester
          GlassCard(
            padding: const EdgeInsets.all(18),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _promoController,
                    decoration: const InputDecoration(
                      hintText: 'Enter promo code (e.g. ATTIA20, GOGGINS, ATOMIC, PULSE)...',
                      prefixIcon: Icon(Icons.discount_outlined, color: AppColors.cyan),
                    ),
                  ),
                ),
                const SizedBox(width: 14),
                ElevatedButton(
                  onPressed: _applyPromo,
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                  ),
                  child: const Text('Apply Code'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _featureLine(String text, {bool isDimmed = false}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Text(
        text,
        style: TextStyle(
          color: isDimmed ? AppColors.textSubtle : AppColors.textLight,
          fontSize: 13,
          height: 1.4,
        ),
      ),
    );
  }
}
