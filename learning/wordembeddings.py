import gensim.downloader as api

# Load a pretrained Word2Vec model
model = api.load("word2vec-google-news-300")

# Get an embedding for a word
vector = model["computer"]

print("Vector:", vector)
print("Dimensions:", len(vector))

# Compare two words
similarity = model.similarity("computer", "technology")

print("Similarity:", similarity)