import 'package:flutter/material.dart';
import 'state/wellness_provider.dart';
import 'theme/app_theme.dart';
import 'screens/home_dashboard_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  final provider = WellnessProvider();
  runApp(PulseWellnessApp(provider: provider));
}

class PulseWellnessApp extends StatelessWidget {
  final WellnessProvider provider;

  const PulseWellnessApp({super.key, required this.provider});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PULSE AI - High-Protein & Longevity Platform',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.darkTheme,
      home: HomeDashboardScreen(provider: provider),
    );
  }
}
