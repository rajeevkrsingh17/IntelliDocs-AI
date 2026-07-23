import chromadb
import scripts.vector_store

class MockVoyageEmbeddingFunction(chromadb.EmbeddingFunction):
    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        return [[0.0] * 512 for _ in input]

if not scripts.vector_store._EF_VOYAGE:
    scripts.vector_store._EF_VOYAGE = MockVoyageEmbeddingFunction()
