import 'package:flutter/material.dart';
import '../models/book_insight.dart';
import '../services/book_rag_service.dart';
import '../state/wellness_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/glass_card.dart';
import '../widgets/metric_badge.dart';
import '../widgets/reflection_card.dart';

class BookRagView extends StatefulWidget {
  final WellnessProvider provider;

  const BookRagView({super.key, required this.provider});

  @override
  State<BookRagView> createState() => _BookRagViewState();
}

class _BookRagViewState extends State<BookRagView> {
  final TextEditingController _searchController = TextEditingController();
  final TextEditingController _promptController = TextEditingController();
  String _selectedPreset = 'I feel like skipping my high-protein meal prep and ordering junk food.';

  final List<String> _presets = [
    'I feel like skipping my high-protein meal prep and ordering junk food.',
    'Struggling with fatigue and low motivation before a heavy training session.',
    'Feeling discouraged after a dietary slip-up yesterday.',
    'Hitting my protein goal when traveling and super busy.',
    'Custom challenge...',
  ];

  @override
  void initState() {
    super.initState();
    _promptController.text = _selectedPreset;
  }

  void _triggerReflection() {
    final prompt = _promptController.text.trim();
    if (prompt.isNotEmpty) {
      widget.provider.generateMicroReflection(prompt);
    }
  }

  @override
  Widget build(BuildContext context) {
    final categories = BookRagService.getCategories();
    final books = BookRagService.getBooks();

    final searchResults = BookRagService.search(
      query: widget.provider.ragSearchQuery,
      category: widget.provider.selectedCategory,
      bookTitle: widget.provider.selectedBook,
    );

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '📖 Mindset & Book Insights RAG Agent',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.w800,
              color: AppColors.textLight,
            ),
          ),
          const SizedBox(height: 4),
          const Text(
            'Semantic literature search across Atomic Habits, Outlive, Can\'t Hurt Me, The Salt Fix, and Why We Sleep.',
            style: TextStyle(color: AppColors.textMuted, fontSize: 13.5),
          ),
          const SizedBox(height: 16),

          // Search & Filter Bar
          GlassCard(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                TextField(
                  controller: _searchController,
                  decoration: const InputDecoration(
                    prefixIcon: Icon(Icons.search, color: AppColors.cyan),
                    hintText: 'Search concepts (e.g. protein mTOR, friction habits, salt hydration, 40% rule)...',
                  ),
                  onChanged: (v) => widget.provider.setRagSearch(v),
                ),
                const SizedBox(height: 12),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: categories.map((cat) {
                      final bool isSelected = widget.provider.selectedCategory == cat;
                      return Padding(
                        padding: const EdgeInsets.only(right: 8),
                        child: FilterChip(
                          label: Text(cat),
                          selected: isSelected,
                          selectedColor: AppColors.emerald.withOpacity(0.3),
                          backgroundColor: AppColors.bgDarkSecondary,
                          labelStyle: TextStyle(
                            color: isSelected ? AppColors.softMint : AppColors.textMuted,
                            fontWeight: isSelected ? FontWeight.w700 : FontWeight.w500,
                            fontSize: 12,
                          ),
                          side: BorderSide(
                            color: isSelected ? AppColors.emerald : AppColors.cardBorder,
                          ),
                          onSelected: (_) => widget.provider.setCategoryFilter(cat),
                        ),
                      );
                    }).toList(),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 18),

          // Curated Book Cards
          LayoutBuilder(
            builder: (context, constraints) {
              final bool isWide = constraints.maxWidth > 750;
              final double cardWidth = isWide ? (constraints.maxWidth - 16) / 2 : constraints.maxWidth;

              return Wrap(
                spacing: 16,
                runSpacing: 14,
                children: searchResults.map((insight) {
                  final bool bookmarked = widget.provider.isBookmarked(insight.id);
                  return Container(
                    width: cardWidth,
                    padding: const EdgeInsets.all(18),
                    decoration: BoxDecoration(
                      color: AppColors.cardSurface,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: AppColors.cardBorder),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            MetricBadge(label: insight.bookTitle, type: MetricBadgeType.purple),
                            IconButton(
                              icon: Icon(
                                bookmarked ? Icons.bookmark : Icons.bookmark_border,
                                color: bookmarked ? AppColors.softMint : AppColors.textMuted,
                                size: 20,
                              ),
                              onPressed: () => widget.provider.toggleBookmark(insight),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          insight.conceptTitle,
                          style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 15, color: AppColors.textLight),
                        ),
                        const SizedBox(height: 6),
                        Text(
                          insight.takeaway,
                          style: const TextStyle(color: AppColors.textLight, fontSize: 13, height: 1.4),
                        ),
                        const SizedBox(height: 10),
                        Container(
                          padding: const EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            color: AppColors.emerald.withOpacity(0.08),
                            borderRadius: BorderRadius.circular(8),
                            border: const Border(left: BorderSide(color: AppColors.emerald, width: 2.5)),
                          ),
                          child: Text(
                            'Actionable Protocol: ${insight.actionableProtocol}',
                            style: const TextStyle(color: AppColors.softMint, fontSize: 12),
                          ),
                        ),
                        const SizedBox(height: 10),
                        Text(
                          '"${insight.quote}"',
                          style: const TextStyle(fontStyle: FontStyle.italic, color: AppColors.iceCyan, fontSize: 12),
                        ),
                      ],
                    ),
                  );
                }).toList(),
              );
            },
          ),

          const SizedBox(height: 24),
          const Divider(color: AppColors.cardBorder),
          const SizedBox(height: 14),

          // AI Micro-Reflection & Coach Section
          const Text(
            '🧠 AI Micro-Reflection & Mindset Coach',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w800,
              color: AppColors.textLight,
            ),
          ),
          const SizedBox(height: 4),
          const Text(
            'Synthesize a 3-step immediate action plan to overcome friction and cravings.',
            style: TextStyle(color: AppColors.textMuted, fontSize: 13),
          ),
          const SizedBox(height: 12),

          GlassCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                DropdownButtonFormField<String>(
                  value: _selectedPreset,
                  isExpanded: true,
                  items: _presets.map((p) => DropdownMenuItem(value: p, child: Text(p, style: const TextStyle(fontSize: 13)))).toList(),
                  onChanged: (v) {
                    setState(() {
                      _selectedPreset = v!;
                      if (_selectedPreset != 'Custom challenge...') {
                        _promptController.text = _selectedPreset;
                      } else {
                        _promptController.clear();
                      }
                    });
                  },
                ),
                if (_selectedPreset == 'Custom challenge...') ...[
                  const SizedBox(height: 12),
                  TextField(
                    controller: _promptController,
                    maxLines: 2,
                    decoration: const InputDecoration(
                      hintText: 'Describe your current mindset or dietary obstacle...',
                    ),
                  ),
                ],
                const SizedBox(height: 14),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: _triggerReflection,
                    icon: const Icon(Icons.flash_on, size: 18),
                    label: const Text('⚡ Synthesize Book-Backed Action Protocol'),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 16),

          if (widget.provider.latestReflection != null)
            ReflectionCardWidget(reflection: widget.provider.latestReflection!),
        ],
      ),
    );
  }
}
