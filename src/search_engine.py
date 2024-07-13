from rank_bm25 import BM25Okapi

from src.reranker import Reranker


class SearchEngine:
    def __init__(self, db, texts):
        self.db = db
        self.texts = texts
        self.corpus = [doc.page_content for doc in texts]
        self.bm25 = BM25Okapi([doc.split() for doc in self.corpus])
        self.reranker = Reranker()

    def hybrid_search(self, query, alpha=0.5, top_k=10):
        semantic_results = self.db.similarity_search_with_score(query, k=top_k)
        bm25_scores = self.bm25.get_scores(query.split())

        combined_scores = []
        for i, (doc, score) in enumerate(semantic_results):
            combined_score = alpha * (1 - score) + (1 - alpha) * bm25_scores[i]
            combined_scores.append((doc, combined_score))

        sorted_results = sorted(combined_scores, key=lambda x: x[1], reverse=True)
        return self.reranker.rerank(query, sorted_results, top_k=top_k)
