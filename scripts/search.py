import math
import re
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# ------------------------------------------------
# Load Embedding Model
# ------------------------------------------------

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------------------------------------
# BM25 Keyword Search Implementation
# ------------------------------------------------

class BM25:
    """
    A lightweight, pure-Python implementation of the Okapi BM25 retrieval algorithm.
    """
    def __init__(self, corpus, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus)
        self.avg_doc_len = 0
        self.doc_lengths = []
        self.doc_term_freqs = []
        self.idf = {}
        self._initialize(corpus)

    def _tokenize(self, text):
        return re.findall(r'\w+', text.lower())

    def _initialize(self, corpus):
        total_len = 0
        term_doc_freq = {}  # Number of documents containing term t

        for doc in corpus:
            tokens = self._tokenize(doc)
            doc_len = len(tokens)
            self.doc_lengths.append(doc_len)
            total_len += doc_len
            
            # Term frequencies in this document
            tf = {}
            for token in tokens:
                tf[token] = tf.get(token, 0) + 1
            self.doc_term_freqs.append(tf)
            
            # Document frequency for terms
            for token in tf.keys():
                term_doc_freq[token] = term_doc_freq.get(token, 0) + 1

        self.avg_doc_len = total_len / self.corpus_size if self.corpus_size > 0 else 0
        
        # Calculate IDF for each term
        for term, freq in term_doc_freq.items():
            self.idf[term] = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0)

    def get_scores(self, query):
        query_tokens = self._tokenize(query)
        scores = []
        
        for i in range(self.corpus_size):
            score = 0.0
            doc_len = self.doc_lengths[i]
            tf = self.doc_term_freqs[i]
            
            for token in query_tokens:
                if token in tf:
                    term_freq = tf[token]
                    numerator = term_freq * (self.k1 + 1)
                    denominator = term_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len)
                    score += self.idf.get(token, 0.0) * (numerator / denominator)
            scores.append(score)
            
        return scores


# ------------------------------------------------
# ChromaDB
# ------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "chroma_db"


def get_collection():
    """
    Always get the latest collection from ChromaDB.
    """

    client = chromadb.PersistentClient(path=str(DB_PATH))

    return client.get_collection("intellidocs")


# ------------------------------------------------
# Retrieve Relevant Chunks (Hybrid QA Search)
# ------------------------------------------------

def retrieve_relevant_chunks(query, n_results=10, document_name=None):
    """
    Retrieve the most relevant chunks using Hybrid Search (BM25 + Dense vector similarity).
    Results are merged using Reciprocal Rank Fusion (RRF).
    """

    try:
        collection = get_collection()
    except Exception:
        raise RuntimeError(
            "No documents indexed yet. Please upload a document first."
        )

    print("\n" + "=" * 80)
    print("HYBRID SEARCH QUERY")
    print("=" * 80)
    try:
        print(query)
    except UnicodeEncodeError:
        print(query.encode('ascii', errors='replace').decode('ascii'))

    total_chunks = collection.count()
    if total_chunks == 0:
        return {"documents": [], "metadata": []}

    # 1. DENSE VECTOR SEARCH
    query_embedding = model.encode([query]).tolist()
    # Retrieve top 20 candidates for dense search
    vector_n = min(30, total_chunks)
    
    where_clause = {"document_name": document_name} if document_name else None
    
    vector_results = collection.query(
        query_embeddings=query_embedding,
        n_results=vector_n,
        where=where_clause,
        include=["documents", "metadatas"],
    )

    vec_ids = vector_results.get("ids", [[]])[0]
    vec_docs = vector_results.get("documents", [[]])[0]
    vec_metas = vector_results.get("metadatas", [[]])[0]

    # Map details for quick lookup
    id_to_doc = {}
    id_to_meta = {}
    for vid, vdoc, vmeta in zip(vec_ids, vec_docs, vec_metas):
        id_to_doc[vid] = vdoc
        id_to_meta[vid] = vmeta

    # 2. BM25 KEYWORD SEARCH
    # Retrieve documents to run BM25 locally
    all_data = collection.get(
        where=where_clause,
        include=["documents", "metadatas"]
    )
    all_ids = all_data.get("ids", [])
    all_docs = all_data.get("documents", [])
    all_metas = all_data.get("metadatas", [])

    for aid, adoc, ameta in zip(all_ids, all_docs, all_metas):
        id_to_doc[aid] = adoc
        id_to_meta[aid] = ameta

    # Build index & score
    bm25_scorer = BM25(all_docs)
    bm25_scores = bm25_scorer.get_scores(query)
    
    # Sort and take top 20 candidates
    bm25_ranked = sorted(zip(all_ids, bm25_scores), key=lambda x: x[1], reverse=True)
    bm25_top_n = min(30, len(bm25_ranked))
    bm25_ids = [bid for bid, bscore in bm25_ranked[:bm25_top_n]]

    # 3. RECIPROCAL RANK FUSION (RRF)
    # RRF constant k
    k = 60
    rrf_scores = {}

    # Rank lists
    for rank, rid in enumerate(vec_ids, start=1):
        rrf_scores[rid] = rrf_scores.get(rid, 0.0) + (1.0 / (k + rank))

    for rank, rid in enumerate(bm25_ids, start=1):
        rrf_scores[rid] = rrf_scores.get(rid, 0.0) + (1.0 / (k + rank))

    # Sort candidates by RRF score descending
    sorted_candidates = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
    top_candidates = sorted_candidates[:n_results]

    final_documents = []
    final_metadata = []

    print("\n" + "=" * 80)
    print("RETRIEVED CHUNKS (HYBRID RRF)")
    print("=" * 80)

    for i, (cid, score) in enumerate(top_candidates, start=1):
        doc_text = id_to_doc[cid]
        doc_meta = id_to_meta[cid]
        final_documents.append(doc_text)
        final_metadata.append(doc_meta)

        # Print debug log
        print(f"\nChunk {i} (RRF Score: {score:.5f})")
        print("-" * 60)
        try:
            print(f"Document : {doc_meta.get('document_name')}")
        except UnicodeEncodeError:
            print(f"Document : {str(doc_meta.get('document_name')).encode('ascii', errors='replace').decode('ascii')}")
        print(f"Type     : {doc_meta.get('document_type')}")
        print(f"Chunk    : {doc_meta.get('chunk')}")
        print(f"Page     : {doc_meta.get('page')}")
        
        # Show ranks in original sources
        vec_rank = vec_ids.index(cid) + 1 if cid in vec_ids else "N/A"
        bm25_rank = bm25_ids.index(cid) + 1 if cid in bm25_ids else "N/A"
        print(f"Dense Rank: {vec_rank} | BM25 Rank: {bm25_rank}")
        
        print("\nPreview:\n")
        try:
            print(doc_text[:500])
        except UnicodeEncodeError:
            print(doc_text[:500].encode('ascii', errors='replace').decode('ascii'))

    print("=" * 80)

    return {
        "documents": final_documents,
        "metadata": final_metadata,
    }


