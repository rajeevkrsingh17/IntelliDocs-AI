import os
import pytest
import scripts.vector_store

# Disable Voyage embedding function globally during unit tests
# to keep them fast, offline-friendly, and safe from API daily limits.
scripts.vector_store.VOYAGE_API_KEY = None
scripts.vector_store._EF_VOYAGE = None
