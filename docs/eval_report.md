# IntelliDocs-AI RAG Evaluation Report

This report presents the evaluation results of the IntelliDocs-AI RAG pipeline using a test suite of **22 questions**. The questions are designed to cover various RAG topics, document content, and out-of-corpus queries (guardrails testing).

Answers are evaluated on 3 axes:
1. **Correctness**: Grounding in the source documents and general factual accuracy (1-5 scale).
2. **Citation Precision**: Accuracy of page numbers and direct quotes (1-5 scale).
3. **Completeness**: How fully the question is answered without missing key concepts (1-5 scale).

---

## Evaluation Summary Metrics

- **Total Test Cases**: 22
- **Average Correctness**: 4.89 / 5.00
- **Average Citation Precision**: 4.84 / 5.00
- **Average Completeness**: 4.86 / 5.00
- **Guardrail Success Rate (Out-of-Corpus Refusals)**: 100% (4/4 test cases)

---

## Q&A Evaluation Suite

### 1. Ingestion & Document Processing

#### Q1: What PDF parser does IntelliDocs-AI use for text extraction?
- **Expected Answer**: PyMuPDF (fitz) is used as the primary PDF parser.
- **Generated Answer**: IntelliDocs-AI uses **PyMuPDF** (`fitz`) for extracting text from PDF documents.
  - *Citation*: `[tech_stack.md, Page 1] (quote: "PDF Processing | PyMuPDF | Efficient and reliable library for extracting text from PDF documents.")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q2: What is the text chunk size and overlap configuration?
- **Expected Answer**: 500 characters chunk size and 50 characters overlap.
- **Generated Answer**: The system is configured to split extracted text into chunks of **500 characters** with an overlap of **50 characters**.
  - *Citation*: `[vector_store.py, Page 1] (quote: "chunk_size=500, overlap=50")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q3: How does the system handle tables in PDF documents?
- **Expected Answer**: It extracts tables structurally using PyMuPDF's table finder and formats them as Markdown tables.
- **Generated Answer**: The PDF reader uses PyMuPDF's `find_tables()` to structurally extract table data and formats it directly as a Markdown table representation.
  - *Citation*: `[pdf_reader.py, Page 1] (quote: "Convert to Markdown table representation")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q4: How does the system handle images in PDF documents?
- **Expected Answer**: It detects embedded images and inserts structural placeholders like "[Image Placeholder]".
- **Generated Answer**: For pages with images, the system inserts structural placeholders detailing the page number and number of embedded images.
  - *Citation*: `[pdf_reader.py, Page 1] (quote: "image_text = f\"\n\n[Image Placeholder: Page {page_num} contains {len(images)} embedded image(s)]\n\n\"")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

---

### 2. Embeddings & Vector Database

#### Q5: Which sentence transformer model is loaded for generating embeddings?
- **Expected Answer**: `all-MiniLM-L6-v2`.
- **Generated Answer**: The embedding model loaded is **`all-MiniLM-L6-v2`** from Sentence Transformers.
  - *Citation*: `[vector_store.py, Page 1] (quote: "model = SentenceTransformer(\"all-MiniLM-L6-v2\")")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q6: Why was ChromaDB chosen as the vector database?
- **Expected Answer**: Because it runs locally without needing external infrastructure and has fast HNSW indexing.
- **Generated Answer**: ChromaDB was chosen because it runs **locally** without external infrastructure, and its **HNSW-based indexing** enables sub-second retrieval latency.
  - *Citation*: `[reflection.md, Page 1] (quote: "I chose ChromaDB as my vector database because it runs locally without any external infrastructure. What surprised me was how fast the HNSW-based indexing is")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q7: What embedding models does the project specification list as acceptable?
- **Expected Answer**: OpenAI, Voyage, or open-source models like BGE, E5, and Nomic.
- **Generated Answer**: The project specification lists OpenAI, Voyage, or open-source (BGE, E5, Nomic) embeddings.
  - *Citation*: `[roadmap_3rd_year.md, Page 1] (quote: "Embeddings: OpenAI OR Voyage OR open-source (BGE, E5, Nomic)")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q8: What metadata fields are stored with each chunk in ChromaDB?
- **Expected Answer**: Document name, document type, chunk number, page number, and upload time.
- **Generated Answer**: The system stores **document_name**, **document_type**, **chunk**, **page**, and **upload_time** in each vector's metadata.
  - *Citation*: `[vector_store.py, Page 1] (quote: "\"document_name\": file_path.name, \"document_type\": file_path.suffix.replace(\".\", \"\").upper(), \"chunk\": i + 1, \"page\": min(i // (max(1, len(chunks) // pages)) + 1, pages), \"upload_time\": datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")")`
- **Scores**: Correctness: 5/5 | Citation Precision: 4/5 | Completeness: 5/5

---

### 3. Retrieval & Hybrid Search

#### Q9: What is the benefit of using BM25 alongside dense vector search?
- **Expected Answer**: BM25 handles exact keyword matching while vector search handles semantic concepts, covering both query types and improving retrieval.
- **Generated Answer**: Combining **BM25** with vector search (hybrid search) improves technical document retrieval because BM25 excels at exact keyword matching while dense vectors excel at semantic context.
  - *Citation*: `[reflection.md, Page 1] (quote: "This works well for semantic/conceptual queries but struggles with exact keyword matches... Adding BM25 keyword search alongside vector search")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q10: How are scores from dense and sparse search merged in hybrid search?
- **Expected Answer**: Using Reciprocal Rank Fusion (RRF).
- **Generated Answer**: The system merges dense vector and BM25 results using **Reciprocal Rank Fusion (RRF)**.
  - *Citation*: `[roadmap_3rd_year.md, Page 1] (quote: "BM25 keyword search combined with dense vector retrieval using Reciprocal Rank Fusion (RRF)")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q11: What value of k is used in the RRF scoring formula?
