import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# Load environment variables from .env file
load_dotenv()

# --- Configuration for Azure AI OpenAI ---
token = os.getenv("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com"

# Define the embedding model name (must match what was used in ingest.py)
embedding_model_name = "text-embedding-3-small"

# Define the chat model name (a generative model)
chat_model_name = "gpt-4o-mini" # Using a suitable chat model

# Check if the token is available
if not token:
    raise ValueError("GITHUB_TOKEN environment variable not set.")
if not endpoint:
    raise ValueError("Azure AI endpoint not defined.")

# Initialize the OpenAI client (used implicitly by LangChain components)
azure_openai_client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

print("--- Initializing Chatbot ---")

# --- Load Embeddings Model ---
embedding = OpenAIEmbeddings(
    model=embedding_model_name,
    openai_api_base=endpoint,
    openai_api_key=token,
)

# --- Load Persisted Chroma DB ---
persist_directory = "chroma_db"
if not os.path.exists(persist_directory):
    print(f"Error: Chroma DB not found at '{persist_directory}'. Please run ingest.py first.")
    exit()

print(f"Loading Chroma DB from: {persist_directory}")
vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding
)

# Create a retriever from the vector database
retriever = vectordb.as_retriever(search_kwargs={"k": 3})
print("Chroma DB loaded and retriever created.")

# --- Initialize Chat Model ---
print(f"Initializing ChatOpenAI with model: {chat_model_name}")
llm = ChatOpenAI(
    model=chat_model_name,
    openai_api_base=endpoint,
    openai_api_key=token,
    temperature=0.7 # Adjust temperature for creativity (0.0 for factual, 1.0 for creative)
)

# --- Define the RAG Prompt Template ---
# This template tells the LLM how to use the retrieved context
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Answer the user's question ONLY based on the following context. If you don't know the answer from the context, politely say that you don't have enough information."),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ]
)

# --- Build the RAG Chain using LangChain Expression Language (LCEL) ---
# This chain orchestrates the retrieval and generation steps directly
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()} # Retrieve context and pass question
    | prompt_template # Format with the prompt
    | llm # Pass to the language model
    | StrOutputParser() # Parse the string output
)
print("RAG Chain initialized. Ready to answer questions.")

# --- Chat Loop ---
print("\n--- Start Chatbot (Type 'exit' to quit) ---")
while True:
    user_query = input("You: ")
    if user_query.lower() == 'exit':
        print("Chatbot: Goodbye!")
        break

    try:
        # Invoke the RAG chain with the user's query
        response = rag_chain.invoke(user_query)
        print(f"Chatbot: {response}")
    except Exception as e:
        print(f"Chatbot Error: An error occurred while processing your request: {e}")
        print("Please check your API key, endpoint, and model names.")