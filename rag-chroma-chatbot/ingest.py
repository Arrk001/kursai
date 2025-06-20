import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings # Using langchain_openai for better client integration
from langchain.vectorstores import Chroma

# Load environment variables from .env file
load_dotenv()

# --- Configuration for Azure AI OpenAI ---
# Your GitHub Token, assumed to be for authentication with Azure AI
token = os.getenv("GITHUB_TOKEN")
# Azure AI endpoint for inference
endpoint = "https://models.inference.ai.azure.com"
model_name = "text-embedding-3-small"

# Check if the token is available
if not token:
    raise ValueError("GITHUB_TOKEN environment variable not set.")
if not endpoint:
    raise ValueError("Azure AI endpoint not defined.")

# Initialize the OpenAI client for direct API calls for EMBEDDINGS (e.g., for testing or if needed directly)
# This client uses your specified embedding endpoint and API key.
azure_openai_embedding_client = OpenAI(
    base_url=endpoint,
    api_key=token,
)
print("--- Starting Document Ingestion and Embedding ---")

# --- 1. Load and Split Documents ---
docs_path = "rag-chroma-chatbot/docs" # Assuming your .txt files are in a folder named 'docs'
if not os.path.exists(docs_path):
    os.makedirs(docs_path)
    print(f"Created '{docs_path}' directory. Please place your .txt files inside it.")
    print("Exiting ingestion as no documents are available.")
    exit()

# Load documents from the 'docs' directory
print(f"Loading documents from: {docs_path}")
loader = DirectoryLoader(
    docs_path,
    loader_cls=lambda path: TextLoader(path, encoding="utf-8", autodetect_encoding=True)
)
documents = loader.load()

if not documents:
    print(f"No documents found in '{docs_path}'. Please ensure your .txt files are there.")
    exit()

print(f"Loaded {len(documents)} document(s).")

# Split documents into smaller chunks
print("Splitting documents into chunks...")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks.")

# --- 2. Create Embeddings and Chroma Vectorstore ---
print(f"Initializing OpenAIEmbeddings with model: {model_name}")

# Initialize OpenAIEmbeddings with your custom client configuration.
# This ensures that LangChain uses your Azure AI endpoint and token for embeddings.
embedding = OpenAIEmbeddings(
    model=model_name,
    openai_api_base=endpoint,
    openai_api_key=token,
    # If using 'langchain-openai' and a pre-initialized 'client' object
    # you can also do:
    # client=azure_openai_client
    # In this case, openai_api_base and openai_api_key can be omitted as client handles them.
)

# Create Chroma vectorstore from documents
# The persist_directory ensures the embeddings are saved to disk
persist_directory = "chroma_db"
print(f"Creating Chroma vector database in: {persist_directory}")
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory=persist_directory
)

# Persist the database to disk
vectordb.persist()
print("✅ Chroma DB created and persisted.")
print(f"Embeddings generated using '{model_name}' from '{endpoint}'.")

# --- Example of direct embedding call (for verification, similar to your snippet) ---
# You can remove this block if not needed for debugging/verification
try:
    print("\n--- Testing direct embedding call (for verification) ---")
    response_test = azure_openai_embedding_client.embeddings.create(
        input=["This is a test phrase.", "Another phrase for testing embeddings."],
        model=model_name,
    )
    for item in response_test.data:
        print(f"Test embedding length: {len(item.embedding)}, index: {item.index}")
    print(f"Test embedding usage: {response_test.usage}")
    print("✅ Direct embedding call successful.")
except Exception as e:
    print(f"❌ Error during direct embedding test call: {e}")

