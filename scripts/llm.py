import os
import time
import traceback
from pathlib import Path

from dotenv import load_dotenv
import google.genai as genai

# ------------------------------------------------
# Load Environment Variables
# ------------------------------------------------

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Primary Gemini model from .env, fallback to gemini-3.1-flash-lite
PRIMARY_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

# ============================================================
# MODEL FALLBACK CHAIN
# ============================================================
# Format:
#   ("provider", "model_name")
#
#   provider = "gemini" → uses Google GenAI client
#   provider = "mock"   → offline fallback, no API needed
#
# On 429 (quota exceeded) the next model in the chain is tried.
# On 503 the same model is retried up to 3 times with 5s delay.
# "mock" is always the last resort.
# ============================================================

FALLBACK_CHAIN = [
    ("gemini", PRIMARY_MODEL),              # 1st: user config (gemini-3.1-flash-lite)
    ("gemini", "gemini-2.0-flash"),         # 2nd: gemini-2.0-flash
    ("gemini", "gemini-1.5-flash"),         # 3rd: gemini-1.5-flash
    ("mock",   "mock"),                     # 4th: offline mock fallback
]

# ============================================================
# Client Initialisation
# ============================================================

gemini_client = None
if GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"[WARN] Error initialising Gemini client: {e}")
else:
    print("[WARN] GEMINI_API_KEY not found. Gemini models will be skipped.")

print("=" * 60)
print("Primary Gemini Model :", PRIMARY_MODEL)
print("Fallback chain       :", [(p, m) for p, m in FALLBACK_CHAIN])
print("ENV File             :", ENV_PATH)
print("=" * 60)


# ============================================================
# Helper: Clean answer text
# ============================================================

def _clean_text(text):
    """Clean LLM output text while preserving Markdown structure and code blocks."""
    if not text:
        return ""

    cleaned = text.strip()
    
    # If the LLM wrapped the entire response in a single ```markdown ... ``` wrapper, unwrap it
    if cleaned.startswith("```markdown") and cleaned.endswith("```"):
        cleaned = cleaned[11:-3].strip()
    elif cleaned.startswith("```") and cleaned.endswith("```"):
        cleaned = cleaned[3:-3].strip()
        
    return cleaned



# ============================================================
# Helper: Call Gemini
# ============================================================

def _call_gemini(model_name, prompt):
    """
    Call a Gemini model. Returns the text response.
    Raises exception on any error.
    """
    if gemini_client is None:
        raise ValueError("Gemini client not initialised (missing API key).")
    response = gemini_client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    return response.text.strip()




# ============================================================
# Helper: Build mock response
# ============================================================

def _mock_response(prompt, task_name, models_tried):
    """Generate an offline mock response when all API models are exhausted."""
    context_part = ""
    if "DOCUMENT CONTEXT" in prompt:
        try:
            context_part = (
                prompt
                .split("DOCUMENT CONTEXT\n--------------------------------------------------\n")[1]
                .split("\n--------------------------------------------------\nQUESTION")[0]
                .strip()
            )
        except Exception:
            pass

    if task_name == "QA":
        mock_text = (
            "### [AI] [MOCK LLM FALLBACK ACTIVE]\n\n"
            "**Note:** All Gemini API models are currently exhausted "
            "or the API key is invalid/missing. "
            "Below is the relevant information retrieved from your uploaded documents "
            "matching your question:\n\n"
        )
        if context_part:
            paragraphs = [p.strip() for p in context_part.split("\n\n") if p.strip()]
            for i, p in enumerate(paragraphs[:3], 1):
                mock_text += f"{i}. {p}\n\n"
        else:
            mock_text += "No document context was found to extract an answer from."
    else:
        mock_text = (
            "### [AI] [MOCK LLM FALLBACK ACTIVE]\n\n"
            "**Note:** All Gemini API models are currently exhausted "
            "or the API key is invalid/missing. "
            "Below is a comparison overview of the selected documents based on "
            "the retrieved contents:\n\n"
        )
        if "DOCUMENT 1" in prompt:
            try:
                docs_split = prompt.split("==================================================")
                doc_index = 1
                for split in docs_split:
                    if "DOCUMENT" in split and "Content:" in split:
                        lines = split.split("\n")
                        filename = ""
                        for line in lines:
                            if "Filename:" in line:
                                filename = lines[lines.index(line) + 1].strip()
                                break
                        mock_text += (
                            f"**Document {doc_index}: {filename}**\n"
                            "- Extracted metadata and contents successfully.\n"
                            "- Running in mock comparison mode.\n\n"
                        )
                        doc_index += 1
            except Exception:
                mock_text += (
                    "Selected documents are uploaded and stored in the database. "
                    "Use a valid API to perform a detailed AI comparison."
                )
        else:
            mock_text += "Selected documents are indexed and stored. Use a valid API to compare."

    chain_info = "; ".join(f"Tried: {p}/{m} [FAILED]" for p, m in models_tried[:-1])
    chain_info += ("; " if chain_info else "") + "Tried: mock [SUCCESS]"

    return {
        "text": mock_text,
        "model_used": "mock",
        "provider_used": "mock",
        "fallback_chain": chain_info,
    }


