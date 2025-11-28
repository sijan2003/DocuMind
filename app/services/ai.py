import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Choose the default model
MODEL_NAME = "gemini-flash-latest"


# -----------------------------
# 1. SUMMARY
# -----------------------------
def generate_summary(text: str) -> str:
    """
    Generates a summary using Gemini.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not found in environment variables."
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            f"Summarize this in a clear and concise way:\n\n{text}"
        )
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"


# -----------------------------
# 2. KEY POINTS
# -----------------------------
def extract_key_points(text: str) -> str:
    """
    Extract key bullet points from text.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not found in environment variables."
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            "Extract the key points from the following text. "
            "Use bullet points.\n\n"
            f"{text}"
        )
        return response.text
    except Exception as e:
        return f"Error extracting key points: {str(e)}"


# -----------------------------
# 3. PARAPHRASE
# -----------------------------
def paraphrase(text: str) -> str:
    """
    Rewrite the text with clearer, simpler wording.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not found in environment variables."
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            "Rewrite the following text in a clearer, simpler, "
            "and more natural way without changing its meaning:\n\n"
            f"{text}"
        )
        return response.text
    except Exception as e:
        return f"Error paraphrasing: {str(e)}"


# -----------------------------
# 4. ANSWER QUESTION
# -----------------------------
def answer_question(text: str, question: str) -> str:
    """
    Answer a question using ONLY the provided document.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not found in environment variables."
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            f"Here is the document:\n{text}\n\n"
            f"Answer this question using ONLY the information from the document:\n"
            f"{question}"
        )
        return response.text
    except Exception as e:
        return f"Error answering question: {str(e)}"
