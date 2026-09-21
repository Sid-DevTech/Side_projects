import streamlit as st
from google import genai
from dotenv import load_dotenv
import time
import urllib.parse

load_dotenv()

client = genai.Client()

def ai_output():
    for word in interaction.output_text.split(" "):
        yield word + " "
        time.sleep(0.02)
    
def render_badge(text, color="#00C6FF", bg_color="rgba(0, 198, 255, 0.1)"):
    st.markdown(f"""
        <span style="
            background-color: {bg_color};
            color: {color};
            border: 1px solid {color};
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 10px;
        ">
            ● {text}
        </span>
    """, unsafe_allow_html=True)

def update_status(placeholder, emoji, text):
    """Renders shining text and a floating emoji inside an st.empty slot."""
    placeholder.markdown(f"""
        <div class="aero-status-box">
            <span class="floating-icon">{emoji}</span>
            <span class="shine-text">{text}</span>
        </div>
    """, unsafe_allow_html=True)


with st.sidebar:
    st.title("Aero",text_alignment="center",width='stretch',icon=":material/flight:")
    st.divider()
    # render_badge("READY TO EXPLORE", color="#00E676", bg_color="rgba(0, 230, 118, 0.1)")
    st.pills("Status", ["🟢 Ready to Explore", "⚡ Gemini Powered"], selection_mode="multi")  
    location= st.text_input("Where are you planning to go? ")
    # days_number= st.number_input("Number of days to plan the trip", min_value=1, max_value=30)
    days_number=st.slider("Number of days to plan the trip",min_value=1,max_value=30,value=1)
    budget= st.selectbox("What's your budget?", ("Luxury","Moderate", "Budgeted"))
    trip_plan= st.radio("Who are you planning to go with?", ["Family","Friends","Solo","Partner"])
    plan_btn = st.button("Plan trip",type="primary",use_container_width=True)
    date_time=st.date_input("Schedule your trip")


st.title("Aero Destination Dashboard",icon=":material/flight:")
st.caption("Your Personal Trip Assistant")
st.markdown("""
    <style>
    /* Prevent metric labels and text from cutting off with '...' */
    div[data-testid="stMetricValue"] > div, 
    div[data-testid="stMetricLabel"] > div {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
    }
    </style>
""", unsafe_allow_html=True)

col1 ,col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Destination 🗺️", value=location if location else "Not Set",border=True)
with col2:
    st.metric(label="Duration ⏱️",value=f"{days_number} Days",border=True)
with col3:
    st.metric(label="Trip type",value=f"{trip_plan}",border=True)
with col4:
    st.metric(label="Budget 💰",value=f"{budget}",border=True,width="stretch")
st.divider()    




prompt = f"""
You are a travel planner. Plan a {days_number}-day trip to {location} for {trip_plan} scheduled time for trip {date_time}.
DATE & SEASONAL INTELLIGENCE:
- The trip starts on {date_time}.
- Tailor activities strictly to the typical weather, climate, daylight hours, and local seasonal events in {location} during {date_time}.
- Provide specific date-conscious advice for each day (e.g., weekend crowd warnings on Saturday/Sunday, seasonal night markets, or winter/summer opening hours).
Provide two sections in your response:

SECTION 1 - ITINERARY:
Detailed day-by-day itinerary in bullet points.

SECTION 2 - LOCATIONS:
A single line containing ONLY the key place names separated by commas (e.g., Tokyo Tower, Senso-ji Temple, Shibuya Crossing).

SECTION 3 - COSTS:
Provide an itemized cost estimate for this entire {days_number}-day trip in {location} for a {budget} budget.
Return ONLY four lines in this exact format:
Accommodation: $X
Food & Dining: $Y
Activities & Tickets: $Z
Local Transit: $W
"""

if plan_btn:
    st.markdown("""
    <style>
    @keyframes textShine {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    @keyframes floatIcon {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-4px); }
    }

    .aero-status-box {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        margin-bottom: 8px !important;
    }

    .aero-status-box .shine-text {
        font-family: Source Sans Pro, -apple-system, BlinkMacSystemFont, Roboto, sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        background: linear-gradient(
            90deg, 
            #00C6FF 0%, 
            #FFFFFF 30%, 
            #0072FF 60%, 
            #00C6FF 100%
        ) !important;
        background-size: 200% auto !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        animation: textShine 3s linear infinite !important;
    }

    .aero-status-box .floating-icon {
        font-size: 1.1rem !important;
        display: inline-block !important;
        animation: floatIcon 2.5s ease-in-out infinite !important;
    }
    </style>
""", unsafe_allow_html=True)
    if not location:
        st.warning("Please enter a destination in the sidebar.")
    else:
        status_box = st.empty()
        progress_bar = st.progress(0)


        update_status(status_box, "🔍", f"Analyzing preferences for {location}...")
        for p in range(0, 36):
            time.sleep(0.3)
            progress_bar.progress(p)


        update_status(status_box, "✈️", f"Mapping top spots across {days_number} days...")
        for p in range(36, 71):
            time.sleep(0.3)
            progress_bar.progress(p)


        update_status(status_box, "🗓️", "Building your custom itinerary...")
        for p in range(71, 96):
            time.sleep(0.3)
            progress_bar.progress(p)

    st.subheader("Route & Daily Itinerary",icon="🗺️")
    interaction= client.interactions.create( model = "gemini-3.5-flash-lite",
    input=prompt)
    progress_bar.progress(100)
    time.sleep(0.2)
    progress_bar.empty()
    status_box.empty()
    with st.container():
        st.caption("Interactive Map View")
    if "SECTION 2 - LOCATIONS:" in interaction.output_text:
        raw_locations = interaction.output_text.split("SECTION 2 - LOCATIONS:")[1].strip()
        query = urllib.parse.quote(f"{raw_locations} in {location}")
        map_url = f"https://maps.google.com/maps?q={query}&t=&z=12&ie=UTF8&iwloc=&output=embed"
        st.iframe(map_url, height=400)
    st.success(f"🎉 Awesome! Your **{days_number}-day custom guide for {location}** is ready below.")
    st.subheader("Trip Essentials And Tools")
    with st.expander("Recommended Packing Checklist",expanded=False):
        st.checkbox("Universal Power Adapter")
        st.checkbox("Travel Assurance Documents")
        st.checkbox("Comfortable Walking Shoes")
    if "SECTION 3 - COSTS:" in interaction.output_text:
        cost_text= interaction.output_text.split("SECTION 3 - COSTS:")[1].strip()
        costs={}
        for line in cost_text.split("\n"):
            if ":" in line:
                category,val= line.split(":",1)
                costs[category.strip()] = val.strip()
        with st.expander("💵 Estimated Cost Breakdown", expanded=False):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Accommodation", costs.get("Accommodation", "N/A"))
            c2.metric("Food & Dining", costs.get("Food & Dining", "N/A"))
            c3.metric("Activities", costs.get("Activities & Tickets", "N/A"))
            c4.metric("Local Transit", costs.get("Local Transit", "N/A"))        
    with st.expander("💡 Local Safety & Etiquette", expanded=False):
        st.info("Emergency Contact: 112 | Always carry cash for local vendors.")    

    st.write_stream(ai_output)
    st.feedback("faces")