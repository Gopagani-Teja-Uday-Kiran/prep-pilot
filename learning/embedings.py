from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "Python is a programming language.",
    "Python supports loops and functions.",
    "JavaScript is used for web development."
]

embeddings = model.encode(sentences)

for sentence, embedding in zip(sentences, embeddings):
    print("\nSentence:", sentence)
    print("Vector:", embedding)
    print("Dimensions:", len(embedding))