import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=api_key)

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents="Carlton is a diverse inner-city suburb with strong rental activity.",
)

embedding = response.embeddings[0].values

print("Embedding dimension:", len(embedding))
print("First 5 values:", embedding[:5])