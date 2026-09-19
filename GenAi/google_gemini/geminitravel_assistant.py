import os
import streamlit as st
from google import genai
from google.genai.errors import APIError
from dotenv import load_dotenv

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Initialize GenAI Client
@st.cache_resource
def get_genai_client():
    # Automatically picks up GEMINI_API_KEY from environment
    return genai.Client()

client = get_genai_client()

# 2. Custom CSS Styling
st.markdown("""
    <style>
    /* Main container padding */
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    
    /* Header styling */
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #0072FF, #00C6FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    /* Subtitle styling */
    .sub-header {
        color: #555555;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Card containers */
    .stCard {
        background-color: #F8F9FA;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #E0E0E0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. App Header
st.markdown('<div class="main-header">✈️ AI Travel Companion</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Craft personalized, day-by-day travel itineraries in seconds.</div>', unsafe_allow_html=True)

# 4. Sidebar Inputs
with st.sidebar:
    st.header("⚙️ Trip Preferences")
    
    location = st.text_input(
        "Destination", 
        placeholder="e.g., Tokyo, Japan",
        help="Enter the city, country, or region you plan to visit."
    )
    
    days_number = st.number_input(
        "Duration (Days)", 
        min_value=1, 
        max_value=30, 
        value=5
    )
    
    budget = st.selectbox(
        "Budget Tier", 
        ("Budget-Friendly", "Moderate", "Luxury")
    )
    
    trip_plan = st.radio(
        "Traveling With", 
        ["Solo", "Partner", "Family", "Friends"]
    )
    
    st.divider()
    generate_btn = st.button("✨ Generate Itinerary", type="primary", use_container_width=True)

# 5. Main Content Section
if generate_btn:
    if not location.strip():
        st.warning("⚠️ Please enter a destination to start planning your trip.")
    else:
        # Construct detailed prompt
        prompt = f"""
        You are an expert travel planner. Create a highly structured, engaging, and practical travel itinerary based on the following details:
        
        - **Destination:** {location}
        - **Duration:** {days_number} days
        - **Budget Level:** {budget}
        - **Travel Style / Group:** {trip_plan}
        
        Please format your response in clear Markdown with the following sections:
        1. **Trip Overview & Highlights** (2-3 bullet points)
        2. **Day-by-Day Itinerary** (Bold day headers, organized into Morning, Afternoon, Evening activities)
        3. **Budget & Local Tips** (Currency, transportation, dining advice tailored to a {budget} budget)
        """

        try:
            with st.spinner("🔍 Curating recommendations and generating itinerary..."):
                # Call Gemini API using standard model syntax
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )
                
            # Success Notice
            st.success(f"🎉 Awesome! Your **{days_number}-day {budget.lower()} guide for {location}** is ready.")
            
            # Key Summary Cards
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Destination", location)
            col2.metric("Duration", f"{days_number} Days")
            col3.metric("Budget", budget)
            col4.metric("Group", trip_plan)
            
            st.divider()
            
            # Interactive Tabs
            tab1, tab2 = st.tabs(["🗺️ Complete Itinerary", "💡 Travel Tips & Export"])
            
            with tab1:
                st.markdown(response.text)
                
            with tab2:
                st.info("💡 Pro Tip: Take offline screenshots or download the itinerary as a text file for your trip!")
                st.download_button(
                    label="📥 Download Itinerary (.txt)",
                    data=response.text,
                    file_name=f"{location.replace(' ', '_').lower()}_itinerary.txt",
                    mime="text/plain"
                )

        except APIError as e:
            st.error(f"❌ Google GenAI API Error: {e.message}")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")

else:
    # Landing page state before generation
    st.info("👈 Fill in your travel details in the sidebar and click **Generate Itinerary** to get started.")
    
    # Visual placeholder columns
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🎯 Smart Recommendations")
        st.caption("Tailored activities suited for solo travelers, families, couples, or groups.")
    with c2:
        st.markdown("### 💰 Budget Aligned")
        st.caption("Customized dining, lodging, and activity picks matching your budget style.")
    with c3:
        st.markdown("### ⚡ Instant Planning")
        st.caption("Detailed morning, afternoon, and evening routines ready in seconds.")