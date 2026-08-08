import 'package:flutter_test/flutter_test.dart';
import '../lib/services/book_rag_service.dart';

void main() {
  group('BookRagService Unit Tests', () {
    test('Retrieves books and categories', () {
      final categories = BookRagService.getCategories();
      expect(categories.contains('Habit Formation'), true);
      expect(categories.contains('Longevity & Biology'), true);

      final books = BookRagService.getBooks();
      expect(books.contains('Atomic Habits'), true);
      expect(books.contains('Outlive: The Science and Art of Longevity'), true);
    });

    test('Searches by keyword query and category filter', () {
      final results = BookRagService.search(query: 'protein leucine mTOR');
      expect(results.isNotEmpty, true);
      expect(results.first.bookTitle.contains('Outlive'), true);
    });

    test('Generates 3-step actionable micro-reflection protocol', () {
      final reflection = BookRagService.generateReflection(
        'I feel like skipping my workout and eating junk food.',
      );
      expect(reflection.threeStepActionPlan.length, 3);
      expect(reflection.motivationalMantra.isNotEmpty, true);
      expect(reflection.sourceCitation.isNotEmpty, true);
    });
  });
}
