
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class BrandPreprocessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='spanish')
        self.is_fitted = False

    def fit(self, texts):
        self.vectorizer.fit(texts)
        self.is_fitted = True

    def transform(self, brand_input):
        text = f"{brand_input['name']} {brand_input['mission']} {brand_input['values']} {brand_input['audience']} {brand_input['sector']}"
        return self.vectorizer.transform([text]).toarray()[0]