from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

sentences = [
    "Python is a programming language.",
    "Python is used for software development.",
    "SQL is used to manage databases."
]


embeddings = model.encode(sentences)

print("Number of sentences:", len(sentences))
print("Embedding shape:", embeddings.shape)

for i, embedding in enumerate(embeddings):
    print(f"\nSentence {i + 1}: {sentences[i]}")
    print("Dimensions:", len(embedding))
    print("First five values:", embedding[:5])