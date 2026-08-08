"""
Unit tests for core/book_rag.py
Verifies vector indexing, semantic search, filtering, and reflection generation.
"""

import pytest
from core.book_rag import BookRAGSystem, BookInsight, ReflectionResponse


def test_book_rag_initialization():
    rag = BookRAGSystem()
    assert len(rag.corpus) >= 5
    categories = rag.get_all_categories()
    assert "Habit Formation" in categories
    assert "Longevity & Biology" in categories
    books = rag.get_all_books()
    assert "Atomic Habits" in books
    assert "Outlive: The Science and Art of Longevity" in books


def test_rag_semantic_search():
    rag = BookRAGSystem()
    results = rag.search("protein leucine muscle synthesis mTOR", top_k=2)
    assert len(results) >= 1
    top = results[0]
    assert "Outlive" in top.book_title or "Protein" in top.concept_title


def test_rag_filter_by_book():
    rag = BookRAGSystem()
    results = rag.search("mindset and friction", top_k=3, book_title="Can't Hurt Me")
    for r in results:
        assert r.book_title == "Can't Hurt Me"


def test_rag_generate_micro_reflection_fallback():
    rag = BookRAGSystem()
    prompt = "I feel like skipping my workout and eating junk food late at night."
    reflection = rag.generate_micro_reflection(prompt, api_key="")

    assert isinstance(reflection, ReflectionResponse)
    assert reflection.user_prompt == prompt
    assert len(reflection.three_step_action_plan) == 3
    assert len(reflection.motivational_mantra) > 5
    assert len(reflection.key_book_frameworks) > 0
