import chromadb
from chromadb.config import Settings
import os
from Embedding_model import embedding_model
import os
import uuid


print("Current working directory:", os.getcwd())
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection("support_docs")

def vector_db(documents, metadatas=None):
    """Insert new documents and embeddings into the Chroma vector database."""
    if not documents:
        raise ValueError("No documents provided for embedding.")

    # Compute embeddings
    embeddings = embedding_model(documents)
    if not embeddings or len(embeddings) != len(documents):
        raise ValueError("Embedding generation failed or mismatch.")

    # Generate unique IDs
    ids = [f"doc_{uuid.uuid4()}" for _ in documents]

    # Add metadata
    if metadatas is None:
        metadatas = [{"source": "FAQ"} for _ in documents]

    # Insert into Chroma
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"✅ Added {len(documents)} documents to 'support_docs' collection.")
    return True


def query_text(query,n_results=3):
     query_embedding = embedding_model([query])
     results = collection.query(query_embeddings=query_embedding,n_results=n_results)
     
     return results["documents"][0], results["metadatas"][0]
