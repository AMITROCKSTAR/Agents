from sentence_transformers import SentenceTransformer


def embedding_model(data:str):
    ## Initialise embedding model
    model = SentenceTransformer("all-MiniLM-L6-V2")

    ## Creating embedding
    embedding = model.encode(data).tolist()

    return embedding