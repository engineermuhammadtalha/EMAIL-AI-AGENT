from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_reply(email_body: str) -> str:
    prompt = f"""You are a professional email assistant.
Read the following email and write a polite, helpful, and concise reply.
Keep the reply short, professional and friendly.

Email:
{email_body}

Reply:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
