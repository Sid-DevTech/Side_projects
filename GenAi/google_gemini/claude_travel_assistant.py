import html
import os
import re

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

APP_NAME = "Meridian"
MODEL_NAME = "gemini-3.5-flash-lite"

st.set_page_config(
    page_title=f"{APP_NAME} — Travel Concierge",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def inject_css() -> None:
    st.html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --ink: #16233B;
        --teal: #1F4842;
        --gold: #B8894F;
        --gold-soft: #D8B583;
        --parchment: #FAF6EE;
        --card: #FFFFFF;
        --charcoal: #26262A;
        --muted: #746C5E;
        --border: #E4DCC8;
    }

    [data-testid="stAppViewContainer"] { background: var(--parchment); }
    [data-testid="stHeader"] { background: transparent; }
    footer { visibility: hidden; }

    .main .block-container {
        max-width: 720px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    [data-testid="stAppViewContainer"] * {
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    .hero-title,
    .info-value {
        font-family: 'Fraunces', serif !important;
    }
    [data-testid="stAppViewContainer"] code,
    [data-testid="stAppViewContainer"] pre {
        font-family: ui-monospace, Consolas, monospace !important;
    }

    /* Hero */
    .st-key-hero {
        background: linear-gradient(155deg, var(--ink) 0%, var(--teal) 130%);
        border-radius: 10px;
        padding: 2.75rem 2.5rem;
        margin-bottom: 1.75rem;
    }
    .hero-mark {
        color: var(--gold-soft);
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .hero-title {
        color: var(--parchment);
        font-size: 2.35rem;
        font-weight: 500;
        line-height: 1.18;
        margin: 0 0 0.75rem 0;
    }
    .hero-subtitle {
        color: #CBD3DE;
        font-size: 1.02rem;
        line-height: 1.55;
        max-width: 32rem;
        margin: 0;
    }

    /* Trip form card */
    .st-key-trip_form {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 2rem 2rem 1.6rem;
        margin-bottom: 1.5rem;
    }

    label[data-testid="stWidgetLabel"] p {
        font-weight: 600;
        color: var(--charcoal);
        font-size: 0.86rem;
    }

    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        border-radius: 6px !important;
        border-color: var(--border) !important;
    }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 1px var(--gold) !important;
    }

    [data-testid="stRadio"] > div { gap: 0.5rem; flex-wrap: wrap; }
    [data-testid="stRadio"] label {
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.3rem 1rem;
        transition: background 0.15s ease, border-color 0.15s ease;
    }
    [data-testid="stRadio"] label:has(input:checked) {
        background: var(--ink);
        border-color: var(--ink);
    }
    [data-testid="stRadio"] label:has(input:checked) p {
        color: var(--parchment) !important;
    }

    [data-testid="stButton"] button {
        background: var(--ink);
        border: 1px solid var(--ink);
        border-radius: 7px;
        padding: 0.65rem 1.5rem;
        font-weight: 600;
        margin-top: 0.4rem;
    }
    [data-testid="stButton"] button p { color: var(--parchment) !important; }
    [data-testid="stButton"] button:hover {
        background: var(--teal);
        border-color: var(--teal);
    }

    [data-testid="stDownloadButton"] button {
        background: transparent;
        border: 1px solid var(--ink);
        border-radius: 7px;
    }
    [data-testid="stDownloadButton"] button p { color: var(--ink) !important; }
    [data-testid="stDownloadButton"] button:hover { background: var(--parchment); }

    /* Result card */
    .st-key-result_card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1.75rem 2rem 2rem;
        margin-top: 0.25rem;
    }
    .info-strip {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        border-bottom: 1px dashed var(--border);
        padding-bottom: 1.25rem;
        margin-bottom: 1.25rem;
    }
    .info-field .info-label {
        display: block;
        font-size: 0.66rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 0.2rem;
    }
    .info-field .info-value {
        font-size: 1.02rem;
        color: var(--charcoal);
        font-weight: 500;
    }
    .st-key-result_card h2 {
        color: var(--ink);
        font-size: 1.28rem;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        padding-left: 0.6rem;
        border-left: 3px solid var(--gold);
    }
    .st-key-result_card [data-testid="stMarkdownContainer"] ul li::marker {
        color: var(--gold);
    }

    @media (max-width: 640px) {
        .info-strip { grid-template-columns: repeat(2, 1fr); }
        .hero-title { font-size: 1.85rem; }
        .st-key-hero { padding: 2rem 1.5rem; }
        .st-key-trip_form { padding: 1.5rem; }
    }
    </style>
    """)


def build_prompt(destination: str, days: int, budget: str, companions: str) -> str:
    return f"""You are an expert travel concierge. Create a detailed {days}-day itinerary for a trip to {destination}.

