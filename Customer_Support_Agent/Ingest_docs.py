import chromadb
from chromadb.config import Settings
import os
## Initialise chroma client with persistent directory

print("Current working directory : ",os.getcwd())
client = chromadb.Client(Settings(persist_directory="./chroma_db",anonymized_telemetry=False))

## Creating collection , collection is like table in db where we keep documents , embeddings, metadata , id etc
collection = client.get_or_create_collection("support_docs")
collection.add(
    ids=["1"],
    documents = ["This is a test document"],
    metadatas = [{"source":"demo"}]
)

print("✅ Document added successfully!")
print("Database stored at:", os.path.abspath("./chroma_db"))

print(collection)
