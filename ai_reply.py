from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_reply(email_body: str) -> str:
    prompt = f"""You are a professional email assistant.
Read the following email and write a polite, helpful, and concise reply.

Email:
{email_body}

Reply:"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text.strip()
