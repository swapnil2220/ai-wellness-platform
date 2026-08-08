import 'package:flutter/material.dart';
import '../state/wellness_provider.dart';
import '../theme/app_theme.dart';
import 'macro_tracker_view.dart';
import 'meal_builder_view.dart';
import 'book_rag_view.dart';
import 'pro_tier_view.dart';

class HomeDashboardScreen extends StatefulWidget {
  final WellnessProvider provider;

  const HomeDashboardScreen({super.key, required this.provider});

  @override
  State<HomeDashboardScreen> createState() => _HomeDashboardScreenState();
}

class _HomeDashboardScreenState extends State<HomeDashboardScreen> {
  @override
  void initState() {
    super.initState();
    widget.provider.addListener(_onStateChange);
  }

  @override
  void dispose() {
    widget.provider.removeListener(_onStateChange);
    super.dispose();
  }

  void _onStateChange() {
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    final int activeTab = widget.provider.currentTabIndex;

    final List<Widget> views = [
      MacroTrackerView(provider: widget.provider),
      MealBuilderView(provider: widget.provider),
      BookRagView(provider: widget.provider),
      ProTierView(provider: widget.provider),
    ];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: AppColors.bgDarkSecondary,
        elevation: 0,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: AppColors.emerald.withOpacity(0.2),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: AppColors.emerald.withOpacity(0.4)),
              ),
              child: const Text('🌿', style: TextStyle(fontSize: 18)),
            ),
            const SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: const [
                Text(
                  'PULSE AI',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 0.5,
                    color: AppColors.textLight,
                  ),
                ),
                Text(
                  'High-Protein Metabolic Engine & Book RAG',
                  style: TextStyle(
                    fontSize: 11,
                    color: AppColors.softMint,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
          ],
        ),
        actions: [
          Container(
            margin: const EdgeInsets.only(right: 16),
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: AppColors.cyan.withOpacity(0.15),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: AppColors.cyan.withOpacity(0.4)),
            ),
            child: Row(
              children: const [
                Icon(Icons.spa_outlined, color: AppColors.brightAqua, size: 16),
                SizedBox(width: 6),
                Text(
                  'Soothing Mode',
                  style: TextStyle(color: AppColors.brightAqua, fontSize: 12, fontWeight: FontWeight.w600),
                ),
              ],
            ),
          ),
        ],
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          final bool isDesktop = constraints.maxWidth > 800;

          if (isDesktop) {
            return Row(
              children: [
                NavigationRail(
                  backgroundColor: AppColors.bgDarkSecondary,
                  selectedIndex: activeTab,
                  onDestinationSelected: (idx) => widget.provider.setTabIndex(idx),
                  labelType: NavigationRailLabelType.all,
                  selectedIconTheme: const IconThemeData(color: AppColors.softMint),
                  unselectedIconTheme: const IconThemeData(color: AppColors.textMuted),
                  selectedLabelTextStyle: const TextStyle(color: AppColors.softMint, fontWeight: FontWeight.w700, fontSize: 12),
                  unselectedLabelTextStyle: const TextStyle(color: AppColors.textMuted, fontSize: 11.5),
                  destinations: const [
                    NavigationRailDestination(
                      icon: Icon(Icons.analytics_outlined),
                      selectedIcon: Icon(Icons.analytics),
                      label: Text('Macro Tracker'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.restaurant_menu_outlined),
                      selectedIcon: Icon(Icons.restaurant_menu),
                      label: Text('AI Meal Builder'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.menu_book_outlined),
                      selectedIcon: Icon(Icons.menu_book),
                      label: Text('Mindset RAG'),
                    ),
                    NavigationRailDestination(
                      icon: Icon(Icons.diamond_outlined),
                      selectedIcon: Icon(Icons.diamond),
                      label: Text('Pro Tier'),
                    ),
                  ],
                ),
                const VerticalDivider(thickness: 1, width: 1, color: AppColors.cardBorder),
                Expanded(child: views[activeTab]),
              ],
            );
          } else {
            return views[activeTab];
          }
        },
      ),
      bottomNavigationBar: LayoutBuilder(
        builder: (context, constraints) {
          if (constraints.maxWidth > 800) return const SizedBox.shrink();
          return NavigationBar(
            backgroundColor: AppColors.bgDarkSecondary,
            indicatorColor: AppColors.emerald.withOpacity(0.3),
            selectedIndex: activeTab,
            onDestinationSelected: (idx) => widget.provider.setTabIndex(idx),
            destinations: const [
              NavigationDestination(
                icon: Icon(Icons.analytics_outlined, color: AppColors.textMuted),
                selectedIcon: Icon(Icons.analytics, color: AppColors.softMint),
                label: 'Tracker',
              ),
              NavigationDestination(
                icon: Icon(Icons.restaurant_menu_outlined, color: AppColors.textMuted),
                selectedIcon: Icon(Icons.restaurant_menu, color: AppColors.softMint),
                label: 'Meals',
              ),
              NavigationDestination(
                icon: Icon(Icons.menu_book_outlined, color: AppColors.textMuted),
                selectedIcon: Icon(Icons.menu_book, color: AppColors.brightAqua),
                label: 'RAG Mindset',
              ),
              NavigationDestination(
                icon: Icon(Icons.diamond_outlined, color: AppColors.textMuted),
                selectedIcon: Icon(Icons.diamond, color: AppColors.brightAqua),
                label: 'Pro',
              ),
            ],
          );
        },
      ),
    );
  }
}
