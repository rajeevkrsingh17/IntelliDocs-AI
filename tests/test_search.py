import sys
from pathlib import Path

# Add scripts directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

from search import BM25


def test_bm25_ranking():
    corpus = [
        "The quick brown fox jumps over the lazy dog",
        "Python is a great programming language for AI and machine learning",
        "Information retrieval systems use vector search and BM25 keyword matching",
    ]

    bm25 = BM25(corpus)

    # Query matching exact words in document 2
    scores_python = bm25.get_scores("Python programming AI")
    # Document 2 (index 1) should have the highest score
    best_doc_idx = scores_python.index(max(scores_python))
    assert best_doc_idx == 1

    # Query matching exact words in document 3
    scores_ir = bm25.get_scores("vector search BM25")
    best_doc_idx_ir = scores_ir.index(max(scores_ir))
    assert best_doc_idx_ir == 2


def test_bm25_cache_hits():
    """
    Test that retrieve_relevant_chunks successfully caches the BM25 scorer
    and retrieves from the cache on subsequent queries.
    """
    from unittest.mock import patch
    from search import retrieve_relevant_chunks, _BM25_CACHE, get_collection
    
    collection = get_collection()
    
    # Add dummy document to verify retrieval
    collection.add(
        ids=["dummy_chunk_1", "dummy_chunk_2"],
        documents=["This is a dummy document about search optimization.", "Caching results makes it faster."],
        embeddings=[[0.1] * 768, [0.2] * 768],
        metadatas=[{"document_name": "dummy.txt", "session_id": "test_session", "chunk": 1, "page": 1},
                   {"document_name": "dummy.txt", "session_id": "test_session", "chunk": 2, "page": 1}]
    )
    
    try:
        # Clear the cache to start clean
        _BM25_CACHE.cache.clear()
        
        with patch('search.get_embeddings') as mock_get_embeddings:
            mock_get_embeddings.return_value = [[0.1] * 768]
            
            # First search (Cache Miss)
            res1 = retrieve_relevant_chunks("dummy search", n_results=2, session_id="test_session")
            assert len(_BM25_CACHE.cache) == 1
            
            # Record the cached objects
            cache_key = list(_BM25_CACHE.cache.keys())[0]
            cached_val = _BM25_CACHE.get(cache_key)
            assert cached_val is not None
            bm25_scorer_1, _, _ = cached_val
            
            # Second search (Cache Hit)
            res2 = retrieve_relevant_chunks("dummy speed", n_results=2, session_id="test_session")
            assert len(_BM25_CACHE.cache) == 1
            cached_val_2 = _BM25_CACHE.get(cache_key)
            bm25_scorer_2, _, _ = cached_val_2
            
            assert bm25_scorer_1 is bm25_scorer_2
            
    finally:
        # Clean up dummy data from collection
        collection.delete(ids=["dummy_chunk_1", "dummy_chunk_2"])
