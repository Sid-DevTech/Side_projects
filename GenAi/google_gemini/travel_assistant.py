import streamlit as st
from google import genai
from dotenv import load_dotenv
import time

load_dotenv()

client = genai.Client()

st.title("Travel Assistant")
st.caption("Your Personal Assistant")

location= st.text_input("Where are you planning to go? ")
days_number= st.number_input("Number of days to plan the trip", min_value=1, max_value=30)

budget= st.selectbox("What's your budget?", ("Luxury","Moderate", "Budgeted"))
trip_plan= st.radio("Who are you planning to go with?", ["Family","Friends","Solo","Partner"])
prompt= f"""You are a travel planner, User is saying they want to go to {location} for {days_number} days with {trip_plan} Plan a trip in bullet points"""

if st.button("Plan trip"):
    interaction= client.interactions.create( model = "gemini-3.5-flash-lite",
    input=prompt)
    with st.spinner("Hang tight... We're getting everything ready for you.",show_time=True):
        time.sleep(3)

    st.success(f"🎉 Awesome! Your **{days_number}-day custom guide for {location}** is ready below.")
    st.write(interaction.output_text)