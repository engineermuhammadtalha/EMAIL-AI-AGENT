import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY  = os.getenv("GROQ_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def validate_config():
    missing = []
    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")
    if not EMAIL_ADDRESS:
        missing.append("EMAIL_ADDRESS")
    if not EMAIL_PASSWORD:
        missing.append("EMAIL_PASSWORD")
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)} Check your .env file.")
