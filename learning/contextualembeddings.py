from transformers import AutoTokenizer, TFAutoModel

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModel.from_pretrained(model_name)

sentence = "Python is used for machine learning."
inputs = tokenizer(sentence, return_tensors="tf")

outputs = model(**inputs, training=False)
token_embeddings = outputs.last_hidden_state

print("Shape:", token_embeddings.shape)
