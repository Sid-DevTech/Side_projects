import streamlit as st
from google import genai
from dotenv import load_dotenv
import time

# ---------- Setup ----------
load_dotenv()
client = genai.Client()

st.set_page_config(
    page_title="Voyara · Travel Assistant",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- Custom Premium CSS ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Background */
    .stApp {
        background: radial-gradient(1200px 600px at 20% -10%, #1f2a44 0%, #0d1117 45%, #06080d 100%);
        color: #e8ecf3;
    }

    /* Hero */
    .hero {
        text-align: center;
        padding: 2.6rem 1rem 1.2rem 1rem;
        animation: fadeUp 0.8s ease-out;
    }
    .hero-badge {
        display: inline-block;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        background: linear-gradient(135deg, rgba(120,180,255,0.15), rgba(180,120,255,0.15));
        border: 1px solid rgba(140,180,255,0.35);
        color: #a9c5ff;
        font-size: 0.78rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        line-height: 1.1;
        margin: 0;
        background: linear-gradient(120deg, #ffffff 10%, #a9c5ff 55%, #d0b3ff 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-sub {
        color: #98a2b3;
        font-size: 1rem;
        margin-top: 0.6rem;
        font-weight: 300;
    }

    /* Section label */
    .section-label {
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #7f8aa3;
        margin: 1.4rem 0 0.4rem 0;
        font-weight: 600;
    }

    /* Inputs */
    .stTextInput input, .stNumberInput input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
        color: #e8ecf3 !important;
        padding: 0.7rem 0.9rem !important;
        transition: all 0.2s ease;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #7aa2ff !important;
        box-shadow: 0 0 0 3px rgba(122,162,255,0.18) !important;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
        color: #e8ecf3 !important;
    }

    /* Radio */
    div[role="radiogroup"] label {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 0.45rem 0.9rem;
        border-radius: 10px;
        margin-right: 0.4rem;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    div[role="radiogroup"] label:hover {
        border-color: rgba(122,162,255,0.5);
        background: rgba(122,162,255,0.08);
    }

    /* Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #5b8cff 0%, #8f6bff 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.85rem 1.4rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.02em;
        box-shadow: 0 10px 30px -10px rgba(91,140,255,0.6);
        transition: all 0.25s ease;
        margin-top: 1rem;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 40px -12px rgba(143,107,255,0.75);
        color: white;
    }

    /* Result card */
    .result-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 18px;
        padding: 1.8rem 2rem;
        margin-top: 1.2rem;
        box-shadow: 0 20px 60px -30px rgba(0,0,0,0.9);
        animation: fadeUp 0.6s ease-out;
    }
    .result-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        margin-bottom: 0.2rem;
        color: #ffffff;
    }
    .result-meta {
        color: #98a2b3;
        font-size: 0.88rem;
        margin-bottom: 1.2rem;
    }
    .result-body h1, .result-body h2, .result-body h3 {
        color: #dbe4f5;
        font-family: 'Playfair Display', serif;
    }
    .result-body p, .result-body li {
        color: #cdd6e6;
        line-height: 1.7;
    }

    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.08) !important;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Hero ----------
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">✈️ Voyara · AI Travel Studio</div>
        <h1 class="hero-title">Design your next journey</h1>
        <p class="hero-sub">Tell us where you're headed — we'll craft a bespoke itinerary in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Inputs ----------
st.markdown('<div class="section-label">Destination</div>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    location = st.text_input(
        "Where are you planning to go?",
        placeholder="e.g. Kyoto, Japan",
        label_visibility="collapsed",
    )
with col2:
    days_number = st.number_input(
        "Days",
        min_value=1,
        max_value=30,
        value=5,
        label_visibility="collapsed",
        help="Number of days",
    )

st.markdown('<div class="section-label">Style & Company</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    budget = st.selectbox(
        "What's your budget?",
        ("Luxury", "Moderate", "Budgeted"),
        label_visibility="collapsed",
    )
with col4:
    trip_plan = st.radio(
        "Who are you planning to go with?",
        ["Family", "Friends", "Solo", "Partner"],
        horizontal=True,
        label_visibility="collapsed",
    )

# ---------- Prompt ----------
prompt = f"""You are an expert travel planner.
The user wants to travel to {location} for {days_number} days.
Travel companions: {trip_plan}.
Budget style: {budget}.

Craft a detailed, elegant day-by-day itinerary in Markdown bullet points.
Include:
- A short intro line about the destination
- Day-wise plan with morning / afternoon / evening activities
- Recommended local food & experiences
- A short packing/advice tip at the end.
Keep tone warm, inspiring, and premium.
"""

# ---------- Button & Output ----------
plan_clicked = st.button("✨  Generate My Itinerary")

if plan_clicked:
    if not location.strip():
        st.warning("Please enter a destination to continue.")
    else:
        with st.spinner("Curating your journey… this will just take a moment."):
            try:
                interaction = client.interactions.create(
                    model="gemini-3.5-flash-lite",
                    input=prompt,
                )
                # small cinematic pause
                time.sleep(1.2)
                result_text = interaction.output_text
            except Exception as e:
                st.error(f"Something went wrong while planning your trip: {e}")
                result_text = None

        if result_text:
            st.success(
                f"🎉 Your **{days_number}-day {budget.lower()} itinerary** for "
                f"**{location}** ({trip_plan}) is ready."
            )
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-title">{location}</div>
                    <div class="result-meta">
                        {days_number} days · {budget} · {trip_plan} trip
                    </div>
                    <div class="result-body">
                """,
                unsafe_allow_html=True,
            )
            st.markdown(result_text)
            st.markdown("</div></div>", unsafe_allow_html=True)