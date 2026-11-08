import os

from dotenv import load_dotenv
from anthropic import Anthropic


# .env dosyasındaki API anahtarını yükle
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found!")

# Claude API istemcisini oluştur
client = Anthropic(api_key=api_key)

# Claude'a test mesajı gönder
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=200,
    messages=[
        {
            "role": "user",
            "content": "Explain what Retrieval-Augmented Generation (RAG) is in simple terms."
        }
    ]
)

# Claude'un cevabını yazdır
print("\nClaude response:\n")

print(response.content[0].text)

print("\nAPI connection successful!")