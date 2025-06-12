# from Artūras Vellemaa
from ollama import embeddings
import chromadb

def get_embedding(fact):
    return embeddings(model='nomic-embed-text', prompt=fact)

def get_embeddings(prompt_list):
    result = []
    for fact in prompt_list:
        result.append(get_embedding(fact))
    return result

def init_chroma():
    client = chromadb.Client()
    collection = client.get_or_create_collection("my_collection")
    return (client, collection)
        
(chroma_client, chroma_collection) = init_chroma()
facts = ["The sun is a star.", "The blue whale is a mammal.", 
        "The komodo dragon is a lizard.", "The tarantula is an arachnid", 
        "The great white shark is a fish"]
embedding_collection = get_embeddings(facts)
    
for i in range(0, len(embedding_collection)):
    chroma_collection.upsert(documents=facts[i],ids=[f"fact-{i+1}"], 
                            embeddings=[embedding_collection[i].embedding], 
                             metadatas=[{"source": "homework", "name": "arturas"}])

while True:
    query = input("Please ask something\n")
    
    if(('exit' or 'stop') in query):
        break
    
    embedded_query = get_embedding(query)
        
    result = chroma_collection.query(query_embeddings=[embedded_query.embedding], n_results=1)
        
    print(result["documents"])
    print(result["distances"])
    print(result["metadatas"])