import 'package:flutter/material.dart';

class AppColors {
  // Soothing Green Palette (Mint, Sage, Emerald)
  static const Color emerald = Color(0xFF10B981);
  static const Color mint = Color(0xFF06D6A0);
  static const Color softMint = Color(0xFF34D399);
  static const Color sageGlow = Color(0xFFA7F3D0);

  // Soothing Cyan Palette (Aqua, Sky, Deep Ocean)
  static const Color cyan = Color(0xFF06B6D4);
  static const Color brightAqua = Color(0xFF22D3EE);
  static const Color oceanCyan = Color(0xFF0891B2);
  static const Color iceCyan = Color(0xFFE0F2FE);

  // Background & Slate Teal Dark Glass Surfaces
  static const Color bgDark = Color(0xFF091219);
  static const Color bgDarkSecondary = Color(0xFF0D1B24);
  static const Color surfaceGlass = Color(0xFF122430);
  static const Color cardSurface = Color(0xFF152A38);
  static const Color cardBorder = Color(0x3322D3EE); // 20% Cyan border

  // Text Accents
  static const Color textLight = Color(0xFFF0FDFA);
  static const Color textMuted = Color(0xFF94A3B8);
  static const Color textSubtle = Color(0xFF64748B);
}

class AppGradients {
  static const LinearGradient heroGradient = LinearGradient(
    colors: [
      Color(0x2410B981), // 14% Emerald
      Color(0x2806B6D4), // 16% Cyan
      Color(0x1F0891B2), // 12% Ocean Cyan
    ],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient primaryButton = LinearGradient(
    colors: [AppColors.emerald, AppColors.oceanCyan],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient proCardGradient = LinearGradient(
    colors: [Color(0x2410B981), Color(0xF0122430)],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );

  static const LinearGradient eliteCardGradient = LinearGradient(
    colors: [Color(0x2606B6D4), Color(0xF0122430)],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );
}

class AppTheme {
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: AppColors.bgDark,
      primaryColor: AppColors.emerald,
      colorScheme: const ColorScheme.dark(
        primary: AppColors.emerald,
        secondary: AppColors.cyan,
        surface: AppColors.surfaceGlass,
        onPrimary: Colors.white,
        onSurface: AppColors.textLight,
      ),
      fontFamily: 'Inter',
      cardTheme: CardTheme(
        color: AppColors.surfaceGlass,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(18),
          side: const BorderSide(color: AppColors.cardBorder, width: 1),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.emerald,
          foregroundColor: Colors.white,
          elevation: 2,
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: const TextStyle(
            fontWeight: FontWeight.w700,
            fontSize: 14,
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AppColors.bgDarkSecondary,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: AppColors.cardBorder),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: AppColors.cardBorder),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: AppColors.brightAqua, width: 1.5),
        ),
        labelStyle: const TextStyle(color: AppColors.textMuted),
        hintStyle: const TextStyle(color: AppColors.textSubtle),
      ),
    );
  }
}
