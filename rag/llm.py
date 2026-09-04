from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_CHAT_MODEL, GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(
    model=GEMINI_CHAT_MODEL,
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
    max_output_tokens=1024,
)
