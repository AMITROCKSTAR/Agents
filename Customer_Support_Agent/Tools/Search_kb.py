from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from Embedding_model import embedding_model
from Ingest_docs import query_text


def search_kb(query:str, top_k: int =1):
    
    docs , _= query_text(query,top_k)
    if docs:
        return "\n".join(docs)
    else:
        "No relevant info found in knowledge base"

