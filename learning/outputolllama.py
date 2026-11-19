import ollama

response = ollama.chat(
    model="llama3.1:latest",
    messages=[
        {"role": "user", "content": "Explain AI"}
    ],
)

print("Response:", response.message.content)
