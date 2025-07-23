"""File for storing and searching for relevant articles."""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class ArticleEmbeddingSearch:
    """Store articles as embeddings and search for most relevant articles to used in conjunction with client URLs for ad generation."""
    def __init__(self, articles_df: pd.DataFrame):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.articles_df = articles_df
        self.article_summaries = articles_df['summary'].apply(lambda x: x['article_summary']).tolist()
        self.articles_df['embedding'] = self._store_articles(self.article_summaries)


    def _store_articles(self, article_summaries: list[str]) -> list:
        """Store article summaries as embeddings."""
        article_embeddings = self.model.encode(article_summaries)
        return article_embeddings.tolist()

    def search(self, query_str: str, top_k: int = 5, from_date: datetime = datetime.now() - timedelta(days=30)) -> list:
        """Search for top k most relevant articles newer than from_date."""
        filtered_df = self.articles_df[self.articles_df['Published date'] >= from_date]
        if filtered_df.empty:
            return []
        query_embed = self.model.encode([query_str])
        embeddings = np.vstack(filtered_df['embedding'].values)
        similarities = cosine_similarity(query_embed, embeddings)[0]
        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        # Return the corresponding summaries
        top_summaries = filtered_df.iloc[top_indices]['summary'].apply(lambda x: x['article_summary']).tolist()
        return [summary for summary in top_summaries if summary]  # Remove any empty summaries if filter led to them being kept. 