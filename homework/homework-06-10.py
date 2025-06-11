import os
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np

texts = [
    "Istorija: Vilnius yra žinomas dėl savo senamiesčio, kuris įtrauktas į UNESCO pasaulio paveldo sąrašą.",
    "Architektūra: Vilniaus katedra su baltais kolonų fasadais yra vienas ryškiausių miesto architektūros pavyzdžių.",
    "Kultūra: Kiekvieną pavasarį Vilniuje vyksta tarptautinis kino festivalis „Kino pavasaris“.",
    "Gamta: Neris teka per Vilnių, suteikdama miestui žaliąsias pakrantes ir poilsio zonas.",
    "Technologijos: Vilnius sparčiai vystosi kaip startuolių centras Baltijos šalyse."
]

load_dotenv()
token = os.getenv("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com"
model = "text-embedding-3-small"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_embedding(text):
    response = client.embeddings.create(
    input=text,
    model=model,
    )
    return response.data[0].embedding

    
initial_embeddings = []

for text in texts:
    embedding = get_embedding(text)
    initial_embeddings.append(embedding)


query = input("Užduok klausimą apie Vilnių: ")

# Get the vector of semantics from AI
question_embedding = get_embedding(query)

similarities = []

for emb in initial_embeddings:
    similarity = cosine_similarity(question_embedding, emb)
    similarities.append(similarity)

best_match_index = np.argmax(similarities)

print(texts[best_match_index])