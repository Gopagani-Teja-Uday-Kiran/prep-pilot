import numpy as np

vector_a = np.array([1, 2, 3])
vector_b = np.array([2, 3, 4])

# Dot product
dot_product = np.dot(vector_a, vector_b)

# Cosine similarity
cosine_similarity = dot_product / (
    np.linalg.norm(vector_a) *
    np.linalg.norm(vector_b)
)

# Euclidean distance
euclidean_distance = np.linalg.norm(
    vector_a - vector_b
)

print("Dot product:", dot_product)
print("Cosine similarity:", cosine_similarity)
print("Euclidean distance:", euclidean_distance)