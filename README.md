# 🌿 PULSE AI | High-Protein Metabolism & Longevity Platform

PULSE AI is a production-grade, modular wellness platform combining clinical metabolism science, generative AI culinary recipe synthesis, and a cognitive mindset RAG agent. The codebase includes a **Python/Streamlit Web Dashboard** and a **cross-platform Flutter application**, both styled in a soothing **Emerald, Mint, and Cyan** glassmorphism theme.

---

## 🧬 Scientific & Technical Nuances

### 1. Metabolic & Macro Engine
The core calculations are built on clinical nutrition and longevity science (Medicine 3.0 principles):
*   **Basal Metabolic Rate (BMR)**: Calculated using the **Mifflin-St Jeor Equation** for maximum clinical accuracy over older Harris-Benedict formulas:
    $$\text{BMR (Male)} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age (y)} + 5$$
    $$\text{BMR (Female)} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age (y)} - 161$$
*   **Total Daily Energy Expenditure (TDEE)**: Computed by applying physical activity multipliers (Sedentary `1.2x` to Heavy Athlete `1.9x`).
*   **The Leucine Trigger & MPS**: Muscle Protein Synthesis (MPS) is maximally stimulated through the **mTORC1** pathway. To cross the threshold, a meal must contain **2.5g–3.5g of Leucine** (typically found in **28g–35g of High Biological Value protein**). The platform tracks this "Leucine Trigger" for every meal to prevent sarcopenia and preserve lean body mass.
*   **Protein Satiety Standard**: Daily targets enforce **1.6g to 2.2g of protein per kg of bodyweight** to leverage the thermic effect of food (TEF) and defend lean mass during caloric deficits.

### 2. Generative AI Chef & Affiliate Scaling
*   **Google GenAI SDK**: Connects to `gemini-2.5-flash` using structured JSON schema validation.
*   **Offline Fallback Synthesizer**: If no API key is present or the rate limit is hit, a deterministic scaling engine processes a structured local catalog of chicken, salmon, yogurt, and tempeh dishes, scaling ingredients proportionally to match the exact remaining protein/calorie targets.
*   **Ergogenic Affiliate Integration**: Recommends customized clinical supplements based on the dish type (e.g., Creatine Monohydrate for power workouts, Electrolytes for pre-hydration, Omega-3s with fish dishes).

### 3. Mindset RAG (Retrieval-Augmented Generation)
*   **In-Memory Semantic Search**: Vector indexing maps text queries to concept nodes using TF-IDF term frequency and cosine distance similarity.
*   **Indexed Seminal Literature**: Outlive (Peter Attia), Atomic Habits (James Clear), Can't Hurt Me (David Goggins), Mindset (Carol Dweck), The Salt Fix (Dr. DiNicolantonio), and Why We Sleep (Matthew Walker).
*   **AI Cognitive Reframing Coach**: Processes user friction (e.g., late-night cravings, workout fatigue) and generates a 3-step immediate action protocol anchored by literature-backed habit-stacking, friction-reduction, and accountability mirrors.

---

## 🛠️ The Tech Stack

### 🐍 Backend & Web App (Python)
*   **Streamlit**: Highly customized with glassmorphism CSS overlays, interactive Plotly charts, collapsible configurations, and responsive progress bars.
*   **SQLAlchemy ORM**: Connects to a local SQLite instance with schema migrations, caching session generators, and UTC-timestamped entries.
*   **Plotly Express / Graph Objects**: Custom HSL-matched donut charts and double-axis per-meal calorie/protein charts.

### 📱 Mobile & Desktop App (Flutter & Dart)
*   **Layered Architecture**: Strictly follows the UI -> Controller/Provider -> Data/Service separation.
*   **ChangeNotifier State Management**: Provides real-time reactive state updates across profile configuration, meal logging, and bookmarking.
*   **Custom Graphics Canvas**: Implements a custom `CustomPainter` to draw anti-aliased macro calorie breakdown donut charts.
*   **Responsive Shell**: Automatically switches between a sidebar `NavigationRail` (desktop/tablets) and a bottom `NavigationBar` (mobile).

---

## 📂 Project Directory Structure

```
ai-wellness-platform/
├── app.py                         # Python Streamlit Web Dashboard
├── core/
│   ├── protein_engine.py          # Mifflin-St Jeor, BMR, TDEE, & Leucine algorithms
│   ├── meal_planner.py            # Gemini 2.5 Flash SDK wrapper & fallback engine
│   └── book_rag.py                # Cosine vector retrieval & RAG coach
├── database/
│   └── db.py                      # SQLAlchemy ORM, SQLite schema, & transaction layers
├── flutter_app/
│   ├── pubspec.yaml               # Flutter pub dependency manager
│   ├── lib/
│   │   ├── main.dart              # Flutter application entrypoint
│   │   ├── theme/
│   │   │   └── app_theme.dart     # Soothing green & cyan glassmorphism variables
│   │   ├── models/                # Domain data representations
│   │   ├── services/              # Clean Dart ports of calculation engines & RAG
│   │   ├── state/
│   │   │   └── wellness_provider.dart # ChangeNotifier reactive dispatcher
│   │   ├── widgets/               # Reusable recipe cards, progress painters, badges
│   │   └── screens/               # Tracker, Builder, RAG, and Pro pricing views
│   └── test/                      # Dart unit test coverage
├── tests/                         # Pytest integration & unit testing
├── requirements.txt               # Python package manifest
└── README.md                      # Complete system documentation
```

---

## ⚡ Setup & Run Guidelines

### 🐍 running the Python Web Dashboard
1.  **Initialize Environment & Install Packages**:
    ```bash
    source venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Add API Keys (Optional)**:
    Create a `.env` file from the template:
    ```bash
    cp .env.example .env
    ```
    Insert your `GEMINI_API_KEY=...` to enable live AI recipe generation.
3.  **Run Pytest Verification**:
    ```bash
    pytest tests/ -v
    ```
4.  **Boot the Dashboard**:
    ```bash
    streamlit run app.py --server.port 8501
    ```

### 📱 running the Flutter Application
1.  **Retrieve Dependencies**:
    ```bash
    cd flutter_app
    flutter pub get
    ```
2.  **Run Dart Unit Tests**:
    ```bash
    flutter test
    ```
3.  **Launch the App**:
    ```bash
    flutter run
    ```
