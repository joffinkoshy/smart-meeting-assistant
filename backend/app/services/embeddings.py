try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception:
    model = None

metadata = []

def index_chunks(chunks: list):
    if model is None:
        metadata.extend(chunks)
        return [c.get('id') for c in chunks]
    embs = model.encode([c['text'] for c in chunks], convert_to_numpy=True)
    metadata.extend(chunks)
    return [c.get('id') for c in chunks]

def search(query: str, top_k: int = 5):
    if model is None:
        return metadata[:top_k]
    q_emb = model.encode([query], convert_to_numpy=True)
    return metadata[:top_k]
