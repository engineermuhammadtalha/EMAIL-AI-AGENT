import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_reply(email_body: str) -> str:
    prompt = f"""You are a professional email assistant.
Read the following email and write a polite, helpful, and concise reply.

Email:
{email_body}

Reply:"""
    response = model.generate_content(prompt)
    return response.text.strip()
