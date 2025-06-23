import os
from openai import OpenAI
from dotenv import load_dotenv
from csv_reader import get_bday_people
from rich import print
from bday_filter import filter_bday_people
import json
from tools import send_email_definition, send_email

load_dotenv()
TOKEN = os.getenv("GH_API_TOKEN")
ENDPOINT = "https://models.github.ai/inference"
MODEL = "openai/gpt-4.1-mini"

client = OpenAI(
    base_url=ENDPOINT,
    api_key=TOKEN,
)

people = get_bday_people()
bday_people = filter_bday_people(people)
system_message = """You are a warm and friendly birthday greetings assistant.
Your job is to generate short, personal, and cheerful birthday greetings based on a person's name, personality traits, and interests which is provided in user message. 
Use natural and conversational Lithuanian language.
You should pass email_content as HTML markup. You can use colors, semantic tags and this image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTymGedbqksQgqz34xtXOi1A6XuVtVg58umw&s"
"""

print(people)
print(bday_people)

for person in bday_people:
    messages = [{"role": "system", "content": system_message}]
    person_data_str = json.dumps(person)
    messages.append({"role": "user", "content": person_data_str})
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=[send_email_definition],
        tool_choice="auto"
    )
    tool_call = response.choices[0].message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)

    send_email(
        recipient=arguments["recipient"],
        subject=arguments["subject"],
        email_content=arguments["email_content"]
    )
