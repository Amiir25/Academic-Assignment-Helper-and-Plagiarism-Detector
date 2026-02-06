import hashlib
import random


EMBEDDING_DIM = 1536


def embed_text(text: str) -> list[float]:
    """
    Deterministic fake embedding.
    Same text -> same vector
    Different text -> different vector
    """

    seed = int(hashlib.sha256(text.encode()).hexdigest(), 16) % (2**32)
    random.seed(seed)

    return [random.random() for _ in range(EMBEDDING_DIM)]
