import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

class VectorDB:

    def __init__(self, embedding_model:str="all-MiniLM-L6-v2", chunk_size: int = 500):
        self.model = SentenceTransformer(embedding_model)
        self.chunk_size=500
        self.index = None
        self.chunks=[]
        self.sources = []

    def get_chunks(self, content: str, chunk_size: int = 500):
        return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    
    def add(self, content: str):
        chunks = self.get_chunks(content, self.chunk_size)
        embeddings = self.model.encode(chunks, show_progress_bar=True)

        dim = embeddings[0].shape[0]

        if self.index == None:
            self.index = faiss.IndexFlatL2(dim)
        
        self.index.add(np.array(embeddings))
        self.chunks.extend(chunks)
    

    def search(self, query: str, top_k: int = 3):
        if self.index is None:
            raise RuntimeError("VectorDB is empty. Add files before searching.")
        
        query_embedding = self.model.encode([query])
        D, I = self.index.search(np.array(query_embedding), top_k)

        return '\n\n'.join([f"Content: {self.chunks[i]}" for idx, i in enumerate(I[0])
        ])