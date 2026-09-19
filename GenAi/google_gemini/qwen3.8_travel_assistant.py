import os
import streamlit as st
from google import genai
from dotenv import load_dotenv


# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()


# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Travel Assistant | Premium Trip Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ----------------------------
# Premium custom CSS
# ----------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap');

:root {
  --bg-gradient: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
  --card: #ffffff;
  --text: #0f172a;
  --muted: #64748b;
  --accent: #2563eb;
  --accent-dark: #1d4ed8;
  --border: #e5e7eb;
  --success-bg: rgba(16, 185, 129, 0.08);
  --success-border: rgba(16, 185, 129, 0.25);
  --shadow: 0 20px 45px rgba(15, 23, 42, 0.08);
}

* {
  box-sizing: border-box;
}

html, body, [class*="css"] {
  font-family: "Inter", sans-serif;
  color: var(--text);
}

.stApp {
  background: var(--bg-gradient);
}

#MainMenu {
  visibility: hidden;
}

footer {
  visibility: hidden;
}

header[data-testid="stHeader"] {
  background: transparent;
}

div[data-testid="stMain"] {
  padding-top: 2.5rem;
}

h1 {
  font-family: "Manrope", sans-serif !important;
  font-size: 2.75rem !important;
  font-weight: 800 !important;
  letter-spacing: -0.045em !important;
  line-height: 1.1 !important;
  margin-bottom: 0.25rem !important;
}

div[data-testid="stMain"] [data-testid="stCaptionContainer"] p {
  color: var(--muted) !important;
  font-size: 1.05rem !important;
  font-weight: 500;
  margin-bottom: 1.75rem !important;
  max-width: 760px;
}

h2 {
  font-size: 1.25rem !important;
  font-weight: 700 !important;
  margin-top: 0.25rem !important;
  margin-bottom: 0.5rem !important;
}

h3 {
  font-size: 1.05rem !important;
  font-weight: 700 !important;
}

.stTextInput input,
.stNumberInput input,
.stSelectbox select,
.stTextArea textarea {
  border-radius: 12px !important;
  border: 1px solid var(--border) !important;
  padding: 0.55rem 0.75rem !important;
  font-size: 1rem !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stSelectbox select:focus,
.stTextArea textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
  outline: none !important;
}

.stFormSubmitButton > button,
.stButton > button {
  width: 100% !important;
  background: linear-gradient(135deg, var(--accent), var(--accent-dark)) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 14px !important;
  padding: 0.9rem 1.25rem !important;
  font-size: 1.05rem !important;
  font-weight: 700 !important;
  box-shadow: 0 14px 30px rgba(37, 99, 235, 0.24) !important;
  transition: transform 0.18s ease, box-shadow 0.18s ease !important;
}

.stFormSubmitButton > button:hover,
.stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 36px rgba(37, 99, 235, 0.32) !important;
  color: #fff !important;
}

.stFormSubmitButton > button:active,
.stButton > button:active {
  transform: translateY(0);
}

[data-testid="stVerticalBlockBorder"] {
  border-radius: 20px !important;
  border: 1px solid var(--border) !important;
  box-shadow: var(--shadow) !important;
}

.stRadio label {
  font-weight: 600;
}

.stRadio [role="radio"] {
  border-radius: 12px;
}

div[data-testid="stMetric"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 18px !important;
  padding: 0.9rem 1rem !important;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06) !important;
}

div[data-testid="stMetricLabel"] p {
  color: var(--muted) !important;
  font-size: 0.85rem !important;
  font-weight: 600;
}

div[data-testid="stMetricValue"] p {
  font-size: 1.15rem !important;
  font-weight: 800 !important;
}

div[data-testid="stAlert"] {
  border-radius: 16px !important;
}

div[data-testid="stAlert"][data-basement="success"] {
  background: var(--success-bg) !important;
  border: 1px solid var(--success-border) !important;
}

ul li {
  margin-bottom: 0.32rem;
  line-height: 1.45;
}

section[data-testid="stSidebar"] {
  background: rgba(255, 255, 255, 0.72) !important;
  backdrop-filter: blur(14px);
}

section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
  color: var(--muted) !important;
  font-size: 0.92rem !important;
}

