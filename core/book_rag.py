"""
Mindset & Book Insights RAG Agent (core/book_rag.py)
---------------------------------------------------
Vector search and semantic retrieval engine indexing core frameworks, scientific protocols,
and actionable wisdom from top wellness and mindset books:
- Atomic Habits (James Clear)
- Outlive: The Science and Art of Longevity (Dr. Peter Attia)
- Can't Hurt Me (David Goggins)
- The Salt Fix (Dr. James DiNicolantonio)
- Mindset: The New Psychology of Success (Carol Dweck)
- Why We Sleep (Matthew Walker)
- Deep Work (Cal Newport)

Features TF-IDF/cosine similarity in-memory RAG with book/theme filters,
and dynamic micro-reflection generation via Gemini 2.5 Flash with offline synthesis fallback.
"""

import os
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class BookInsight(BaseModel):
    id: str
    book_title: str
    author: str
    category: str
    concept_title: str
    takeaway: str
    actionable_protocol: str
    quote: str
    relevance_score: Optional[float] = None


class ReflectionResponse(BaseModel):
    user_prompt: str
    reflection_summary: str
    key_book_frameworks: List[BookInsight]
    three_step_action_plan: List[str]
    motivational_mantra: str
    source_citation: str


# Comprehensive Curated Knowledge Base
KNOWLEDGE_BASE: List[Dict[str, str]] = [
    {
        "id": "atomic_habits_identity",
        "book_title": "Atomic Habits",
        "author": "James Clear",
        "category": "Habit Formation",
        "concept_title": "Identity-Based Habits & The 2-Minute Rule",
        "takeaway": "True behavior change is identity change. Every high-protein meal logged and every workout completed is a vote for the type of person you are becoming. Never negotiate with friction: scale down habits until they take under 2 minutes to start.",
        "actionable_protocol": "When motivation dips, do not aim for a flawless 90-minute session. Simply put your shoes on and step inside the gym, or prep one single high-protein shake. Protect the habit streak at all costs.",
        "quote": "You do not rise to the level of your goals. You fall to the level of your systems."
    },
    {
        "id": "atomic_habits_friction",
        "book_title": "Atomic Habits",
        "author": "James Clear",
        "category": "Habit Formation",
        "concept_title": "Environment Design & Friction Reduction",
        "takeaway": "Self-control is a muscle that fatigues. Winner athletes design environments where good nutrition is frictionless and poor food choices require excessive effort.",
        "actionable_protocol": "Batch-cook chicken breast or boiled eggs on Sunday; keep whey isolate on the front kitchen counter and eliminate ultra-processed snacks from your immediate visual field.",
        "quote": "Environment is the invisible hand that shapes human behavior."
    },
    {
        "id": "outlive_protein_mtor",
        "book_title": "Outlive: The Science and Art of Longevity",
        "author": "Dr. Peter Attia",
        "category": "Longevity & Biology",
        "concept_title": "The Protein Threshold & Sarcopenia Prevention",
        "takeaway": "Muscle mass and VO2 max are the single greatest predictors of longevity and healthspan. To stimulate Muscle Protein Synthesis (MPS), you need a minimum of ~30g–40g of intact protein per meal containing 2.5g–3.5g of leucine to cross the mTOR threshold.",
        "actionable_protocol": "Consume 1.6g to 2.2g of protein per kg of body weight daily, distributed across 3 to 4 distinct feeding windows rather than grazing on low-protein snacks throughout the day.",
        "quote": "Muscle is the currency of longevity. You cannot afford to be bankrupt when you are eighty."
    },
    {
        "id": "outlive_zone2",
        "book_title": "Outlive: The Science and Art of Longevity",
        "author": "Dr. Peter Attia",
        "category": "Longevity & Biology",
        "concept_title": "Zone 2 Training & Mitochondrial Density",
        "takeaway": "Zone 2 aerobic training expands mitochondrial efficiency, enabling your body to clear lactate and burn fat as fuel while preserving glycogen for high-intensity efforts.",
        "actionable_protocol": "Accumulate 150 to 200 minutes of Zone 2 cardio per week (a pace where you can still speak in full sentences, but barely).",
        "quote": "Medicine 3.0 focuses on extending your healthspan—the period of life spent free from chronic disease—not just lifespan."
    },
    {
        "id": "goggins_40_percent",
        "book_title": "Can't Hurt Me",
        "author": "David Goggins",
        "category": "Mental Toughness",
        "concept_title": "The 40% Rule & The Accountability Mirror",
        "takeaway": "When your mind tells you you are exhausted, starving, or ready to quit, you have only tapped into roughly 40% of your actual physiological and psychological capacity. The governor in your brain tries to protect you from pain.",
        "actionable_protocol": "When physical or dietary friction strikes, acknowledge the voice of weakness, breathe through the discomfort for 30 seconds, and execute the next mandatory action immediately without debate.",
        "quote": "Don't stop when you're tired. Stop when you're done."
    },
    {
        "id": "goggins_cookie_jar",
        "book_title": "Can't Hurt Me",
        "author": "David Goggins",
        "category": "Mental Toughness",
        "concept_title": "The Cookie Jar & Callousing the Mind",
        "takeaway": "Store every past struggle, tough workout, and difficult obstacle you have overcome in your mental 'Cookie Jar'. Reach into it when you feel overwhelmed by a tough training block or strict nutritional discipline.",
        "actionable_protocol": "Keep a written log of moments where you persevered despite self-doubt. Read one entry before challenging physical tests.",
        "quote": "You are in danger of living a life so comfortable and soft, that you will die without ever realizing your true potential."
    },
    {
        "id": "salt_fix_electrolytes",
        "book_title": "The Salt Fix",
        "author": "Dr. James DiNicolantonio",
        "category": "Hydration & Electrolytes",
        "concept_title": "Electrolyte Balance in Active & High-Protein Metabolism",
        "takeaway": "Salt restriction triggers insulin resistance, elevated resting heart rate, and sympathetic stress. Active individuals consuming high-protein diets require optimal sodium (3g–5g daily) to power the cellular sodium-potassium pump and support amino acid transport.",
        "actionable_protocol": "Add 500mg–1000mg of pure sodium (flaky sea salt or electrolyte powder) to 750ml water 45 minutes before strenuous training.",
        "quote": "We do not have a salt problem; we have a refined sugar and processed food problem masquerading as sodium sensitivity."
    },
    {
        "id": "mindset_growth",
        "book_title": "Mindset: The New Psychology of Success",
        "author": "Carol Dweck",
        "category": "Mindset & Growth",
        "concept_title": "Growth Mindset vs. Fixed Mindset in Physical Transformation",
        "takeaway": "In a growth mindset, challenges and temporary nutritional slip-ups are not indictments of your character—they are biological feedback loops that refine your strategy.",
        "actionable_protocol": "Replace 'I failed my diet today' with 'What specific trigger caused this slip, and how can I re-engineer my environment before tomorrow morning?'",
        "quote": "Becoming is better than being. The passion for stretching yourself and sticking to it is the hallmark of the growth mindset."
    },
    {
        "id": "why_we_sleep_hormones",
        "book_title": "Why We Sleep",
        "author": "Matthew Walker",
        "category": "Sleep & Recovery",
        "concept_title": "Sleep Deprivation, Ghrelin, Leptin & Muscle Repair",
        "takeaway": "Sleeping under 7 hours drops leptin (satiety hormone) and spikes ghrelin (hunger hormone), triggering a primal 300+ kcal craving for refined carbs while blunting growth hormone secretion needed for protein synthesis.",
        "actionable_protocol": "Establish a consistent 8-hour sleep opportunity window in a pitch-black room at 18°C (65°F). Turn off screens 60 minutes prior.",
        "quote": "Sleep is the single most effective thing we can do to reset our brain and body health each day."
    },
    {
        "id": "deep_work_focus",
        "book_title": "Deep Work",
        "author": "Cal Newport",
        "category": "Focus & Habits",
        "concept_title": "Time-Blocking & Nutritional Solitude",
        "takeaway": "Treat your daily meal preparation, hydration, and resistance training as protected deep blocks that cannot be interrupted by low-value digital noise.",
        "actionable_protocol": "Block a recurring 45-minute calendar slot for daily meal prep and treat it with the same sanctity as an executive meeting.",
        "quote": "If you don’t produce, you won’t thrive—no matter how skilled or talented you are."
    }
]


