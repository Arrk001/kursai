# Part 1: Create and Embed Your Own Knowledge
# Create a new Python file: my_insertion.py 

#Use the embedding function from embed.py to embed 5 facts of your choice
#They can be from your favorite topic: tech, music, history, food, etc.
#Example: "The sun is a star.", "Mozart composed over 600 works."

#Insert those facts into a new Chroma collection called "my_knowledge_base"
#Use upsert() and assign IDs like "fact-1", "fact-2" ...
#Store a metadata field {"source": "homework", "student": "your_name"}


#🔍 Part 2: Semantic Search
#Create a Python file: my_search.py
#Prompt the user with input("What would you like to know? ")
#Embed their question using the same embedding model
#Use query_embeddings=[...] to find the top 2 closest facts
#Print:
#The matched fact(s)
#The distance score(s)
#The metadata of the match
#🗃️ Bonus (Optional)
#Try one or more of the following:

#Add count() logic to display total stored facts before querying
#Export all documents to a .txt file (one per line)
#Implement a check that warns if query results are far away (distance > 1.2)#

#📦 What to Submit
#Upload the following files:
#my_insertion.py
#my_search.py
#A screenshot or printout of:
#Your inserted facts
#A successful semantic search query and result

#📌 Notes
#Your collection should use OpenAI-generated embeddings, not Chroma’s default
#Use persistent storage (PersistentClient(path="./vector-db"))
#Don’t mix different embedding models in the same collection
#Clean, well-commented code is appreciated
#🏁 Example Output
#Query: What type of body is the sun?
#Match: The sun is a star.
#Distance: 0.1841
#Metadata: {"source": "homework", "student": "Ada"}