# ------------------------------------------------
# Retrieve Full Document Content (Compare Documents)
# ------------------------------------------------

def retrieve_document_content(document_name):
    """
    Retrieve all chunks belonging to a specific document.
    Returns the complete reconstructed document text.
    """

    try:
        collection = get_collection()

    except Exception:
        raise RuntimeError(
            "No documents indexed yet. Please upload a document first."
        )

    results = collection.get(
        where={
            "document_name": document_name
        },
        include=[
            "documents",
            "metadatas",
        ],
    )

    documents = results.get("documents", [])
    metadata = results.get("metadatas", [])

    if not documents:
        return {
            "name": document_name,
            "content": "",
            "metadata": [],
        }

    # Sort chunks by chunk number
    paired = sorted(
        zip(documents, metadata),
        key=lambda x: x[1].get("chunk", 0)
    )

    full_text = "\n\n".join(
        chunk for chunk, _ in paired
    )

    return {
        "name": document_name,
        "content": full_text,
        "metadata": metadata,
    }


# ------------------------------------------------
# Retrieve Multiple Documents
# ------------------------------------------------

def retrieve_multiple_documents(document_names):
    """
    Retrieve multiple documents for comparison.
    """

    documents = []

    for name in document_names:

        doc = retrieve_document_content(name)

        if doc["content"].strip():
            documents.append(doc)

    return documents


# ------------------------------------------------
# CLI Test
# ------------------------------------------------

if __name__ == "__main__":

    from scripts.llm import generate_answer

    print("\n" + "=" * 60)
    print("IntelliDocs AI")
    print("=" * 60)

    while True:

        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        try:

            retrieved = retrieve_relevant_chunks(
                query=question,
                n_results=5,
            )

            documents = retrieved["documents"]
            metadata = retrieved["metadata"]

            if not documents:
                print("\nNo relevant information found.")
                continue

            context = "\n\n".join(documents)

            answer = generate_answer(
                question=question,
                context=context,
            )

            print("\n" + "=" * 60)
            print("ANSWER")
            print("=" * 60)
            print(answer)

            print("\n" + "=" * 60)
            print("SOURCES")
            print("=" * 60)

            for i, meta in enumerate(metadata, start=1):

                print(f"\nSource {i}")
                print(f"Document : {meta.get('document_name')}")
                print(f"Type     : {meta.get('document_type')}")
                print(f"Page     : {meta.get('page')}")
                print(f"Chunk    : {meta.get('chunk')}")

        except Exception:

            import traceback
            traceback.print_exc()