@media (max-width: 768px) {
  h1 {
    font-size: 2.1rem !important;
  }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ----------------------------
# Session state
# ----------------------------
if "plan" not in st.session_state:
    st.session_state.plan = ""

if "plan_details" not in st.session_state:
    st.session_state.plan_details = {}


# ----------------------------
# Cached Gemini client
# ----------------------------
@st.cache_resource(show_spinner=False)
def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return genai.Client(api_key=api_key)

    return genai.Client()


# ----------------------------
# Helpers
# ----------------------------
def api_key_exists() -> bool:
    return bool(os.getenv("GEMINI_API_KEY"))


def extract_response_text(response) -> str:
    """
    Try to extract text from different Gemini response shapes.
    """
    text = getattr(response, "text", None)
    if text:
        return str(text).strip()

    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", None) or []

        for part in parts:
            part_text = getattr(part, "text", None)
            if part_text:
                return str(part_text).strip()

    return str(response).strip()


def generate_plan(prompt: str, model: str) -> str:
    """
    Generate a travel plan using Gemini.

    This supports:
    1. client.models.generate_content(...)
    2. client.interactions.create(...)
    """
    client = get_client()

    if hasattr(client, "models"):
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return extract_response_text(response)

    interaction = client.interactions.create(
        model=model,
        input=prompt
    )

    return str(getattr(interaction, "output_text", "") or "").strip()


# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.title("⚙️ Settings")
    st.caption("Advanced options")

    model = st.selectbox(
        "Gemini model",
        [
            "gemini-3.5-flash-lite",
            "gemini-2.5-flash-lite",
            "gemini-2.5-flash",
            "gemini-2.0-flash",
        ],
        index=0,
        help="Choose a model your API key supports.",
    )

    st.divider()

    if api_key_exists():
        st.success("GEMINI_API_KEY detected", icon="✅")
    else:
        st.info("No GEMINI_API_KEY detected. Set it in .env or use configured credentials.")

    st.caption("Streamlit · Gemini · Python")

    st.divider()

    if st.button("🧹 Clear current plan"):
        st.session_state.plan = ""
        st.session_state.plan_details = {}
        st.rerun()


# ----------------------------
# Hero section
# ----------------------------
st.title("✈️ Travel Assistant")
st.caption(
    "Create a polished, personalized travel plan in seconds. "
    "Tell us your destination, duration, budget, and travel style."
)


# ----------------------------
# Input form
# ----------------------------
with st.container(border=True):
    with st.form("trip_form", clear_on_submit=False):
        st.subheader("Trip Details")

        col1, col2 = st.columns([3, 2])

        location = col1.text_input(
            "Where are you planning to go?",
            placeholder="e.g. Bali, Japan, Paris, Marrakech",
        )

        days_number = col2.number_input(
            "Number of days",
            min_value=1,
            max_value=30,
            value=3,
        )

        col3, col4 = st.columns(2)

        budget = col3.selectbox(
            "Budget",
            ["Luxury", "Moderate", "Budgeted"],
            index=1,
        )

        trip_plan = col4.radio(
            "Traveling with",
            ["Family", "Friends", "Solo", "Partner"],
            horizontal=True,
        )

        additional = st.text_area(
            "Additional preferences (optional)",
            placeholder="e.g. prefer beach, food, slow pace, vegetarian, no long flights",
            height=95,
        )

        submitted = st.form_submit_button(
            "✨ Generate Premium Trip Plan",
            use_container_width=True,
        )


# ----------------------------
# Handle form submission
# ----------------------------
if submitted:
    destination = (location or "").strip()

    try:
        days = int(days_number)
    except Exception:
        days = 3

    if not destination:
        st.warning("Please enter a destination.")
    else:
        prefs = (additional or "").strip() or "None"

        prompt = f"""
You are a premium travel planner. Create a concise, professional, and practical itinerary.

Destination: {destination}
Duration: {days} days
Traveler type: {trip_plan}
Budget level: {budget}
Additional preferences: {prefs}

Output format:
1. Trip Overview: 1-2 sentences.
2. Day-by-Day Itinerary in bullet points.
   - Each day should include Morning, Afternoon, and Evening.
   - Mention transport, food, and one practical tip.
3. Budget Notes: estimated daily range and cost-saving tips.
4. Final Recommendations: 3-5 must-do experiences.

Keep it polished, specific, and easy to read.
"""

        try:
            with st.spinner("Hang tight... crafting your premium itinerary."):
                plan = generate_plan(prompt, model)

            if not plan:
                st.warning("The model returned an empty response. Please try again.")
            else:
                st.session_state.plan = plan
                st.session_state.plan_details = {
                    "destination": destination,
                    "days": days,
                    "budget": budget,
                    "travelers": trip_plan,
                }

                st.success(
                    f"🎉 Awesome! Your **{days}-day premium guide for {destination}** is ready below."
                )

        except Exception as exc:
            st.error(f"Something went wrong while generating the plan: {exc}")


# ----------------------------
# Output section
# ----------------------------
if st.session_state.plan:
    details = st.session_state.plan_details

    st.divider()
    st.subheader("Your Itinerary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Destination", details.get("destination", "—"))
    c2.metric("Days", str(details.get("days", "—")))
    c3.metric("Budget", details.get("budget", "—"))
    c4.metric("Travelers", details.get("travelers", "—"))

    with st.container(border=True):
        st.markdown(st.session_state.plan)

    st.caption("Generated with Gemini. You can regenerate a new plan anytime.")