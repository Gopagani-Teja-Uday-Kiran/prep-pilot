from sentence_transformers import SentenceTransformer

models = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "BAAI/bge-small-en-v1.5",
    "BAAI/bge-base-en-v1.5"
]

sentences = [
    "What is a Python dictionary?",
    "A dictionary stores data in key-value pairs.",
    "What is a SQL database?",
    "SQL databases store and retrieve structured data."
]

for model_name in models:

    print("\nModel:", model_name)

    model = SentenceTransformer(model_name)

    embeddings = model.encode(
        sentences,
        normalize_embeddings=True
    )

    print("Embedding shape:", embeddings.shape)
    print("Dimensions:", embeddings.shape[1])

    del model