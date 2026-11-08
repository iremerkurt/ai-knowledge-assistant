from app.services.embedding_service import generate_embeddings

import numpy as np


texts = [
    "Artificial Intelligence is transforming the world.",
    "Machine Learning is a subset of Artificial Intelligence.",
    "I like eating pizza."
]


embeddings = generate_embeddings(texts)

# İlk iki cümlenin benzerliği
similarity_1 = np.dot(embeddings[0], embeddings[1])

# İlk ve üçüncü cümlenin benzerliği
similarity_2 = np.dot(embeddings[0], embeddings[2])


print("Similarity between text 1 and text 2:", similarity_1)
print("Similarity between text 1 and text 3:", similarity_2)