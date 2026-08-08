"""
AI Wellness & High-Protein Platform (app.py)
--------------------------------------------
Production-ready Streamlit frontend dashboard featuring:
1. 📊 Macro Tracker & Metabolism Engine (Mifflin-St Jeor + 1.6-2.2g/kg protein targets + Plotly analytics)
2. 🥗 AI High-Protein Meal Generator (Gemini 2.5 Flash + fallback recipe engine + affiliate supplements)
3. 📖 Mindset & Book Insights RAG Agent (In-memory semantic TF-IDF search across top wellness books + micro-reflections)
4. 💎 Monetization & Pro Tier Preview (Sleek comparison matrix & checkout simulator)
"""

import datetime
import json
import os
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Core modules
from core.protein_engine import (
    Gender,
    ActivityLevel,
    FitnessGoal,
    UserProfileInput,
    calculate_macro_targets,
)
from core.meal_planner import (
    DietaryPreference,
    MealType,
    MealPlanRequest,
    RecipeModel,
    generate_high_protein_meal,
    AFFILIATE_CATALOG,
)
from core.book_rag import (
    BookRAGSystem,
    BookInsight,
    ReflectionResponse,
)
from database.db import (
    get_session,
    init_db,
    save_or_update_profile,
    get_latest_profile,
    log_meal,
    get_today_progress,
    save_favorite_insight,
    get_favorite_insights,
    update_water,
)