# ============================================================
# Core: Generate with full fallback chain
# ============================================================

def _generate_with_fallback(prompt, task_name="answer"):
    """
    Attempt to generate content across the full FALLBACK_CHAIN.

    For each model:
      - Retries up to 3 times on 503 / UNAVAILABLE with 5s delay.
      - On 429 / RESOURCE_EXHAUSTED, immediately moves to next model.
      - On any other error, immediately moves to next model.

    Returns dict with keys:
        text, model_used, provider_used, fallback_chain
    """

    models_tried = []
    last_error = None

    for provider, model_name in FALLBACK_CHAIN:
        print(f"\n--- [{task_name}] Trying {provider}/{model_name} ---")
        models_tried.append((provider, model_name))

        # ---- Mock fallback (last resort) ----
        if provider == "mock":
            return _mock_response(prompt, task_name, models_tried)

        # ---- Real API call with retry on 503 ----
        for attempt in range(3):
            try:
                if provider == "gemini":
                    text = _call_gemini(model_name, prompt)
                else:
                    raise ValueError(f"Unknown provider: {provider}")

                print(f"[{task_name}] [OK] Success with {provider}/{model_name}")

                text = _clean_text(text)

                chain_info = "; ".join(
                    f"Tried: {p}/{m}" + (" [SUCCESS]" if (p, m) == (provider, model_name) else " [FAILED]")
                    for p, m in models_tried
                )

                return {
                    "text": text,
                    "model_used": model_name,
                    "provider_used": provider,
                    "fallback_chain": chain_info,
                }

            except Exception as e:
                print("\n" + "=" * 70)
                print(f"EXCEPTION with {provider}/{model_name} (attempt {attempt + 1}/3)")
                print("=" * 70)
                traceback.print_exc()
                print("=" * 70 + "\n")

                error_str = str(e)
                last_error = error_str

                # 503 / Service unavailable → retry same model
                if any(k in error_str for k in ("503", "UNAVAILABLE", "Internal")):
                    print(f"Service unavailable for {provider}/{model_name}. Retry {attempt + 1}/3 in 5s...")
                    time.sleep(5)
                    continue

                # 429 / Quota exceeded → wait 2s and retry (or skip after 3 attempts)
                if any(k in error_str for k in ("429", "RESOURCE_EXHAUSTED", "rate_limit_exceeded", "RateLimitError")):
                    print(f"Quota/rate limit hit for {provider}/{model_name}. Retrying in 2s (attempt {attempt + 1}/3)...")
                    time.sleep(2)
                    continue

                # Client not initialised (missing key) → skip to next
                if "not initialised" in error_str or "placeholder" in error_str:
                    print(f"Client not available for {provider}/{model_name}. Skipping...")
                    break

                # Any other error → skip to next model
                print(f"Non-retriable error on {provider}/{model_name}. Moving to next model...")
                break

        else:
            # All 3 503 retries exhausted
            print(f"{provider}/{model_name} unavailable after 3 retries. Trying next model...")

    # ---- All models exhausted (should not reach here with mock at end) ----
    chain_info = "; ".join(f"Tried: {p}/{m} [FAILED]" for p, m in models_tried)

    if last_error and any(k in last_error for k in ("429", "RESOURCE_EXHAUSTED", "rate_limit_exceeded")):
        return {
            "text": (
                "**All Gemini models are currently over quota.**\n\n"
                "Please wait a few minutes before trying again, or check your Gemini API key."
            ),
            "model_used": "none",
            "provider_used": "none",
            "fallback_chain": chain_info,
        }

    return {
        "text": (
            "**All AI services are currently unavailable.**\n\n"
            "Please check your API keys and try again later."
        ),
        "model_used": "none",
        "provider_used": "none",
        "fallback_chain": chain_info,
    }