class BookRAGSystem:
    """In-memory Vector RAG engine with TF-IDF semantic search and reflection generation."""

    def __init__(self):
        self.corpus = KNOWLEDGE_BASE
        self.documents = [
            f"{item['book_title']} by {item['author']}. Category: {item['category']}. "
            f"Concept: {item['concept_title']}. Takeaway: {item['takeaway']} "
            f"Protocol: {item['actionable_protocol']} Quote: {item['quote']}"
            for item in self.corpus
        ]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

    def search(
        self,
        query: str,
        top_k: int = 3,
        category: Optional[str] = None,
        book_title: Optional[str] = None
    ) -> List[BookInsight]:
        """Retrieve the most semantically relevant book insights."""
        if not query.strip():
            # Return top default entries
            matches = []
            for item in self.corpus[:top_k]:
                matches.append(BookInsight(**item, relevance_score=1.0))
            return matches

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]

        ranked_indices = similarities.argsort()[::-1]
        results: List[BookInsight] = []

        for idx in ranked_indices:
            item = self.corpus[idx]
            score = float(similarities[idx])

            # Apply filters
            if category and category.lower() != "all" and item["category"].lower() != category.lower():
                continue
            if book_title and book_title.lower() != "all" and item["book_title"].lower() != book_title.lower():
                continue

            results.append(BookInsight(
                id=item["id"],
                book_title=item["book_title"],
                author=item["author"],
                category=item["category"],
                concept_title=item["concept_title"],
                takeaway=item["takeaway"],
                actionable_protocol=item["actionable_protocol"],
                quote=item["quote"],
                relevance_score=round(score, 3)
            ))

            if len(results) >= top_k:
                break

        return results

    def get_all_categories(self) -> List[str]:
        return sorted(list({item["category"] for item in self.corpus}))

    def get_all_books(self) -> List[str]:
        return sorted(list({item["book_title"] for item in self.corpus}))

    def generate_micro_reflection(
        self,
        user_prompt: str,
        api_key: Optional[str] = None
    ) -> ReflectionResponse:
        """
        Generate contextual 3-step action steps and reflection using RAG context.
        Integrates Gemini 2.5 Flash if available, with instant fallback synthesis.
        """
        top_insights = self.search(user_prompt, top_k=3)
        effective_api_key = api_key or os.environ.get("GEMINI_API_KEY")

        # Fallback synthesis if no API key or offline
        if not effective_api_key or "your_gemini" in effective_api_key.lower() or len(effective_api_key.strip()) < 10:
            return self._synthesize_offline_reflection(user_prompt, top_insights)

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=effective_api_key)

            context_str = "\n\n".join([
                f"- Book: '{i.book_title}' ({i.author}) | Concept: {i.concept_title}\n"
                f"  Takeaway: {i.takeaway}\n"
                f"  Protocol: {i.actionable_protocol}\n"
                f"  Quote: \"{i.quote}\""
                for i in top_insights
            ])

            prompt = f"""
You are an elite cognitive-behavioral wellness and high-performance coach.
A user has shared their current challenge or reflection prompt:
"{user_prompt}"

Here is the retrieved literature context from seminal books:
{context_str}

Synthesize a deeply motivational, grounded, and immediately actionable response matching this JSON schema:
{{
  "reflection_summary": "string (2-3 sentences connecting their challenge to the scientific/mindset principles)",
  "three_step_action_plan": [
    "Step 1: Immediate action within 5 minutes",
    "Step 2: Nutrition/Environment setup for today",
    "Step 3: Mindset anchor to repeat when friction arises"
  ],
  "motivational_mantra": "string (A punchy 1-line quote or mental cue)",
  "source_citation": "string (e.g. Synthesized from Atomic Habits & Outlive)"
}}
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.3,
                ),
            )

            import json
            data = json.loads(response.text or "{}")

            return ReflectionResponse(
                user_prompt=user_prompt,
                reflection_summary=data.get(
                    "reflection_summary",
                    "Your current friction is a natural biological threshold. By applying intentional environment design and high-protein fueling, you regain total momentum."
                ),
                key_book_frameworks=top_insights,
                three_step_action_plan=data.get("three_step_action_plan", [
                    "Drink 500ml of cold water with a pinch of sea salt to re-hydrate the brain.",
                    "Eat a 35g+ high-protein meal or shake to suppress ghrelin spikes and trigger mTOR.",
                    "Repeat Goggins' rule: You are only at 40% of your real capacity—execute the next step."
                ]),
                motivational_mantra=data.get(
                    "motivational_mantra",
                    "Every high-protein meal and disciplined decision is a vote for your future self."
                ),
                source_citation=data.get(
                    "source_citation",
                    f"Synthesized from {top_insights[0].book_title if top_insights else 'Seminal Wellness Literature'}"
                )
            )

        except Exception:
            return self._synthesize_offline_reflection(user_prompt, top_insights)

    def _synthesize_offline_reflection(
        self,
        user_prompt: str,
        top_insights: List[BookInsight]
    ) -> ReflectionResponse:
        """Deterministic offline synthesis of top retrieved book wisdom."""
        primary = top_insights[0] if top_insights else BookInsight(
            id="default",
            book_title="Atomic Habits",
            author="James Clear",
            category="Habit Formation",
            concept_title="Identity-Based Action",
            takeaway="Action creates motivation, not the other way around.",
            actionable_protocol="Scale the friction down to a 2-minute step.",
            quote="You do not rise to the level of your goals. You fall to the level of your systems."
        )

        second = top_insights[1] if len(top_insights) > 1 else primary

        return ReflectionResponse(
            user_prompt=user_prompt,
            reflection_summary=(
                f"When addressing '{user_prompt}', the literature indicates that friction is simply the mind's governor testing your systems. "
                f"As {primary.author} emphasizes in '{primary.book_title}', {primary.takeaway.lower()}"
            ),
            key_book_frameworks=top_insights,
            three_step_action_plan=[
                f"Immediate 5-Min Step: {primary.actionable_protocol}",
                f"Metabolic / Nutrition Setup: {second.actionable_protocol}",
                f"Mental Anchor: Remember—'{primary.quote}'"
            ],
            motivational_mantra=primary.quote,
            source_citation=f"Synthesized from '{primary.book_title}' ({primary.author}) & '{second.book_title}' ({second.author})"
        )
