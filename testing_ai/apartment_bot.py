import os # Importing OS for environment variable handling
from dotenv import load_dotenv # Importing load_dotenv to load environment variables from a .env file
from openai import OpenAI # Importing OpenAI client for API interactions
load_dotenv() # Load environment variables from .env file
token = os.getenv("GITHUB_TOKEN") # Retrieve the GitHub token from environment variables
model_name = "openai/gpt-4.1" # Define the model name to be used for the API call
github_models_base_url = "https://models.github.ai/inference" # Define the base URL for the GitHub models API
client = OpenAI(
    api_key=token,
    base_url=github_models_base_url
)
KW = ["apartment", "flat", "room", "renovation", "furniture", "storage", "decor"]
SYSTEM = (
    "You are an expert on improving apartments. "
    "If the user asks anything outside that domain, answer: "
    "\"Sorry, I don't have knowledge on that.\" Wait for a new question."
)

# Function to make the API call using the OpenAI client
def ask_llm(question):
    try:
        response = client.chat.completions.create(
            model = model_name, # Use the defined model_name
            temperature = 0.7, # Set the temperature based on task requirements
            messages = [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content # Return the content of the first choice from the response
    except Exception as e:
        return f"API Error: {e}"

# 🧾 Function to handle input and route logic
def main():
    question = input("Ask your question: ").strip().lower()

    if any(kw in question for kw in KW): # Check if the question contains any of the keywords
        answer = ask_llm(question) # Answer gotten from the ask_llm function
        print(answer) # Print the answer to the user
    else:
        print("Sorry, I don't have knowledge on that.")

if __name__ == "__main__":
    main()