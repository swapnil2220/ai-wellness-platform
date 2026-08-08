class BookInsight {
  final String id;
  final String bookTitle;
  final String author;
  final String category;
  final String conceptTitle;
  final String takeaway;
  final String actionableProtocol;
  final String quote;
  final double relevanceScore;

  const BookInsight({
    required this.id,
    required this.bookTitle,
    required this.author,
    required this.category,
    required this.conceptTitle,
    required this.takeaway,
    required this.actionableProtocol,
    required this.quote,
    this.relevanceScore = 1.0,
  });
}

class ReflectionResponse {
  final String userPrompt;
  final String reflectionSummary;
  final List<BookInsight> keyBookFrameworks;
  final List<String> threeStepActionPlan;
  final String motivationalMantra;
  final String sourceCitation;

  const ReflectionResponse({
    required this.userPrompt,
    required this.reflectionSummary,
    required this.keyBookFrameworks,
    required this.threeStepActionPlan,
    required this.motivationalMantra,
    required this.sourceCitation,
  });
}
