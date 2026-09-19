import streamlit as st
from google import genai
from dotenv import load_dotenv
import time

# ---------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------

st.set_page_config(
    page_title="TravelAI",
    page_icon="✈️",
    layout="centered"
)

# ---------------------------------------
# LOAD API
# ---------------------------------------

load_dotenv()

client = genai.Client()

# ---------------------------------------
# CUSTOM CSS
# ---------------------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(59, 130, 246, 0.15),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(139, 92, 246, 0.15),
                transparent 30%
            ),
            #080b14;
    }

    /* Main container */
    .block-container {
        max-width: 850px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    /* Input styling */
    div[data-baseweb="input"] {
        border-radius: 12px;
    }

    div[data-baseweb="select"] > div {
        border-radius: 12px;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        height: 52px;
        border-radius: 14px;
        border: none;

        background: linear-gradient(
            90deg,
            #2563eb,
            #7c3aed
        );

        color: white;
        font-size: 16px;
        font-weight: 700;

        transition: 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
    }

    /* Section heading */
    .section-heading {
        font-size: 20px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 15px;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------
# HERO
# ---------------------------------------

st.markdown(
    "<div style='text-align:center; font-size:50px;'>✈️</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align:center;'>TravelAI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:#94a3b8; font-size:18px;'>"
    "Your personal AI-powered travel planner."
    "</p>",
    unsafe_allow_html=True
)

st.caption("Tell us where you're going. We'll plan the rest.")

st.write("")


# ---------------------------------------
# TRIP DETAILS
# ---------------------------------------

st.markdown("### 🌍 Tell us about your trip")

location = st.text_input(
    "Destination",
    placeholder="e.g. Paris, Tokyo, Dubai..."
)

col1, col2 = st.columns(2)

with col1:

    days_number = st.number_input(
        "Trip duration",
        min_value=1,
        max_value=30,
        value=5
    )

with col2:

    budget = st.selectbox(
        "Budget",
        ["Luxury", "Moderate", "Budget"]
    )


trip_plan = st.radio(
    "Who are you travelling with?",
    ["Family", "Friends", "Solo", "Partner"],
    horizontal=True
)


st.write("")


# ---------------------------------------
# PLAN TRIP BUTTON
# ---------------------------------------

if st.button("✨ Create My Travel Plan"):

    # Check destination
    if not location.strip():

        st.warning(
            "Please enter a destination before planning your trip."
        )

    else:

        # ---------------------------------------
        # AI PROMPT
        # ---------------------------------------

        prompt = f"""
You are an expert travel planner.

Create a detailed and practical travel itinerary.

Destination: {location}
Duration: {days_number} days
Budget: {budget}
Travelling with: {trip_plan}

Requirements:

- Create a day-by-day itinerary.
- Include important attractions and experiences.
- Suggest approximate timings.
- Suggest local food or restaurant types to try.
- Include transportation suggestions.
- Keep the itinerary realistic.
- Do not pack too many activities into one day.
- Adapt the recommendations to the selected budget.
- Include estimated daily expenses where useful.
- Include useful travel tips.
- Use clear headings and bullet points.
- Make the itinerary easy to read.

End with a short "Travel Tips" section.
"""

        # ---------------------------------------
        # GENERATE RESPONSE
        # ---------------------------------------

        with st.spinner(
            "✈️ Planning your perfect trip...",
            show_time=True
        ):

            interaction = client.interactions.create(
                model="gemini-3.1-flash-lite-preview",
                input=prompt
            )

            time.sleep(2)


        # ---------------------------------------
        # RESULT
        # ---------------------------------------

        st.success(
            f"🎉 Your {days_number}-day trip to "
            f"{location} is ready!"
        )

        st.markdown("---")

        st.markdown(
            f"## 🗺️ {location} Travel Plan"
        )

        st.caption(
            f"{days_number} days • "
            f"{budget} budget • "
            f"{trip_plan} trip"
        )

        st.write(
            interaction.output_text
        )


# ---------------------------------------
# FOOTER
# ---------------------------------------

st.write("")
st.write("")

st.divider()

st.caption("✈️ TravelAI · Powered by Gemini")
st.caption("Plan smarter. Travel better.")