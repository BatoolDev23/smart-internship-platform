from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecommendationEngine:
    def __init__(self):
        # We will use simple english stop words. For arabic, a custom list could be used or it can just rely on TF-IDF weighting.
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def calculate_text_similarity(self, source_text, target_texts):
        """
        Calculate cosine similarity between source text and a list of target texts.
        Returns array of similarity scores.
        """
        if not source_text or not target_texts:
            return np.zeros(len(target_texts)) if target_texts else np.array([])
            
        all_texts = [source_text] + target_texts
        try:
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            # Compare the first document (source) against all others
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
            return cosine_sim.flatten()
        except ValueError:
            # In case of empty vocabulary
            return np.zeros(len(target_texts))
