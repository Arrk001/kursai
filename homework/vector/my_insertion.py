import chromadb
import embed as em
# Sukuriamas klientas sąveikai su vektorine db
client = chromadb.PersistentClient(path="./homework/vector/vector-db")
# Gaunama kolekcija, kurioje bus saugomi vektoriai ir duomenys
collection = client.get_or_create_collection(name="my_knowledge_base")


# Gauname įvestį iš naudotojo 
prompt = input("Please enter some information LLM should know: ")
new_rule_number = collection.count() + 1
id = new_rule_number

# User input embedding'as
prompt_embedding = em.get_embedding(prompt)

collection.upsert(
    documents=[prompt],
    ids=[f"fact-{new_rule_number}"],
    embeddings=[prompt_embedding],
    metadatas=[{"source": "Homework", "id": id, "student": "Lukas"}]
    )
rules_count = new_rule_number
print(f"✅ Successfully added new rule! Now there are {rules_count} rules in total")