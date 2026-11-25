import torch
from transformers import AutoTokenizer, AutoModel

model_name = "bert-base-uncased"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

sentence = "Python is used for machine learning."

inputs = tokenizer(
    sentence,
    return_tensors="pt"
)

with torch.no_grad():
    outputs = model(**inputs)

# Token-level embeddings
token_embeddings = outputs.last_hidden_state

print("Shape:", token_embeddings.shape)