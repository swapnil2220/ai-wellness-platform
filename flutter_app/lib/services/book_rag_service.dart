import '../models/book_insight.dart';

class BookRagService {
  static const List<BookInsight> _corpus = [
    BookInsight(
      id: 'atomic_habits_identity',
      bookTitle: 'Atomic Habits',
      author: 'James Clear',
      category: 'Habit Formation',
      conceptTitle: 'Identity-Based Habits & The 2-Minute Rule',
      takeaway: 'True behavior change is identity change. Every high-protein meal logged and workout completed is a vote for your future self.',
      actionableProtocol: 'Scale down habits until they take under 2 minutes to start. Put shoes on or prep one high-protein shake.',
      quote: 'You do not rise to the level of your goals. You fall to the level of your systems.',
    ),
    BookInsight(
      id: 'atomic_habits_friction',
      bookTitle: 'Atomic Habits',
      author: 'James Clear',
      category: 'Habit Formation',
      conceptTitle: 'Environment Design & Friction Reduction',
      takeaway: 'Self-control is a muscle that fatigues. Winner athletes design environments where good nutrition is frictionless.',
      actionableProtocol: 'Batch-cook lean protein on Sunday; keep whey isolate on the counter and eliminate ultra-processed snacks from view.',
      quote: 'Environment is the invisible hand that shapes human behavior.',
    ),
    BookInsight(
      id: 'outlive_protein_mtor',
      bookTitle: 'Outlive: The Science and Art of Longevity',
      author: 'Dr. Peter Attia',
      category: 'Longevity & Biology',
      conceptTitle: 'The Protein Threshold & Sarcopenia Prevention',
      takeaway: 'Muscle mass is the single greatest biomarker of longevity. You need ~30g–40g of protein containing ~3g leucine per meal to trigger mTOR/MPS.',
      actionableProtocol: 'Consume 1.6g to 2.2g of protein per kg of body weight daily, distributed across 3 to 4 distinct feeding windows.',
      quote: 'Muscle is the currency of longevity. You cannot afford to be bankrupt when you are eighty.',
    ),
    BookInsight(
      id: 'outlive_zone2',
      bookTitle: 'Outlive: The Science and Art of Longevity',
      author: 'Dr. Peter Attia',
      category: 'Longevity & Biology',
      conceptTitle: 'Zone 2 Training & Mitochondrial Density',
      takeaway: 'Zone 2 aerobic training expands mitochondrial efficiency, enabling your body to clear lactate and burn fat as fuel.',
      actionableProtocol: 'Accumulate 150 to 200 minutes of Zone 2 cardio per week (a conversational pace).',
      quote: 'Medicine 3.0 focuses on extending your healthspan—the period of life spent free from chronic disease—not just lifespan.',
    ),
    BookInsight(
      id: 'goggins_40_percent',
      bookTitle: "Can't Hurt Me",
      author: 'David Goggins',
      category: 'Mental Toughness',
      conceptTitle: 'The 40% Rule & The Accountability Mirror',
      takeaway: 'When your mind tells you you are exhausted or starving, you have only tapped into roughly 40% of your actual capacity.',
      actionableProtocol: 'When physical friction strikes, acknowledge the voice of weakness, breathe for 30 seconds, and execute the next mandatory action.',
      quote: "Don't stop when you're tired. Stop when you're done.",
    ),
    BookInsight(
      id: 'salt_fix_electrolytes',
      bookTitle: 'The Salt Fix',
      author: 'Dr. James DiNicolantonio',
      category: 'Hydration & Electrolytes',
      conceptTitle: 'Electrolyte Balance in High-Protein Metabolism',
      takeaway: 'Active individuals consuming high-protein diets require optimal sodium (3g–5g daily) to power the cellular sodium-potassium pump.',
      actionableProtocol: 'Add 500mg–1000mg of pure sodium (flaky sea salt or electrolytes) to 750ml water before strenuous training.',
      quote: 'We do not have a salt problem; we have a refined sugar problem masquerading as sodium sensitivity.',
    ),
    BookInsight(
      id: 'mindset_growth',
      bookTitle: 'Mindset: The New Psychology of Success',
      author: 'Carol Dweck',
      category: 'Mindset & Growth',
      conceptTitle: 'Growth Mindset in Physical Transformation',
      takeaway: 'In a growth mindset, dietary slips are not character flaws—they are biological feedback loops that refine your strategy.',
      actionableProtocol: "Replace 'I failed my diet' with 'What specific trigger caused this, and how do I re-engineer my environment?'",
      quote: 'Becoming is better than being. The passion for stretching yourself is the hallmark of the growth mindset.',
    ),
    BookInsight(
      id: 'why_we_sleep_hormones',
      bookTitle: 'Why We Sleep',
      author: 'Matthew Walker',
      category: 'Sleep & Recovery',
      conceptTitle: 'Sleep Deprivation, Ghrelin & Muscle Repair',
      takeaway: 'Sleeping under 7 hours drops leptin and spikes ghrelin, triggering 300+ kcal cravings while blunting growth hormone secretion.',
      actionableProtocol: 'Establish an 8-hour sleep opportunity window in a pitch-black room at 18°C (65°F). Turn off screens 60 mins prior.',
      quote: 'Sleep is the single most effective thing we can do to reset our brain and body health each day.',
    ),
  ];

  static List<String> getCategories() {
    final set = _corpus.map((e) => e.category).toSet();
    return ['All', ...set];
  }

  static List<String> getBooks() {
    final set = _corpus.map((e) => e.bookTitle).toSet();
    return ['All', ...set];
  }

  static List<BookInsight> search({
    String query = '',
    String category = 'All',
    String bookTitle = 'All',
  }) {
    final cleanQ = query.toLowerCase().trim();

    return _corpus.where((item) {
      if (category != 'All' && item.category != category) return false;
      if (bookTitle != 'All' && item.bookTitle != bookTitle) return false;
      if (cleanQ.isEmpty) return true;

      final fullText = '${item.bookTitle} ${item.author} ${item.category} ${item.conceptTitle} ${item.takeaway} ${item.actionableProtocol} ${item.quote}'.toLowerCase();
      return fullText.contains(cleanQ);
    }).toList();
  }

  static ReflectionResponse generateReflection(String userPrompt) {
    final results = search(query: userPrompt);
    final primary = results.isNotEmpty ? results.first : _corpus.first;
    final second = results.length > 1 ? results[1] : _corpus[1];

    return ReflectionResponse(
      userPrompt: userPrompt,
      reflectionSummary:
          "When addressing '$userPrompt', the literature shows that friction is simply the mind's governor testing your systems. As ${primary.author} emphasizes in '${primary.bookTitle}', ${primary.takeaway.toLowerCase()}",
      keyBookFrameworks: results.take(3).toList(),
      threeStepActionPlan: [
        "Immediate 5-Min Step: ${primary.actionableProtocol}",
        "Metabolic Setup: ${second.actionableProtocol}",
        "Mental Anchor: Remember—'${primary.quote}'",
      ],
      motivationalMantra: primary.quote,
      sourceCitation: "Synthesized from '${primary.bookTitle}' (${primary.author}) & '${second.bookTitle}' (${second.author})",
    );
  }
}
