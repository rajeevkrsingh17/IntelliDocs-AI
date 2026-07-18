import os
import time
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Create Gemini Client
# -----------------------------
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question, context):
    """
    Generates an answer using Gemini based only on the retrieved document context.
    """

    prompt = f"""
You are an AI assistant for document question answering and document comparison.

You must answer ONLY using the provided context.

The context may contain information from one or more uploaded PDF documents.

Rules:

1. If the user asks a normal question, answer using the retrieved context.

2. If the user asks to compare documents or asks for differences or similarities:

- Clearly mention each document by its filename.
- Explain similarities.
- Explain differences.
- If only one document discusses the topic, mention that.

3. Never invent information.

4. If the answer cannot be found in the provided context, reply exactly:

"I could not find this information in the uploaded document(s)."

=========================
Retrieved Context
=========================

{context}

=========================
User Question
=========================

{question}

=========================
Answer
=========================
"""

    # Retry if Gemini is temporarily busy
    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error = str(e)

            # Retry if server is busy
            if "503" in error or "UNAVAILABLE" in error:
                print(f"Gemini busy... Retrying ({attempt + 1}/3)")
                time.sleep(5)
                continue

            # Quota exceeded
            if "429" in error or "RESOURCE_EXHAUSTED" in error:
                return (
                    "Gemini API quota exceeded.\n"
                    "Please wait a few minutes and try again."
                )

            # Any other error
            return f"Gemini API Error:\n{error}"

    return "Gemini service is currently unavailable. Please try again later."