# Page configuration
st.set_page_config(
    page_title="PULSE AI | High-Protein & Longevity Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize database
init_db()

# Initialize RAG System in Streamlit Cache
@st.cache_resource
def get_rag_engine():
    return BookRAGSystem()

rag_engine = get_rag_engine()

# Custom CSS for modern soothing green and cyan theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', 'Inter', -apple-system, sans-serif;
    }

    /* Calming Slate Teal Background */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0B1922 0%, #061017 60%, #03080C 100%);
        color: #F0FDFA;
    }

    /* Soothing Hero Header */
    .hero-banner {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.14) 0%, rgba(6, 182, 212, 0.16) 50%, rgba(8, 145, 178, 0.12) 100%);
        border: 1px solid rgba(6, 182, 212, 0.25);
        border-radius: 20px;
        padding: 26px 32px;
        margin-bottom: 24px;
        backdrop-filter: blur(16px);
        box-shadow: 0 12px 36px -12px rgba(6, 182, 212, 0.2);
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(120deg, #34D399 0%, #22D3EE 50%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: #99F6E4;
        font-size: 1.05rem;
        font-weight: 400;
    }

    /* Soothing Glass Cards */
    .glass-card {
        background: rgba(13, 28, 36, 0.72);
        border: 1px solid rgba(6, 182, 212, 0.18);
        border-radius: 18px;
        padding: 22px 26px;
        margin-bottom: 16px;
        backdrop-filter: blur(14px);
        transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .glass-card:hover {
        border-color: rgba(52, 211, 153, 0.45);
        box-shadow: 0 12px 30px -8px rgba(16, 185, 129, 0.18);
        transform: translateY(-2px);
    }

    /* Custom KPI Metric Cards */
    .kpi-card {
        background: rgba(18, 38, 48, 0.65);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 16px;
        padding: 16px 20px;
        text-align: left;
        backdrop-filter: blur(10px);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .kpi-card:hover {
        border-color: rgba(16, 185, 129, 0.4);
        background: rgba(18, 38, 48, 0.8);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.12);
    }
    .kpi-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.65rem;
        font-weight: 800;
        color: #F0FDFA;
    }
    .kpi-subtext {
        font-size: 0.82rem;
        color: #34D399;
        font-weight: 500;
        margin-top: 4px;
    }

    /* Custom Progress Bars */
    .progress-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 9999px;
        height: 8px;
        width: 100%;
        margin-top: 8px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }
    .progress-bar {
        border-radius: 9999px;
        height: 100%;
        transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .progress-bar-protein {
        background: linear-gradient(90deg, #10B981 0%, #06D6A0 100%);
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
    }
    .progress-bar-calories {
        background: linear-gradient(90deg, #06B6D4 0%, #22D3EE 100%);
        box-shadow: 0 0 10px rgba(6, 182, 212, 0.4);
    }

    /* Soothing Metric Badges */
    .metric-pill {
        display: inline-block;
        padding: 5px 13px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .pill-green { background: rgba(16, 185, 129, 0.18); color: #34D399; border: 1px solid rgba(52, 211, 153, 0.45); }
    .pill-blue, .pill-cyan { background: rgba(6, 182, 212, 0.18); color: #22D3EE; border: 1px solid rgba(34, 211, 238, 0.45); }
    .pill-purple { background: rgba(13, 148, 136, 0.22); color: #5EEAD4; border: 1px solid rgba(94, 234, 212, 0.45); }
    .pill-amber { background: rgba(20, 184, 166, 0.25); color: #A7F3D0; border: 1px solid rgba(167, 243, 208, 0.45); }

    /* Recipe & Quote Cards */
    .recipe-header {
        font-size: 1.45rem;
        font-weight: 700;
        color: #F0FDFA;
        margin-bottom: 8px;
    }
    .quote-box {
        border-left: 3px solid #06B6D4;
        padding-left: 16px;
        margin: 14px 0;
        font-style: italic;
        color: #CCFBF1;
        background: rgba(6, 182, 212, 0.05);
        padding-top: 8px;
        padding-bottom: 8px;
        border-radius: 0 10px 10px 0;
    }

    /* Affiliate Badge */
    .affiliate-badge {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.12), rgba(16, 185, 129, 0.12));
        border: 1px solid rgba(34, 211, 238, 0.3);
        border-radius: 14px;
        padding: 14px 18px;
        margin-top: 10px;
    }

    /* Tabs Styling with Mint/Cyan Active Indicators */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(13, 28, 36, 0.6);
        border-radius: 12px;
        padding: 10px 22px;
        font-weight: 600;
        color: #94A3B8;
        border: 1px solid rgba(6, 182, 212, 0.12);
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #5EEAD4;
        border-color: rgba(6, 182, 212, 0.35);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.28), rgba(6, 182, 212, 0.28)) !important;
        color: #22D3EE !important;
        border: 1px solid rgba(34, 211, 238, 0.6) !important;
        box-shadow: 0 4px 16px -4px rgba(6, 182, 212, 0.3);
    }

    /* Primary Buttons with Mint & Cyan Gradient */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease;
    }
    .primary-btn button, button[kind="primary"] {
        background: linear-gradient(135deg, #10B981 0%, #0891B2 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 16px rgba(6, 182, 212, 0.35) !important;
    }

    /* Cleaner Streamlit Expander header styles */
    .st-emotion-cache-1h9us5a, .st-emotion-cache-eq1h2b {
        background-color: rgba(13, 28, 36, 0.4) !important;
        border: 1px solid rgba(6, 182, 212, 0.15) !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)


# Top Navigation / Hero Banner
st.markdown("""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <div class="hero-title">🌿 PULSE AI</div>
            <div class="hero-subtitle">High-Protein Metabolic Engine • Gemini Chef • Soothing Mindset RAG</div>
        </div>
        <div style="margin-top: 8px;">
            <span class="metric-pill pill-green">● 1.6–2.2g/kg Protein Protocol</span>
            <span class="metric-pill pill-cyan">● Gemini 2.5 Flash</span>
            <span class="metric-pill pill-purple">● Medicine 3.0 Science</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Sidebar Configuration & Settings
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    
    # API Key Configuration
    env_key = os.environ.get("GEMINI_API_KEY", "")
    has_env_key = bool(env_key and "your_gemini" not in env_key.lower() and len(env_key.strip()) > 10)
    
    api_key_input = st.text_input(
        "Gemini API Key (Optional)",
        value=env_key if has_env_key else "",
        type="password",
        help="Leave blank to use the built-in offline chef and RAG synthesis engine."
    )
    
    if api_key_input:
        st.success("🟢 Live Gemini 2.5 Flash Active")
    else:
        st.info("🟡 Offline Smart Synthesizer Active")
    
    st.divider()
    st.caption("PULSE AI Platform v1.0.0 • SQLite Persisted")


# Main Tabs Navigation
tab_macro, tab_meals, tab_rag, tab_pro = st.tabs([
    "📊 1. Macro & Metabolism Tracker",
    "🥗 2. AI High-Protein Meal Builder",
    "📖 3. Mindset & Book Insights RAG",
    "💎 4. Pro Tier & Monetization Preview",
])


# ==========================================
# TAB 1: MACRO & METABOLISM TRACKER
# ==========================================
with tab_macro:
    db_session = get_session()
    saved_profile = get_latest_profile(db_session)
    
    # Active Logged-in User Profile Summary Card
    if saved_profile:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #10B981; margin-bottom: 18px; padding: 18px 22px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <span class="metric-pill pill-green" style="margin-bottom: 6px;">👤 ACTIVE USER PROFILE</span>
                    <div style="font-size: 1.25rem; font-weight: 700; color: #F0FDFA; margin-top: 4px;">
                        swapnilshrivastava <span style="font-weight: 400; color: #94A3B8; font-size: 0.95rem;">• {saved_profile.age} yrs • {saved_profile.gender.upper()}</span>
                    </div>
                    <div style="font-size: 0.9rem; color: #94A3B8; margin-top: 6px;">
                        📐 Weight: <b>{saved_profile.weight_kg} kg</b> &nbsp;|&nbsp; 
                        📏 Height: <b>{saved_profile.height_cm} cm</b> &nbsp;|&nbsp; 
                        ⚡ Activity: <b>{saved_profile.activity_level.replace('_', ' ').title()}</b> &nbsp;|&nbsp; 
                        🎯 Goal: <b>{saved_profile.goal.replace('_', ' ').title()}</b>
                    </div>
                </div>
                <div style="text-align: right; font-size: 0.88rem; color: #94A3B8;">
                    <div>BMR Baseline: <b style="color: #22D3EE;">{int(saved_profile.bmr)} kcal</b></div>
                    <div style="margin-top: 4px;">TDEE baseline: <b style="color: #34D399;">{int(saved_profile.tdee)} kcal</b></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Defaults from DB if available
    def_weight = saved_profile.weight_kg if saved_profile else 75.0
    def_height = saved_profile.height_cm if saved_profile else 178.0
    def_age = saved_profile.age if saved_profile else 28
    def_gender = saved_profile.gender if saved_profile else "male"
    def_act = saved_profile.activity_level if saved_profile else "moderate"
    def_goal = saved_profile.goal if saved_profile else "fat_loss"
    def_mult = saved_profile.protein_multiplier if saved_profile else 2.0
    
    with st.expander("🧬 Configure Body Metrics & High-Protein Targets (Click to toggle settings)", expanded=not bool(saved_profile)):
        col_u1, col_u2, col_u3 = st.columns([1.2, 1.2, 1])
        
        with col_u1:
            weight = st.number_input("Body Weight (kg)", min_value=30.0, max_value=350.0, value=min(350.0, max(30.0, float(def_weight))), step=0.5)
            height = st.number_input("Height (cm)", min_value=100.0, max_value=260.0, value=min(260.0, max(100.0, float(def_height))), step=1.0)
            age = st.number_input("Age (years)", min_value=12, max_value=115, value=min(115, max(12, int(def_age))), step=1)
        
        with col_u2:
            gender_choice = st.selectbox(
                "Biological Sex (for BMR baseline)",
                options=["male", "female", "other"],
                index=["male", "female", "other"].index(def_gender) if def_gender in ["male", "female", "other"] else 0
            )
            activity_choice = st.selectbox(
                "Activity Level",
                options=["sedentary", "light", "moderate", "very_active", "extra_active"],
                index=["sedentary", "light", "moderate", "very_active", "extra_active"].index(def_act) if def_act in ["sedentary", "light", "moderate", "very_active", "extra_active"] else 2,
                format_func=lambda x: {
                    "sedentary": "Sedentary (Desk job, minimal movement) - 1.2x",
                    "light": "Light Activity (1-3 gym/walk sessions/wk) - 1.375x",
                    "moderate": "Moderate (3-5 vigorous sessions/wk) - 1.55x",
                    "very_active": "Very Active (6-7 heavy training days/wk) - 1.725x",
                    "extra_active": "Athlete / High Labor - 1.9x",
                }.get(x, x)
            )
            goal_choice = st.selectbox(
                "Primary Physique / Health Goal",
                options=["fat_loss", "muscle_gain", "maintenance"],
                index=["fat_loss", "muscle_gain", "maintenance"].index(def_goal) if def_goal in ["fat_loss", "muscle_gain", "maintenance"] else 0,
                format_func=lambda x: {
                    "fat_loss": "🔥 Fat Loss (-20% Deficit, High Protein Satiety)",
                    "muscle_gain": "💪 Muscle Gain (+10% Hypertrophy Surplus)",
                    "maintenance": "⚖️ Metabolic Maintenance & Longevity",
                }.get(x, x)
            )
            
        with col_u3:
            protein_mult = st.slider(
                "Protein Multiplier (g/kg)",
                min_value=1.2,
                max_value=3.2,
                value=min(3.2, max(1.2, float(def_mult))),
                step=0.1,
                help="High-protein standard for lean mass retention & TEF thermogenesis (1.2 - 3.2g/kg bodyweight)."
            )
            meals_count = st.number_input("Target Meals / Day", min_value=1, max_value=8, value=3, step=1)
            
            save_btn = st.button("💾 Save Profile & Update Targets", use_container_width=True, type="primary")

    # If the settings expander is closed, we still read the values from it.
    # Run Macro calculation
    profile_input = UserProfileInput(
        weight_kg=weight,
        height_cm=height,
        age=age,
        gender=Gender(gender_choice),
        activity_level=ActivityLevel(activity_choice),
        goal=FitnessGoal(goal_choice),
        protein_multiplier=protein_mult,
        meals_per_day=meals_count,
    )
    targets = calculate_macro_targets(profile_input)

    if save_btn:
        save_or_update_profile(
            session=db_session,
            weight_kg=weight,
            height_cm=height,
            age=age,
            gender=gender_choice,
            activity_level=activity_choice,
            goal=goal_choice,
            protein_multiplier=protein_mult,
            bmr=targets.bmr,
            tdee=targets.tdee,
            target_calories=targets.target_calories,
            target_protein_g=targets.protein_g,
            target_carbs_g=targets.carbs_g,
            target_fats_g=targets.fats_g,
        )
        st.toast("✅ Profile and scientific macro targets saved to SQLite database!", icon="🎯")
        st.rerun()
    
    # Premium KPI Target Cards Grid (Streamlined to 3 columns to reduce visual clutter)
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""
        <div class="kpi-card" style="min-height: 110px;">
            <div class="kpi-title">🎯 Daily Calorie Target</div>
            <div class="kpi-value">{int(targets.target_calories)} <span style="font-size:0.85rem; color:#94A3B8;">kcal</span></div>
            <div class="kpi-subtext" style="color: #22D3EE;">🍞 {targets.carbs_g}g Carbs &nbsp;|&nbsp; 🥑 {targets.fats_g}g Fats</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card" style="min-height: 110px;">
            <div class="kpi-title">🥩 Target Protein</div>
            <div class="kpi-value">{targets.protein_g}g</div>
            <div class="kpi-subtext">{targets.protein_multiplier_used} g/kg bodyweight</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        per_meal_p = round(targets.protein_g / max(1, meals_count), 1)
        mops_status = "mTOR Active ⚡" if per_meal_p >= 28.0 else "Low MPS ⚠️"
        mops_color = "#34D399" if per_meal_p >= 28.0 else "#F59E0B"
        st.markdown(f"""
        <div class="kpi-card" style="min-height: 110px;">
            <div class="kpi-title">🧬 Leucine Trigger</div>
            <div class="kpi-value">~{per_meal_p}g <span style="font-size:0.85rem; color:#94A3B8;">/meal</span></div>
            <div class="kpi-subtext" style="color: {mops_color};">{mops_status}</div>
        </div>
        """, unsafe_allow_html=True)

    # Interactive Plots
    col_chart1, col_chart2 = st.columns([1, 1.2])
    
    with col_chart1:
        # Donut Chart for Macro Distribution with Soothing Green & Cyan Colors
        donut_fig = go.Figure(data=[go.Pie(
            labels=["Protein (4 kcal/g)", "Carbohydrates (4 kcal/g)", "Healthy Fats (9 kcal/g)"],
            values=[targets.protein_g * 4, targets.carbs_g * 4, targets.fats_g * 9],
            hole=0.58,
            marker=dict(colors=["#10B981", "#06B6D4", "#14B8A6"]),
            textinfo="label+percent",
            hoverinfo="label+value+percent",
        )])
        donut_fig.update_layout(
            title="<b>Daily Calorie Breakdown by Macronutrient</b>",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F0FDFA", family="Outfit"),
            showlegend=False,
            height=320,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(donut_fig, use_container_width=True)

    with col_chart2:
        # Per-Meal Target Allocation List (Saves space and looks extremely clean)
        meal_rows_html = ""
        for m in targets.meals:
            status_pill = "<span class='metric-pill pill-green' style='font-size:0.65rem; padding: 2px 8px;'>Active mTOR</span>" if m.target_protein_g >= 28.0 else "<span class='metric-pill pill-amber' style='font-size:0.65rem; padding: 2px 8px;'>Low MPS</span>"
            meal_rows_html += f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.04);">
                <div>
                    <span style="font-weight: 600; color: #F0FDFA; font-size: 0.92rem;">{m.name}</span>
                    <div style="color: #94A3B8; font-size: 0.8rem; margin-top: 2px;">{int(m.target_calories)} kcal Target</div>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #34D399; font-weight: 700; font-size: 0.98rem;">{m.target_protein_g}g P</span>
                    {status_pill}
                </div>
            </div>
            """
            
        st.markdown(f"""
        <div class="glass-card" style="min-height: 320px; padding: 22px 24px; margin-bottom: 0;">
            <div style="font-weight: 700; font-size: 1.1rem; color: #F0FDFA; margin-bottom: 12px; letter-spacing: -0.2px;">
                🧬 Per-Meal Target Allocation
            </div>
            <div style="display: flex; flex-direction: column;">
                {meal_rows_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Today's Progress & Quick Meal Logger
    st.markdown("### 📋 Today's Progress & Meal Logging")
    today_data = get_today_progress(db_session)
    
    logged_p = today_data["total_protein_g"]
    logged_cal = today_data["total_calories"]
    rem_p = max(0.0, round(targets.protein_g - logged_p, 1))
    rem_cal = max(0.0, round(targets.target_calories - logged_cal, 1))
    
    prog_col1, prog_col2, prog_col3, prog_col4 = st.columns(4)
    with prog_col1:
        p_pct = min(100.0, (logged_p / max(1.0, targets.protein_g)) * 100)
        st.markdown(f"""
        <div class="kpi-card" style="min-height: 140px;">
            <div class="kpi-title">🥩 Consumed Protein</div>
            <div class="kpi-value">{logged_p}g <span style="font-size:0.85rem; color:#94A3B8;">/ {targets.protein_g}g</span></div>
            <div class="kpi-subtext">{rem_p}g remaining</div>
            <div class="progress-container">
                <div class="progress-bar progress-bar-protein" style="width: {p_pct}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with prog_col2:
        cal_pct = min(100.0, (logged_cal / max(1.0, targets.target_calories)) * 100)
        st.markdown(f"""
        <div class="kpi-card" style="min-height: 140px;">
            <div class="kpi-title">🔥 Consumed Calories</div>
            <div class="kpi-value">{int(logged_cal)} <span style="font-size:0.85rem; color:#94A3B8;">/ {int(targets.target_calories)} kcal</span></div>
            <div class="kpi-subtext">{int(rem_cal)} kcal remaining</div>
            <div class="progress-container">
                <div class="progress-bar progress-bar-calories" style="width: {cal_pct}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with prog_col3:
        st.markdown(f"""
        <div class="kpi-card" style="min-height: 140px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="kpi-title">📋 Meals Logged</div>
                <div class="kpi-value" style="margin-top: 6px;">{today_data['meals_count']} <span style="font-size:0.9rem; color:#94A3B8;">meals</span></div>
            </div>
            <div class="kpi-subtext" style="color: #22D3EE;">Target: {meals_count} meals</div>
        </div>
        """, unsafe_allow_html=True)
    with prog_col4:
        water_ml = today_data["water_ml"]
        rec_water = max(2000.0, targets.protein_g * 35.0)
        water_pct = min(100.0, (water_ml / rec_water) * 100)
        st.markdown(f"""
        <div class="kpi-card" style="min-height: 140px; margin-bottom: 8px;">
            <div class="kpi-title">💧 Hydration Status</div>
            <div class="kpi-value">{water_ml} <span style="font-size:0.85rem; color:#94A3B8;">ml</span></div>
            <div class="kpi-subtext" style="color: #22D3EE;">Goal: {int(rec_water)} ml</div>
            <div class="progress-container">
                <div class="progress-bar progress-bar-calories" style="width: {water_pct}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        w_btn_col1, w_btn_col2 = st.columns(2)
        with w_btn_col1:
            if st.button("+250ml", use_container_width=True, key="add_water_250"):
                update_water(db_session, 250)
                st.toast("💧 Logged 250ml Water!", icon="✅")
                st.rerun()
        with w_btn_col2:
            if st.button("+500ml", use_container_width=True, key="add_water_500"):
                update_water(db_session, 500)
                st.toast("💧 Logged 500ml Water!", icon="✅")
                st.rerun()

    # Quick Meal Logger Expandable Form
    with st.expander("➕ Log a Custom Meal or Quick Snack"):
        with st.form("quick_log_form"):
            ql_col1, ql_col2, ql_col3, ql_col4, ql_col5 = st.columns(5)
            with ql_col1:
                q_name = st.text_input("Meal Name", value="Post-Workout Whey Shake")
            with ql_col2:
                q_type = st.selectbox("Meal Type", ["breakfast", "lunch", "dinner", "snack", "post_workout"])
            with ql_col3:
                q_p = st.number_input("Protein (g)", min_value=0.0, value=35.0, step=1.0)
            with ql_col4:
                q_c = st.number_input("Carbs (g)", min_value=0.0, value=15.0, step=1.0)
            with ql_col5:
                q_f = st.number_input("Fat (g)", min_value=0.0, value=3.0, step=1.0)
            
            q_cals = round((q_p * 4.0) + (q_c * 4.0) + (q_f * 9.0), 1)
            st.caption(f"Calculated Calories: **{q_cals} kcal**")
            
            if st.form_submit_button("Record Meal", use_container_width=True, type="primary"):
                log_meal(
                    session=db_session,
                    meal_name=q_name,
                    meal_type=q_type,
                    protein_g=q_p,
                    carbs_g=q_c,
                    fat_g=q_f,
                    calories=q_cals
                )
                st.toast(f"Logged '{q_name}' (+{q_p}g Protein)!", icon="✅")
                st.rerun()

    # Logged Meals List Table
    if today_data["meals"]:
        st.markdown("##### Logged Today:")
        for idx, m in enumerate(today_data["meals"]):
            st.markdown(f"""
            <div class="glass-card" style="padding: 12px 18px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <b>{m['meal_name']}</b> <span class="metric-pill pill-blue" style="font-size:0.7rem;">{m['meal_type'].upper()}</span>
                    <div style="color: #9CA3AF; font-size: 0.85rem; margin-top: 4px;">Logged at {m['time']}</div>
                </div>
                <div style="text-align: right;">
                    <span style="color: #34D399; font-weight: 700; font-size: 1.1rem;">+{m['protein_g']}g P</span> &nbsp;|&nbsp; 
                    <span style="color: #F3F4F6;">{int(m['calories'])} kcal</span>
                    <div style="color: #9CA3AF; font-size: 0.8rem;">{m['carbs_g']}g C • {m['fat_g']}g F</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ==========================================
# TAB 2: AI HIGH-PROTEIN MEAL BUILDER
# ==========================================
with tab_meals:
    st.markdown("### 🥗 AI High-Protein Meal Generator")
    st.caption("Generates culinary high-protein recipes tailored to your remaining macros and dietary preferences using Gemini 2.5 Flash.")
    
    # Pre-fill with remaining macros
    default_p_target = float(rem_p) if rem_p >= 20.0 else round(targets.protein_g / max(1, meals_count), 1)
    default_cals_target = float(rem_cal) if rem_cal >= 200.0 else round(targets.target_calories / max(1, meals_count), 0)

    # Recipe Configuration tucked into a clean expander to declutter the view
    with st.expander("⚙️ Formulate AI Recipe Parameters (Click to customize)", expanded="current_recipe" not in st.session_state):
        col_m1, col_m2, col_m3 = st.columns([1.2, 1.2, 1])
        
        with col_m1:
            meal_type_sel = st.selectbox(
                "Meal Category",
                options=[MealType.LUNCH, MealType.DINNER, MealType.BREAKFAST, MealType.POST_WORKOUT, MealType.SNACK],
                format_func=lambda x: {
                    MealType.BREAKFAST: "🍳 High-Protein Breakfast",
                    MealType.LUNCH: "🍲 High-Protein Power Lunch",
                    MealType.DINNER: "🥩 Recovery Dinner",
                    MealType.POST_WORKOUT: "⚡ Anabolic Post-Workout Shake",
                    MealType.SNACK: "🥑 High-Protein Micro Snack",
                }.get(x, x.value)
            )
            dietary_pref_sel = st.selectbox(
                "Dietary Framework",
                options=[
                    DietaryPreference.HIGH_PROTEIN,
                    DietaryPreference.OMNIVORE,
                    DietaryPreference.VEGETARIAN,
                    DietaryPreference.VEGAN,
                    DietaryPreference.PESCATARIAN,
                    DietaryPreference.KETO,
                ],
                format_func=lambda x: {
                    DietaryPreference.HIGH_PROTEIN: "🥩 High-Protein Pure (Focus on Lean HBV Proteins)",
                    DietaryPreference.OMNIVORE: "🍗 Omnivore (Poultry, Lean Beef, Fish, Dairy)",
                    DietaryPreference.VEGETARIAN: "🧀 Vegetarian (Eggs, Greek Yogurt, Whey, Cottage Cheese)",
                    DietaryPreference.VEGAN: "🌱 100% Plant-Based (Tempeh, Tofu, Pea Isolate, Hemp)",
                    DietaryPreference.PESCATARIAN: "🐟 Pescatarian (Salmon, Tuna, White Fish, Shellfish)",
                    DietaryPreference.KETO: "🥑 High-Protein Keto (Low Carb, Healthy Fats)",
                }.get(x, x.value)
            )

        with col_m2:
            target_meal_p = st.number_input(
                "Target Protein for this Meal (g)",
                min_value=10.0,
                max_value=300.0,
                value=min(300.0, max(10.0, float(default_p_target))),
                step=1.0,
                help="Aim for 30g+ to satisfy the leucine trigger threshold for muscle protein synthesis."
            )
            target_meal_cals = st.number_input(
                "Target Calories (kcal)",
                min_value=80.0,
                max_value=4000.0,
                value=min(4000.0, max(80.0, float(default_cals_target))),
                step=25.0
            )

        with col_m3:
            max_prep_time = st.slider("Max Prep Time (mins)", min_value=5, max_value=120, value=20, step=5)
            allergies_input = st.text_input("Allergies / Exclusions", placeholder="e.g. gluten, dairy, peanuts")
            
            generate_meal_btn = st.button("✨ Generate AI Recipe", use_container_width=True, type="primary")

    # Recipe Generation Logic
    if "current_recipe" not in st.session_state:
        # Default starter recipe
        st.session_state.current_recipe = generate_high_protein_meal(
            MealPlanRequest(
                target_protein_g=default_p_target,
                target_calories=default_cals_target,
                dietary_pref=dietary_pref_sel,
                meal_type=meal_type_sel,
                max_prep_time_mins=max_prep_time,
            ),
            api_key=api_key_input
        )

    if generate_meal_btn:
        with st.spinner("👨‍🍳 Gemini Chef formulating high-protein recipe & macro balance..."):
            exclusions = [x.strip() for x in allergies_input.split(",") if x.strip()]
            req = MealPlanRequest(
                target_protein_g=target_meal_p,
                target_calories=target_meal_cals,
                dietary_pref=dietary_pref_sel,
                meal_type=meal_type_sel,
                allergies_exclusions=exclusions,
                max_prep_time_mins=max_prep_time,
            )
            st.session_state.current_recipe = generate_high_protein_meal(req, api_key=api_key_input)
            st.toast("New High-Protein Recipe Ready!", icon="🥗")

    recipe: RecipeModel = st.session_state.current_recipe

    # Display Recipe Card
    st.markdown(f"""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
            <div>
                <span class="metric-pill pill-green">⏱️ {recipe.prep_time_minutes} min prep • {recipe.cook_time_minutes} min cook</span>
                <span class="metric-pill pill-purple">🧬 Longevity Score: {recipe.longevity_score}/100</span>
                <span class="metric-pill pill-blue">🔥 {recipe.protein_to_calorie_pct}% Protein Density</span>
                <div class="recipe-header" style="margin-top: 10px;">{recipe.meal_name}</div>
                <div style="color: #9CA3AF; font-size: 1rem; max-width: 780px;">{recipe.description}</div>
            </div>
            <div style="text-align: right; margin-top: 8px;">
                <div style="font-size: 2.2rem; font-weight: 800; color: #34D399;">{recipe.protein_g}g <span style="font-size: 1rem; color: #9CA3AF;">Protein</span></div>
                <div style="color: #F3F4F6; font-size: 1.1rem; font-weight: 600;">{int(recipe.calories)} kcal</div>
                <div style="color: #9CA3AF; font-size: 0.85rem;">{recipe.carbs_g}g Carbs • {recipe.fat_g}g Fats</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    r_col1, r_col2 = st.columns([1.1, 1.2])

    with r_col1:
        with st.expander("🛒 View Ingredients & Protein Breakdown", expanded=False):
            for ing in recipe.ingredients:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <span><b>{ing.name}</b> <span style="color:#9CA3AF;">({ing.quantity})</span></span>
                    <span style="color:#34D399; font-weight:600;">+{ing.protein_contribution_g}g P</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="glass-card" style="margin-top: 18px; border-left: 3px solid #60A5FA;">
            <b style="color: #60A5FA;">💡 Pro Chef & Nutritionist Tip:</b><br/>
            <span style="color: #E5E7EB; font-size: 0.95rem;">{recipe.pro_cooking_tip}</span>
        </div>
        """, unsafe_allow_html=True)

    with r_col2:
        st.markdown("#### 🍳 Step-by-Step Instructions")
        for idx, step in enumerate(recipe.instructions, start=1):
            st.markdown(f"""
            <div style="display: flex; gap: 12px; margin-bottom: 12px;">
                <div style="background: rgba(16, 185, 129, 0.2); color: #34D399; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0;">
                    {idx}
                </div>
                <div style="color: #E5E7EB; font-size: 0.95rem; line-height: 1.5;">
                    {step}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # One-Click Log Button
        if st.button("📥 Log This Meal to Daily Tracker", use_container_width=True, type="primary"):
            log_meal(
                session=db_session,
                meal_name=recipe.meal_name,
                meal_type=recipe.meal_type.value,
                protein_g=recipe.protein_g,
                carbs_g=recipe.carbs_g,
                fat_g=recipe.fat_g,
                calories=recipe.calories,
                ingredients_list=[i.model_dump() for i in recipe.ingredients]
            )
            st.toast(f"Added '{recipe.meal_name}' (+{recipe.protein_g}g Protein) to your daily log!", icon="✅")

    # Affiliate & Supplement Integration
    if recipe.affiliate_supplements:
        st.markdown("---")
        st.markdown("#### 💊 Recommended Ergogenic Supplements for this Meal")
        supp_cols = st.columns(len(recipe.affiliate_supplements))
        for idx, supp in enumerate(recipe.affiliate_supplements):
            with supp_cols[idx]:
                st.markdown(f"""
                <div class="affiliate-badge">
                    <span class="metric-pill pill-blue" style="font-size:0.65rem;">{supp.category}</span>
                    <div style="font-weight: 700; color: #F9FAFB; margin-top: 6px; font-size: 0.95rem;">{supp.name}</div>
                    <div style="font-size: 0.8rem; color: #9CA3AF; margin: 6px 0;">{supp.why_recommended}</div>
                    <div style="font-size: 0.75rem; color: #34D399; font-weight:600;">Dose: {supp.suggested_dose}</div>
                    <div style="margin-top: 10px;">
                        <a href="{supp.affiliate_url}" target="_blank" style="display: block; text-align: center; background: rgba(59, 130, 246, 0.25); color: #93C5FD; text-decoration: none; padding: 6px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(96, 165, 250, 0.4);">
                            🛒 View Supplement (Affiliate)
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ==========================================
# TAB 3: MINDSET & BOOK INSIGHTS RAG
# ==========================================
with tab_rag:
    st.markdown("### 📖 Mindset & Book Insights RAG Agent")
    st.caption("Semantic vector search indexing core frameworks from Atomic Habits, Outlive, Can't Hurt Me, The Salt Fix, Mindset, and Why We Sleep.")

    col_rag_search, col_rag_cat, col_rag_book = st.columns([1.5, 1, 1])
    
    with col_rag_search:
        rag_query = st.text_input("🔍 Search Literature (e.g., 'protein mTOR', 'friction habits', 'salt hydration', '40% rule')", value="")
    
    with col_rag_cat:
        all_cats = ["All"] + rag_engine.get_all_categories()
        cat_filter = st.selectbox("Filter Category", all_cats)
    
    with col_rag_book:
        all_books = ["All"] + rag_engine.get_all_books()
        book_filter = st.selectbox("Filter Book", all_books)

    # Perform Vector Search (Reduced top_k from 4 to 2 for cleaner view)
    search_results = rag_engine.search(
        query=rag_query,
        top_k=2,
        category=cat_filter if cat_filter != "All" else None,
        book_title=book_filter if book_filter != "All" else None,
    )

    st.markdown("#### 📚 Curated Book Frameworks")
    r_cols = st.columns(2)
    for idx, insight in enumerate(search_results):
        col_target = r_cols[idx % 2]
        with col_target:
            st.markdown(f"""
            <div class="glass-card" style="min-height: 250px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="metric-pill pill-purple">{insight.book_title}</span>
                    <span style="color: #9CA3AF; font-size: 0.8rem; font-weight: 500;">{insight.author}</span>
                </div>
                <div style="font-weight: 700; font-size: 1.05rem; color: #F0FDFA; margin: 10px 0 6px 0;">{insight.concept_title}</div>
                <div style="color: #D1D5DB; font-size: 0.88rem; margin-bottom: 10px; line-height: 1.45;">{insight.takeaway}</div>
                <div style="background: rgba(16, 185, 129, 0.1); border-left: 2px solid #34D399; padding: 8px 12px; border-radius: 6px; font-size: 0.85rem; color: #E5E7EB; margin-bottom: 10px; line-height: 1.4;">
                    <b>Actionable Protocol:</b> {insight.actionable_protocol}
                </div>
                <div class="quote-box" style="font-size: 0.85rem; margin-top: 8px; margin-bottom: 0;">
                    "{insight.quote}"
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Favorite button styled neatly
            if st.button(f"⭐ Bookmark Framework", key=f"fav_{insight.id}", use_container_width=True):
                save_favorite_insight(
                    session=db_session,
                    insight_id=insight.id,
                    book_title=insight.book_title,
                    author=insight.author,
                    concept_title=insight.concept_title,
                    quote=insight.quote,
                    actionable_protocol=insight.actionable_protocol
                )
                st.toast(f"Saved '{insight.concept_title}' to favorites!", icon="⭐")

    st.markdown("---")

    # AI Micro-Reflection & Coaching Generator
    # AI Mindset Coach wrapped in an expander to declutter the Agent page
    with st.expander("🧠 Overcome Mental Friction & Cravings (AI Mindset Coach)", expanded=False):
        preset_prompts = [
            "I feel like skipping my high-protein meal prep and ordering junk food.",
            "Struggling with fatigue and low motivation before a heavy training session.",
            "Feeling discouraged after a dietary slip-up yesterday.",
            "Hitting my protein goal when traveling and super busy.",
            "Custom write-in..."
        ]
        
        prompt_choice = st.selectbox("Select Current Friction / State", preset_prompts)
        if prompt_choice == "Custom write-in...":
            user_reflection_prompt = st.text_area("Describe your friction or challenge:", placeholder="e.g., I crave sweets late at night and struggle to get to bed before midnight.")
        else:
            user_reflection_prompt = prompt_choice
            
        coach_submit = st.button("⚡ Synthesize Book-Backed Action Protocol", type="primary", use_container_width=True)

    if (prompt_choice != "Custom write-in..." and 'coach_submit' in locals() and coach_submit) or (prompt_choice == "Custom write-in..." and 'coach_submit' in locals() and coach_submit and user_reflection_prompt.strip()):
        with st.spinner("Synthesizing frameworks from Atomic Habits, Outlive & Can't Hurt Me..."):
            reflection: ReflectionResponse = rag_engine.generate_micro_reflection(
                user_prompt=user_reflection_prompt,
                api_key=api_key_input
            )
            
            st.markdown(f"""
            <div class="glass-card" style="border: 1px solid rgba(52, 211, 153, 0.4); margin-top: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="metric-pill pill-green">🧠 Cognitive Reframing</span>
                    <span style="color: #9CA3AF; font-size: 0.8rem;">{reflection.source_citation}</span>
                </div>
                <div style="font-size: 1.1rem; color: #F9FAFB; margin: 12px 0 16px 0; font-weight: 500;">
                    {reflection.reflection_summary}
                </div>
                <div style="font-weight: 700; color: #34D399; margin-bottom: 8px;">🚀 3-Step Immediate Action Protocol:</div>
            """, unsafe_allow_html=True)
            
            for step in reflection.three_step_action_plan:
                st.markdown(f"""
                <div style="display: flex; gap: 10px; margin-bottom: 8px;">
                    <div style="color: #34D399;">➔</div>
                    <div style="color: #E5E7EB; font-size: 0.95rem;">{step}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="quote-box" style="margin-top: 16px; border-left-color: #60A5FA;">
                    <b style="color: #60A5FA;">Daily Mantra:</b> "{reflection.motivational_mantra}"
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Saved Favorites Display
    saved_favs = get_favorite_insights(db_session)
    if saved_favs:
        with st.expander(f"⭐ Saved Bookmarks ({len(saved_favs)})"):
            for f in saved_favs:
                st.markdown(f"""
                - **{f.concept_title}** (*{f.book_title}* by {f.author}): "{f.quote}"
                """)


# ==========================================
# TAB 4: PRO TIER & MONETIZATION PREVIEW
# ==========================================
with tab_pro:
    st.markdown("### 💎 Unlock Full Potential with PULSE Pro & Elite")
    st.caption("Scale your physical transformation with continuous biomarker telemetry, AI voice coaching, and automated grocery fulfillment.")
    
    # Billing Toggle
    bill_col1, bill_col2 = st.columns([1.5, 3.5])
    with bill_col1:
        billing_cycle = st.radio(
            "Select Billing Interval",
            options=["Monthly Billing", "Annual Billing (25% OFF)"],
            horizontal=True
        )
    
    is_annual = "Annual" in billing_cycle
    pro_main_price = "$11.25" if is_annual else "$14.99"
    pro_subtext = "per month, billed annually ($135/yr)" if is_annual else "per month, billed monthly"
    
    elite_main_price = "$29.99" if is_annual else "$39.99"
    elite_subtext = "per month, billed annually ($359/yr)" if is_annual else "per month, billed monthly"

    col_t1, col_t2, col_t3 = st.columns(3)

    # 1. Free Starter Tier
    with col_t1:
        st.markdown("""
        <div class="glass-card" style="min-height: 380px; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center; min-height: 28px;">
                <span class="metric-pill pill-blue">STARTER</span>
                <span style="color: #9CA3AF; font-size: 0.8rem;">Forever Free</span>
            </div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #F9FAFB; margin: 10px 0 2px 0;">$0</div>
            <div style="color: #9CA3AF; font-size: 0.85rem; min-height: 20px; margin-bottom: 16px;">Free lifetime access</div>
            <div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px; font-size: 0.9rem; line-height: 1.8;">
                <div>✅ Scientific Mifflin-St Jeor TDEE</div>
                <div>✅ 1.6–2.2g/kg Protein Targeter</div>
                <div>✅ 5 AI Meal Generations / Day</div>
                <div>✅ Basic Mindset Book Quotes</div>
                <div style="color: #6B7280;">❌ AI Voice Bio-Coach</div>
                <div style="color: #6B7280;">❌ Auto-Grocery Delivery Export</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Current Active Plan", key="btn_free_plan", use_container_width=True, disabled=True)

    # 2. PULSE Pro Tier (Central Column)
    with col_t2:
        discount_badge = "<span class='metric-pill pill-amber'>25% OFF</span>" if is_annual else "<span style='color:#9CA3AF; font-size:0.8rem;'>Flexible Monthly</span>"
        st.markdown(f"""
        <div class="glass-card" style="min-height: 380px; border: 2px solid #10B981; margin-bottom: 8px; background: linear-gradient(180deg, rgba(16, 185, 129, 0.12) 0%, rgba(17, 24, 39, 0.85) 100%);">
            <div style="display: flex; justify-content: space-between; align-items: center; min-height: 28px;">
                <span class="metric-pill pill-green">MOST POPULAR</span>
                {discount_badge}
            </div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #34D399; margin: 10px 0 2px 0;">{pro_main_price} <span style="font-size: 1rem; color: #9CA3AF; font-weight: 500;">/ mo</span></div>
            <div style="color: #34D399; font-size: 0.85rem; min-height: 20px; margin-bottom: 16px;">{pro_subtext}</div>
            <div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px; font-size: 0.9rem; line-height: 1.8;">
                <div>✅ <b>Unlimited</b> Gemini 2.5 Flash Chef</div>
                <div>✅ <b>Full Book RAG</b> Semantic Retrieval</div>
                <div>✅ 🛒 <b>1-Click Instacart / Amazon Fresh</b></div>
                <div>✅ 🧬 <b>Biomarker & Bloodwork Sync</b></div>
                <div>✅ Custom Supplement Stacking Engine</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Upgrade to PULSE Pro", key="btn_pro_upgrade", use_container_width=True, type="primary"):
            st.balloons()
            st.success("🎉 Redirecting to Stripe Secure Checkout... (Simulation)")

    # 3. Longevity Elite Tier
    with col_t3:
        elite_badge = "<span class='metric-pill pill-amber'>25% OFF</span>" if is_annual else "<span style='color:#9CA3AF; font-size:0.8rem;'>All-Inclusive</span>"
        st.markdown(f"""
        <div class="glass-card" style="min-height: 380px; border: 1px solid #8B5CF6; margin-bottom: 8px; background: linear-gradient(180deg, rgba(139, 92, 246, 0.12) 0%, rgba(17, 24, 39, 0.85) 100%);">
            <div style="display: flex; justify-content: space-between; align-items: center; min-height: 28px;">
                <span class="metric-pill pill-purple">LONGEVITY ELITE</span>
                {elite_badge}
            </div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #C084FC; margin: 10px 0 2px 0;">{elite_main_price} <span style="font-size: 1rem; color: #9CA3AF; font-weight: 500;">/ mo</span></div>
            <div style="color: #C084FC; font-size: 0.85rem; min-height: 20px; margin-bottom: 16px;">{elite_subtext}</div>
            <div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 14px; font-size: 0.9rem; line-height: 1.8;">
                <div>✅ Everything in PULSE Pro</div>
                <div>✅ 🎙️ <b>24/7 AI Voice Bio-Coach</b></div>
                <div>✅ 🩺 <b>Continuous Glucose (CGM) Sync</b></div>
                <div>✅ 👨‍⚕️ <b>Monthly 1-on-1 Nutritionist Review</b></div>
                <div>✅ Priority Concierge VIP Support</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👑 Join Longevity Elite", key="btn_elite_upgrade", use_container_width=True):
            st.toast("⚡ Elite Concierge Onboarding Activated!", icon="👑")

    st.markdown("---")
    
    # Promo Code Tester
    with st.expander("🏷️ Have a Partner / Creator Promo Code?"):
        promo_col1, promo_col2 = st.columns([3, 1])
        with promo_col1:
            promo = st.text_input("Enter Promo Code", placeholder="e.g. ATTIA20, GOGGINS, ATOMIC")
        with promo_col2:
            st.write("")
            st.write("")
            if st.button("Apply Code"):
                if promo.upper() in ["ATTIA20", "GOGGINS", "ATOMIC", "PULSE"]:
                    st.success(f"🎉 Code '{promo.upper()}' applied! Additional 20% discount activated.")
                else:
                    st.error("Invalid or expired promo code.")
