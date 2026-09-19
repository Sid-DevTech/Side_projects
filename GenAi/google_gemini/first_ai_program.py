from google import genai
from dotenv import load_dotenv
import time
load_dotenv()
client = genai.Client()
try:
    with open ("aichat_1.txt","r") as f:
        history=f.read()
except FileNotFoundError:
    print("File not found")


query= input("What's Cooking? : ")

history = history + "User :" + query
while True:
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=query,
        generation_config={"temperature":0.7,"top_k":20,"max_output_tokens":400},
        system_instruction="""You are an experienced Travel Planner however you sprinkle some historic facts about that place"""
)
    print("Hang tight... We're getting everything ready for you.")
    for i in range(3):
        print(".", end="", flush=True)
        time.sleep(1)

    print("\nSidsAi replies: \n\n", interaction.output_text)
    history= history +"Assistant :" + interaction.output_text

    query=input("\n\nOver to you... What's on your mind?")
    history = history + "User :" + query
    if (query=="exit") or (query=="") or (query=="close"):
        with open("aichat_1.txt","a") as f:
            f.write(history)
        break
