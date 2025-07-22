"""File for storing and searching for relevant articles."""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class ArticleEmbeddingSearch:
    """Store articles as embeddings and search for most relevant articles to used in conjunction with client URLs for ad generation."""
    def __init__(self, article_summaries: list[str]):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.article_summaries = article_summaries
        self.article_embeddings = self._store_articles(article_summaries)

    def _store_articles(self, article_summaries: list[str]) -> None:
        """Store article summaries as embeddings."""
        article_embeddings = self.model.encode(article_summaries)
        self.article_embeddings = article_embeddings.tolist()

    def search(self, query_str: str, top_k: int = 5) -> list:
        """Search for top k most relevant articles."""
        query_embed = self.model.encode([query_str])
        similarities = cosine_similarity(query_embed, self.article_embeddings)
        most_similar_indices = np.argsort(similarities[0])[-top_k:][::-1]
        return [self.article_summaries[i] for i in most_similar_indices]