from google import genai
# from dotenv import load_dotenv

# load_dotenv()
client = genai.Client(api_key="AQ.Ab8RN6IdkMPNcT5SizUeHZ74hlDRgJB9CY2AwXoswaT9DgaHlw")

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Explain how AI works in a few words"
)
print(interaction.output_text)