from sentence_transformers import SentenceTransformer
#from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

#Load Model
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Model loaded successfully")

## Created a vectorized knowledge base 

kb = [
    "How can I reset my password?",
    "Where can I check my order status?",
    "How to contact customer support?",
    "What is the refund policy",
    "How to update my billing information?"
]

# Encode all KB entries 
kb_embeddings= model.encode(kb,convert_to_numpy=True)

print("kb_embeddings",kb_embeddings)
## Dimension of vector and Creating FAISS index

dimension = kb_embeddings.shape[1]
print(dimension)
index = faiss.IndexFlatL2(dimension)

index.add(kb_embeddings)
## build a Faiss index with embeddings

def search_kb(query:str, top_k: int =1):
    """Return most similar vectors from vector store """

    ## Encoding user query into vector embedding
    query_encode = model.encode([query],convert_to_numpy=True)

    ## Search in FAISS index
    D,I = index.search(query_encode,k=top_k) ## Distences = D, Indices = I

    if len(I[0]) > 0:
        return kb[I[0][0]]
    
    return "No relevant info found in VD"