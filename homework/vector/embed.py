from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com"
model = "text-embedding-3-small"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def get_embedding(text: str):
    response = client.embeddings.create(
    input=text,
    model=model,
    )
    return response.data[0].embedding


def get_embeddings(texts: list[str]):
    response = client.embeddings.create(
    input=texts,
    model=model,
    )
    embedding_objects_list = response.data
    return [eo.embedding for eo in embedding_objects_list]