# ============================================================
# Build Prompt: Question Answering
# ============================================================

def _build_qa_prompt(question, context):
    return f"""
You are IntelliDocs-AI, an expert AI document assistant specializing in Retrieval-Augmented Generation (RAG).

Your objective is to provide an exceptionally well-written, comprehensive, structured, and easy-to-read answer to the user's question using ONLY the provided DOCUMENT CONTEXT.

==================================================
STEP 1 — INTERNAL REASONING (Do NOT print this step)
==================================================

Before writing your answer, silently perform these steps in your head:
1. Read every chunk in the DOCUMENT CONTEXT carefully.
2. Identify which chunks are relevant to the user's question.
3. Detect the question type:
   - SUMMARY → user wants a high-level overview or summary.
   - EXPLANATION → user wants a concept explained step-by-step.
   - COMPARISON → user wants two or more things compared.
   - DEFINITION → user wants a term or concept defined.
   - LIST → user wants a list of items, features, steps, or examples.
   - FACTUAL → user wants specific facts, numbers, names, or dates.
   - HOW-TO → user wants a procedure or process described.
4. Plan the answer structure based on the question type (see rules below).
5. Combine information from ALL relevant chunks — never answer from just one chunk when multiple chunks contain relevant information.

==================================================
STEP 2 — ANSWER STRUCTURE (based on question type)
==================================================

Adapt your answer structure to the detected question type:

**If SUMMARY:**
- Start with a 2-3 sentence **Executive Summary**.
- Follow with **Key Points** as a bulleted list with bold sub-headings.
- End with a **Key Takeaways** section.

**If EXPLANATION:**
- Start with a concise definition or one-line answer.
- Explain step-by-step with numbered points.
- Include any examples, algorithms, or formulas found in the document.
- End with a **Key Takeaways** section.

**If COMPARISON:**
- Start with a brief introduction of the things being compared.
- Present a **Markdown comparison table** with relevant dimensions.
- Follow with a prose analysis of key similarities and differences.
- End with a **Key Takeaways** section.

**If DEFINITION:**
- Start with a clear, precise definition in bold.
- Expand with context, properties, or characteristics.
- Include any examples from the document.

**If LIST:**
- Provide a well-organized bulleted or numbered list.
- Each item should have a **bold label** followed by a description.

**If FACTUAL:**
- Lead with the direct answer (name, number, date, etc.) in bold.
- Provide supporting context from the document.

**If HOW-TO:**
- Present as numbered steps.
- Each step should have a **bold action** followed by details.

==================================================
STEP 3 — FORMATTING RULES (apply to ALL question types)
==================================================

1. **NO INLINE CITATIONS**:
   - DO NOT insert bracketed citations like `[Source: DocName, Page X]` or `(Page X)` inside your response text.
   - Keep the reading flow completely seamless, clean, and professional. Sources are displayed separately by the application.

2. **RICH & ENGAGING FORMATTING**:
   - **Bold Important Terms**: Use **bold text** generously to highlight key terms, definitions, formulas, metrics, and core concepts so the reader can scan effortlessly.
   - **Contextual Definitions**: When you first mention a domain-specific or technical term, briefly define it in parentheses or a short clause (e.g., "**Gradient Descent** (an optimization algorithm that iteratively adjusts parameters)...").
   - **Structured Points**: Organize using clear bullet points (`- `) or numbered lists (`1. `). Every point should start with a **Bold Sub-heading** (e.g., `- **Feature Selection**: Description...`).
   - **Clean Tables**: Use standard Markdown tables for comparisons, types, categories, or any structured data. Keep table text clean, readable, and properly aligned.
   - **Clean Mathematical Expressions**: Do NOT output raw or broken LaTeX delimiters like `$p(y x)$` or `$$\\\\theta$$`. Write formulas cleanly using standard readable characters/symbols (e.g., `p(y | x)`, `h_θ(x) = θ₀ + θ₁x₁ + ...`) or inside code blocks for math syntax.
   - **Examples**: If the document context contains examples, code snippets, algorithms, or case studies, extract and present them clearly. Use code blocks for code and formulas.
   - **Key Takeaways**: ALWAYS conclude with a `> **📌 Key Takeaway:**` blockquote that summarizes the answer in 1-3 sentences for quick scanning.

3. **MULTI-CHUNK SYNTHESIS**:
   - You are given multiple document chunks. Synthesize information across ALL relevant chunks into a unified, coherent answer.
   - Do NOT answer from a single chunk if other chunks contain complementary information.
   - If chunks provide conflicting information, note both perspectives.

4. **CONTENT ACCURACY & ANTI-HALLUCINATION**:
   - Base your answer STRICTLY on the provided DOCUMENT CONTEXT. Do NOT add any facts, claims, definitions, or examples that are not present in the context.
   - If the context contains only partial information, answer what you can and clearly note: `> **⚠️ Note:** The uploaded documents contain limited information on this topic. The above answer is based on the available content.`
   - If the context does not contain the answer at all, respond ONLY with: `I could not find enough information in the uploaded documents to answer this question accurately.`
   - Never guess, assume, or fill gaps with general knowledge.

--------------------------------------------------
DOCUMENT CONTEXT ({context.count(chr(10))+1} lines from retrieved chunks)
--------------------------------------------------

{context}

--------------------------------------------------
USER QUESTION
--------------------------------------------------

{question}

--------------------------------------------------
ANSWER (Clean Markdown · Bold key terms · Tables where useful · Key Takeaways at end · NO inline citations)
--------------------------------------------------
"""


