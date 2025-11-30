from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    """Create embeddings for knowledge base similarity search"""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    async def create_embedding(self, text: str) -> list:
        """Generate embedding vector for text"""
        embedding = self.model.encode(text)
        return embedding.tolist()
    
    async def find_similar_incidents(self, query_text: str, knowledge_base: list, top_k: int = 5):
        """Find similar past incidents using cosine similarity"""
        query_embedding = await self.create_embedding(query_text)
        
        similarities = []
        for kb_entry in knowledge_base:
            kb_embedding = np.array(kb_entry['embedding'])
            similarity = np.dot(query_embedding, kb_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(kb_embedding)
            )
            similarities.append((kb_entry, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return [entry for entry, _ in similarities[:top_k]]
