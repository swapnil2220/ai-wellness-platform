# PULSE AI — High-Protein & Longevity Wellness Platform

A production-ready, modular MVP combining scientific macronutrient distribution (1.6–2.2g/kg protein targets), Gemini 2.5 Flash culinary meal generation with affiliate supplement links, in-memory TF-IDF vector RAG indexing top wellness literature (*Atomic Habits*, *Outlive*, *Can't Hurt Me*, *The Salt Fix*, *Mindset*, *Why We Sleep*), and an interactive multi-tab Streamlit dashboard.

---

## 🚀 Architecture & Key Features

### 1. User Profile & Scientific Macro Engine (`core/protein_engine.py`)
- **Mifflin-St Jeor Equation** with gender, weight, height, and age baselines.
- **Activity & Goal Adjustments**: Sedentary to Extra Active multipliers; Caloric deficit (-20% fat loss), surplus (+10% muscle gain), or maintenance.
- **1.6g–2.2g/kg Protein Protocol**: Preserves lean body mass, stimulates Diet-Induced Thermogenesis (TEF), and satisfies the per-meal ~2.5g–3.5g leucine trigger threshold (mTOR activation).
- **Interactive Plotly Visualizations**: Calorie/Macro donut breakdown and per-meal allocation bars.

### 2. AI High-Protein Meal Generator (`core/meal_planner.py`)
- **Google GenAI SDK Integration**: Utilizes `gemini-2.5-flash` with structured Pydantic schema validation.
- **Resilient Offline Fallback Engine**: If `GEMINI_API_KEY` is not provided or API is offline, an intelligent recipe engine scales chef-crafted recipes to exact remaining protein and calorie budgets.
- **Affiliate Supplement Integrations**: Recommendations for Native Whey Isolate, Creapure® Creatine Monohydrate, Plant Isolate, and Electrolytes with dosage guidance.
- **One-Click Daily Logging**: Instantly save generated meals into the local SQLite database.

### 3. Mindset & Book Insights RAG Agent (`core/book_rag.py`)
- **In-Memory Vector Search**: TF-IDF and Cosine Similarity retrieval over curated knowledge from:
  - *Atomic Habits* (James Clear)
  - *Outlive: The Science and Art of Longevity* (Dr. Peter Attia)
  - *Can't Hurt Me* (David Goggins)
  - *The Salt Fix* (Dr. James DiNicolantonio)
  - *Mindset* (Carol Dweck)
  - *Why We Sleep* (Matthew Walker)
  - *Deep Work* (Cal Newport)
- **AI Micro-Reflection & Cognitive Coach**: Generates a 3-step immediate action plan and mental mantra when facing dietary friction, workout hesitation, or late-night cravings.

### 4. Monetization & Pro Tier Preview (`app.py` - Tab 4)
- **Tier Comparison Grid**: Starter (Free) vs. PULSE Pro ($14.99/mo) vs. Longevity Elite ($39.99/mo).
- **Pro Feature Spotlights**: AI Voice Bio-Coach, Biomarker & Bloodwork Sync, Automated Instacart/Amazon Fresh Grocery Export, 1-on-1 Nutritionist sync.
- **Interactive Discount & Promo Code Simulator**.

---

## 🛠️ Quickstart & Local Setup

### 1. Virtual Environment & Dependencies
```bash
# Clone or navigate to the directory
cd /Users/swapnilshrivastava/.gemini/antigravity/scratch/ai-wellness-platform

# Activate Python 3.12 virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Optional: Add your `GEMINI_API_KEY=...` to enable live Gemini 2.5 Flash generations. If left blank, the app seamlessly runs in offline smart synthesizer mode).*

### 3. Run the Unit Test Suite
```bash
pytest tests/ -v
```

### 4. Launch the Streamlit Dashboard
```bash
streamlit run app.py --server.port 8501
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📂 Project Directory Structure
```
ai-wellness-platform/
├── app.py                      # Main Streamlit Multi-Tab Dashboard
├── core/
│   ├── __init__.py
│   ├── protein_engine.py       # Macro, TDEE, & 1.6-2.2g/kg Protein Calculation
│   ├── meal_planner.py         # Gemini 2.5 Flash Meal Generator & Fallback Engine
│   └── book_rag.py             # Vector RAG Semantic Engine over Wellness Books
├── database/
│   ├── __init__.py
│   └── db.py                   # SQLAlchemy SQLite ORM & CRUD Repository
├── tests/
│   ├── __init__.py
│   ├── test_protein.py         # Unit tests for macro & TDEE formulas
│   ├── test_meal_planner.py    # Unit tests for recipe generation & schema
│   ├── test_book_rag.py        # Unit tests for vector search & reflections
│   └── test_db.py              # Unit tests for database models & progress tracking
├── .env.example                # Environment variables template
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation & Setup guide
```