# ============================================================
# Build Prompt: Document Comparison
# ============================================================

def _build_comparison_prompt(documents, comparison_type, custom_prompt=None):
    comparison_modes = {
        "summary": """
Provide a structured summary comparison:

## Document Summaries
For each document, provide a 3-5 sentence summary covering:
- Main topic and purpose
- Key arguments or content covered
- Target audience and scope

## Comparison Overview Table
Create a Markdown table comparing the documents across these dimensions:
| Dimension | Document 1 | Document 2 | ... |
|-----------|-----------|-----------|-----|
| Main Topic | ... | ... | ... |
| Scope | ... | ... | ... |
| Key Focus | ... | ... | ... |
| Depth | ... | ... | ... |

## Final Conclusion
Summarize the key differences and which document is best suited for what purpose.
""",

        "similarities": """
Provide a thorough similarities and differences analysis:

## Common Ground
List all significant similarities between the documents with **bold** labels.

## Key Differences
Present differences in a comparison table:
| Aspect | Document 1 | Document 2 | ... |
|--------|-----------|-----------|-----|

Then elaborate on the most important differences with bullet points.

## Important Observations
Highlight any notable patterns, complementary information, or contradictions.

## Conclusion
Summarize which topics overlap and where the documents diverge.
""",

        "detailed": """
Provide a comprehensive, detailed comparison:

## Executive Overview
2-3 sentences summarizing what is being compared and the overall finding.

## Individual Document Analysis
For each document, provide:
- **Summary**: 3-5 sentence overview
- **Key Topics**: Bulleted list of main topics covered
- **Strengths**: What this document covers well
- **Notable Details**: Important facts, figures, or claims

## Side-by-Side Comparison Table
Create a detailed Markdown table:
| Dimension | Document 1 | Document 2 | ... |
|-----------|-----------|-----------|-----|
| Main Topic | ... | ... | ... |
| Coverage Depth | ... | ... | ... |
| Key Concepts | ... | ... | ... |
| Unique Content | ... | ... | ... |
| Writing Style | ... | ... | ... |

## Similarities
Bulleted list of significant overlapping content.

## Differences
Bulleted list of key differences with analysis.

## Key Topics Coverage Matrix
| Topic | Doc 1 | Doc 2 | ... |
|-------|-------|-------|-----|
| Topic A | ✅ Covered | ❌ Not covered | ... |

## Final Conclusion
Comprehensive conclusion with recommendations on when to use each document.
""",

        "custom": custom_prompt or """
Follow the user's custom comparison instructions exactly.

If the user asks for:
- chapter-wise comparison → compare chapter by chapter
- interview preparation → extract interview-relevant content from each
- placement perspective → highlight practical/career-relevant differences
- advantages/disadvantages → create a pros/cons table for each document
- topic-wise comparison → compare topic by topic with a coverage matrix
- difficulty level → rate and compare complexity of each document
- learning path → suggest an order for reading the documents

Perform the comparison exactly as requested with rich formatting.
"""
    }

    document_text = ""
    for i, doc in enumerate(documents, start=1):
        document_text += f"""

==================================================
DOCUMENT {i}
==================================================

Filename:
{doc["name"]}

Content:
{doc["content"]}

"""

    return f"""
You are IntelliDocs AI, an expert document comparison assistant.

You are comparing {len(documents)} uploaded documents. Your job is to produce a thorough, well-structured, visually rich comparison.

==================================================
FORMATTING RULES
==================================================

- Use **bold** for key terms and important concepts.
- Use *italic* for emphasis and secondary details.
- Use `#` for main headings, `##` for subheadings, `###` for sub-sections.
- Use bullet points (`- `) for lists and numbered lists (`1. `) for ordered steps.
- Use `> **📌 Key Takeaway:**` blockquotes for critical insights.
- Use `inline code` for technical terms.
- Use Markdown tables (`|---|---|`) for ALL structured comparisons — tables are mandatory, not optional.
- Use code blocks for code or formula examples.

==================================================
CONTENT RULES
==================================================

1. Compare ONLY the uploaded documents. Never use outside knowledge.
2. If information is missing from a document, state "Not covered in this document" — never guess.
3. Use **bold labels** on every bullet point for scanability.
4. Provide at least ONE comparison table in every response.
5. Highlight important similarities and differences with bold formatting.
6. End with a comprehensive conclusion and a `> **📌 Key Takeaway:**` blockquote.
7. Be objective and factual in all comparisons.

--------------------------------------------------

Comparison Instructions

{comparison_modes.get(comparison_type, comparison_modes["detailed"])}

IMPORTANT:
• If comparison_type is "custom", follow the user's instructions EXACTLY.
• Do not ignore the custom prompt.
• Do not add information that is not present in the uploaded documents.

--------------------------------------------------

Documents

{document_text}

--------------------------------------------------

Comparison (with rich markdown formatting, comparison tables, and key takeaways)

"""


