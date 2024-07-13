import yaml
from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(self):
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        self.model = CrossEncoder(config["cross_encoder_model"])

    def rerank(self, query, results, top_k=5):
        pairs = [[query, doc.page_content] for doc, _ in results]
        scores = self.model.predict(pairs)
        reranked_results = [(doc, score) for (doc, _), score in zip(results, scores)]
        return sorted(reranked_results, key=lambda x: x[1], reverse=True)[:top_k]
