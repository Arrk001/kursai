import os
from google import genai
from dotenv import load_dotenv
import pandas as pd
import metadata_api

# --- Configuration ---
load_dotenv()


client = genai.Client()

def clarify_title(user_input):
    prompt = f"User entered: '{user_input}'. Suggest the most likely correct movie or TV show title. Only return the corrected title, nothing else."
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()

def chat_about_watchlist(user_query, watchlist_df):
    # Always use Gemini AI to answer based on the user's question and the watchlist
    csv_data = watchlist_df.to_csv(index=False)
    prompt = f"Here is my watchlist in CSV format:\n{csv_data}\n\nUser question: {user_query}\nAnswer conversationally and as helpfully as possible based only on the data."
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip() 