Traveler profile:
- Budget level: {budget}
- Traveling with: {companions}

Write the itinerary in clean Markdown:
- One "## Day N — [short theme]" heading per day
- Under each day, group suggestions as **Morning**, **Afternoon**, and **Evening**, each with 2-3 concise bullet points
- Make suggestions concrete (real neighborhoods, sights, food styles) and fitting for a {budget} travel style
- Start directly with Day 1 — no introduction paragraph, no closing summary
"""


inject_css()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error(
        "No Gemini API key found. Add `GEMINI_API_KEY=your_key` to a `.env` file "
        "next to this script, then restart the app."
    )
    st.stop()

client = genai.Client()

with st.container(key="hero"):
    st.markdown(
        f"""
        <div class="hero-mark">🧭 {APP_NAME}</div>
        <h1 class="hero-title">Plan your next journey</h1>
        <p class="hero-subtitle">Tell us where you're headed, for how long, and who's
        coming along — we'll shape it into a day-by-day plan in moments.</p>
        """,
        unsafe_allow_html=True,
    )

with st.container(key="trip_form"):
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("Destination", placeholder="e.g. Kyoto, Japan")
    with col2:
        days_number = st.number_input("Duration (days)", min_value=1, max_value=30, value=5)

    col3, col4 = st.columns(2)
    with col3:
        budget = st.selectbox("Budget level", ("Luxury", "Moderate", "Budget"))
    with col4:
        companions = st.radio("Traveling with", ["Family", "Friends", "Solo", "Partner"], horizontal=True)

    generate = st.button("Plan my trip", icon="✨", width="stretch")

if generate:
    destination = location.strip()
    days = int(days_number)

    if not destination:
        st.warning("Add a destination before I can start planning.")
        st.stop()

    prompt = build_prompt(destination, days, budget, companions)

    try:
        with st.spinner("Shaping your itinerary...", show_time=True):
            interaction = client.interactions.create(model=MODEL_NAME, input=prompt)
        itinerary = interaction.output_text
    except Exception as exc:
        st.error(f"The travel desk hit a snag reaching Gemini: {exc}")
        st.stop()

    if not itinerary:
        st.warning("Gemini didn't return anything usable — please try again.")
        st.stop()

    st.success(f"Your {days}-day guide to {destination} is ready.")

    safe_destination = html.escape(destination)

    with st.container(key="result_card"):
        st.markdown(
            f"""
            <div class="info-strip">
                <div class="info-field"><span class="info-label">Destination</span><span class="info-value">{safe_destination}</span></div>
                <div class="info-field"><span class="info-label">Duration</span><span class="info-value">{days} days</span></div>
                <div class="info-field"><span class="info-label">Budget</span><span class="info-value">{budget}</span></div>
                <div class="info-field"><span class="info-label">Traveling with</span><span class="info-value">{companions}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(itinerary)

    file_slug = re.sub(r"[^a-zA-Z0-9]+", "_", destination).strip("_").lower() or "trip"
    st.download_button(
        "Save itinerary as Markdown",
        data=itinerary,
        file_name=f"{file_slug}_itinerary.md",
        mime="text/markdown",
        width="content",
    )

    st.caption("Generated by AI — double-check opening hours, prices, and entry requirements before you travel.")