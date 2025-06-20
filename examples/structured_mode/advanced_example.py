import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

from rich import print

load_dotenv()
token = os.getenv("GH_API_TOKEN")
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)


class CityData(BaseModel):
    city_name: str
    total_population: int
    men_population: int
    women_population: int
    reason_why_city_is_popular: str

class CityDataObject(BaseModel):
    top_cities: list[CityData]

response = client.beta.chat.completions.parse(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant who knows about europe countries and gives statistics in json mode"
        },
        {
            "role": "user",
            "content": "What are the top 10 popular cities of France and what are the city population of men, and women?"
        }
    ],
    model=model,
    response_format=CityDataObject
)

parsed_result = response.choices[0].message.parsed
print(parsed_result.top_cities[0].men_population)