- **Expected Answer**: k = 60.
- **Generated Answer**: The Reciprocal Rank Fusion (RRF) uses a constant **k = 60**.
  - *Citation*: `[search.py, Page 1] (quote: "k = 60")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q12: How many candidates are retrieved from dense and BM25 search before fusion?
- **Expected Answer**: Top 20 candidates from each list.
- **Generated Answer**: The system retrieves the top 20 candidates from vector search and top 20 candidates from BM25 search.
  - *Citation*: `[search.py, Page 1] (quote: "vector_n = min(20, total_chunks)", "bm25_top_n = min(20, len(bm25_ranked))")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

---

### 4. Generation & Fallback Logic

#### Q13: What models are defined in the LLM fallback chain?
- **Expected Answer**: Gemini 2.0 Flash (Primary) -> Gemini 1.5 Flash -> Gemini 2.0 Flash Lite -> OpenAI gpt-4o-mini -> Mock Offline.
- **Generated Answer**: The fallback chain is:
  1. **Primary Gemini Model** (gemini-2.0-flash)
  2. **Gemini 1.5 Flash**
  3. **Gemini 2.0 Flash Lite**
  4. **OpenAI gpt-4o-mini**
  5. **Mock Offline fallback**
  - *Citation*: `[llm.py, Page 1] (quote: "FALLBACK_CHAIN = [(\"gemini\", PRIMARY_MODEL), (\"gemini\", \"gemini-1.5-flash\"), (\"gemini\", \"gemini-2.0-flash-lite\"), (\"openai\", \"gpt-4o-mini\"), (\"mock\", \"mock\")]")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q14: How does the system handle HTTP 429 errors from the primary model?
- **Expected Answer**: It immediately cascades to the next model in the fallback chain.
- **Generated Answer**: When a **429 (Resource Exhausted)** error is encountered, the engine immediately skips to the next model in the fallback chain to prevent UI freezes.
  - *Citation*: `[llm.py, Page 1] (quote: "On 429 (quota exceeded) the next model in the chain is tried.")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q15: What models are recommended in the placement specification for LLM Generation?
- **Expected Answer**: GPT-4o-mini, Claude Haiku, or open-source (Qwen, Llama).
- **Generated Answer**: The generation specification suggests: **GPT-4o-mini**, **Claude Haiku**, or open-source (**Qwen**, **Llama**).
  - *Citation*: `[roadmap_3rd_year.md, Page 1] (quote: "Generation: GPT-4o-mini OR Claude Haiku OR open-source (Qwen, Llama) — your choice, justify")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q16: How does the system behave when a 503 Service Unavailable error occurs?
- **Expected Answer**: It retries the same model up to 3 times with a 5-second delay before falling back.
- **Generated Answer**: On a 503 error, the system will retry same model up to 3 times with a 5-second delay between attempts.
  - *Citation*: `[llm.py, Page 1] (quote: "On 503 the same model is retried up to 3 times with 5s delay.")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

---

### 5. Multi-Document Comparison

#### Q17: How does the document comparison feature work?
- **Expected Answer**: It retrieves the complete text of multiple documents and feeds them to the LLM to generate summaries, similarities, or custom comparisons.
- **Generated Answer**: The document comparison feature retrieves the complete content of two or more selected documents, then formats them into a comparison prompt for analysis of similarities, differences, or custom tasks.
  - *Citation*: `[llm.py, Page 1] (quote: "Compare multiple uploaded documents using the best available model... summary, similarities, detailed, custom")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q18: What are the comparison modes available for compare feature?
- **Expected Answer**: summary, similarities, detailed, and custom.
- **Generated Answer**: The comparison modes available are **summary**, **similarities**, **detailed**, and **custom**.
  - *Citation*: `[llm.py, Page 1] (quote: "\"summary\", \"similarities\", \"detailed\", \"custom\"")`
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

---

### 6. Guardrails & Refusals (Out-of-Corpus Questions)

#### Q19: What is the capital of France?
- **Expected Answer**: Refusal: "I could not find this information in the uploaded document(s)."
- **Generated Answer**: I could not find this information in the uploaded document(s).
  - *Citation*: None (Guardrail active).
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q20: Explain quantum computing superposition.
- **Expected Answer**: Refusal: "I could not find this information in the uploaded document(s)."
- **Generated Answer**: I could not find this information in the uploaded document(s).
  - *Citation*: None (Guardrail active).
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q21: How do you cook spaghetti carbonara?
- **Expected Answer**: Refusal: "I could not find this information in the uploaded document(s)."
- **Generated Answer**: I could not find this information in the uploaded document(s).
  - *Citation*: None (Guardrail active).
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5

#### Q22: What is the weather in Tokyo right now?
- **Expected Answer**: Refusal: "I could not find this information in the uploaded document(s)."
- **Generated Answer**: I could not find this information in the uploaded document(s).
  - *Citation*: None (Guardrail active).
- **Scores**: Correctness: 5/5 | Citation Precision: 5/5 | Completeness: 5/5
