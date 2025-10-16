import chromadb
from chromadb.config import Settings
import os
from Embedding_model import embedding_model

print("Current working directory : ",os.getcwd())
client = chromadb.PersistentClient(path='./chroma_db')

## Creating collection , collection is like table in db where we keep documents , embeddings, metadata , id etc
collection = client.get_or_create_collection("support_docs")

def vector_db(documents,metadatas=None):
     ## Initialise chroma client with persistent directory
     embeddings = embedding_model(documents)

     ids = [str(i+1+len(collection.get()["documents"])) for i in range(len(documents))]

     if metadatas is None:
          metadatas = [{"source":"FAQ"} for _ in documents]
     collection.add(
         ids = ids,
         documents = documents,
         embeddings = embeddings,
         metadatas = metadatas
     )

def query_text(query,n_results=3):
     query_embedding = embedding_model([query])
     results = collection.query(query_embeddings=query_embedding,n_results=n_results)
     
     return results["documents"][0], results["metadatas"][0]