# ============================================================
# Public API: Question Answering
# ============================================================

def generate_answer(question, context):
    """
    Generate an answer using the RAG context.

    Falls back automatically through:
        Gemini models → mock offline fallback
    """

    prompt = _build_qa_prompt(question, context)
    result = _generate_with_fallback(prompt=prompt, task_name="QA")

    answer        = result["text"]
    model_used    = result["model_used"]
    provider_used = result["provider_used"]
    fallback_chain = result["fallback_chain"]

    print("\n" + "=" * 60)
    print(f"Provider   : {provider_used}")
    print(f"Model Used : {model_used}")
    print(f"Chain      : {fallback_chain}")
    print("=" * 60)

    return answer


# ============================================================
# Public API: Document Comparison
# ============================================================

def generate_document_comparison(
    documents,
    comparison_type="detailed",
    custom_prompt=None,
):
    """
    Compare multiple uploaded documents using the best available model.
    """

    prompt = _build_comparison_prompt(documents, comparison_type, custom_prompt)
    result = _generate_with_fallback(prompt=prompt, task_name="Comparison")

    comparison    = result["text"]
    model_used    = result["model_used"]
    provider_used = result["provider_used"]
    fallback_chain = result["fallback_chain"]

    print("\n" + "=" * 60)
    print(f"Provider   : {provider_used}")
    print(f"Model Used : {model_used}")
    print(f"Chain      : {fallback_chain}")
    print("=" * 60)

    return comparison


# ============================================================
# Quick self-test
# ============================================================

if __name__ == "__main__":

    sample_context = """
Python is a programming language created by Guido van Rossum.
Python is widely used for web development, artificial intelligence,
machine learning, automation, and data analysis.
"""

    sample_question = "Who created Python and what is it used for?"

    answer = generate_answer(sample_question, sample_context)

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)
    print(answer)
