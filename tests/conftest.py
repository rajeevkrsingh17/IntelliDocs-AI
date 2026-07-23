import chromadb
import scripts.vector_store

class MockGeminiEmbeddingFunction(chromadb.EmbeddingFunction):
    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        return [[0.0] * 3072 for _ in input]

if not scripts.vector_store._EF_GEMINI:
    scripts.vector_store._EF_GEMINI = MockGeminiEmbeddingFunction()
