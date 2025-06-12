from os import environ
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = environ.get("GEMINI_API_KEY")

print("Gemini API Key cargada:", GEMINI_API_KEY is not None)

