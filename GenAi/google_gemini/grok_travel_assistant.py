import streamlit as st
from google import genai
from dotenv import load_dotenv
import time

# ── Page config (must be first Streamlit command)
st.set_page_config(
    page_title="Aether | Travel Concierge",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()
client = genai.Client()

# ── Custom CSS for a premium look
st.markdown("""
<style>
    /* Global font & background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }
    
    /* Card-like containers */
    .premium-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Primary button */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stRadio > div {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
    }
    
    /* Success message */
    .stSuccess {
        background: rgba(16, 185, 129, 0.15) !important;
        border: 1px solid #10b981 !important;
        border-radius: 12px !important;
        color: #6ee7b7 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #8b5cf6 !important;
    }
    
    /* Divider */
    hr {
        border-color: #334155 !important;
        margin: 2rem 0 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Sidebar – Input Panel
with st.sidebar:
    st.markdown("### ✈️ Trip Details")
    st.caption("Tell us about your journey")
    
    st.markdown("---")
    
    location = st.text_input(
        "Destination",
        placeholder="e.g. Kyoto, Japan",
        help="City or region you want to visit"
    )
    
    days_number = st.number_input(
        "Duration (days)",
        min_value=1,
        max_value=30,
        value=5,
        step=1
    )
    
    budget = st.selectbox(
        "Budget Level",
        options=["Luxury", "Moderate", "Budgeted"],
        index=1
    )
    
    trip_plan = st.radio(
        "Traveling with",
        options=["Family", "Friends", "Solo", "Partner"],
        horizontal=False
    )
    
    st.markdown("---")
    
    plan_button = st.button("✨ Craft My Itinerary", use_container_width=True)
    
    st.markdown("")
    st.caption("Powered by Gemini • Curated for you")

# ── Main Content Area
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # Hero section
    st.markdown("""
    <div style="text-align: center; padding: 2.5rem 0 1.5rem 0;">
        <h1 style="font-size: 2.8rem; margin-bottom: 0.3rem; background: linear-gradient(90deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Aether
        </h1>
        <p style="font-size: 1.15rem; color: #94a3b8; font-weight: 400; margin-top: 0;">
            Your private travel concierge
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Empty state
    if not plan_button:
        st.markdown("""
        <div class="premium-card" style="text-align: center; padding: 3rem 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🌍</div>
            <h3 style="margin-bottom: 0.5rem; color: #e2e8f0;">Ready when you are</h3>
            <p style="color: #94a3b8; max-width: 420px; margin: 0 auto;">
                Fill in your destination, duration, budget and travel style on the left.  
                We’ll craft a refined, day-by-day plan just for you.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Generate plan
    if plan_button:
        if not location or not location.strip():
            st.warning("Please enter a destination to continue.")
        else:
            prompt = f"""You are an expert luxury travel planner.
            Create a refined, practical {days_number}-day itinerary for {location}.
            Travel style: {trip_plan}
            Budget level: {budget}
            
            Structure the response clearly with:
            - A short elegant introduction
            - Day-by-day plan in bullet points (morning / afternoon / evening where useful)
            - Suggested experiences, dining notes, and practical tips
            - Keep the tone sophisticated yet warm
            """
            
            with st.spinner("Curating your personal itinerary..."):
                time.sleep(1.2)  # slight delay for perceived quality
                try:
                    interaction = client.interactions.create(
                        model="gemini-3.5-flash-lite",
                        input=prompt
                    )
                    
                    st.success(f"Your **{days_number}-day guide for {location}** is ready")
                    
                    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                    st.markdown(interaction.output_text)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error("We couldn’t generate the itinerary right now. Please try again in a moment.")
                    st.caption(f"Technical details: {str(e)}")