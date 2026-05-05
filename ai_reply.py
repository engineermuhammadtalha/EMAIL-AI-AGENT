from groq import Groq
from config import GEMINI_API_KEY

client = Groq(api_key="your_groq_api_key")

def generate_reply(email_body: str) -> str:
    prompt = f"""You are a professional email assistant.
Read the following email and write a polite, helpful, and concise reply.

Email:
{email_body}

Reply:"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
