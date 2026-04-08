import joblib
import os
import ast
import numpy as np
from app.config import settings

class ErrorClassifier:
    def __init__(self, model_path=settings.MODEL_PATH, le_path=settings.LE_PATH, tfidf_path=settings.TFIDF_PATH):
        self.model_path = model_path
        self.le_path = le_path
        self.tfidf_path = tfidf_path
        
        self.model = None
        self.le = None
        self.tfidf = None
        
        # Load models
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
            if os.path.exists(self.le_path):
                self.le = joblib.load(self.le_path)
            if os.path.exists(self.tfidf_path):
                self.tfidf = joblib.load(self.tfidf_path)
        except Exception as e:
            print(f"Error loading models: {e}")

    def extract_ast_path(self, code: str) -> str:
        """
        Extract AST paths from code. Simple version for inference.
        """
        try:
            tree = ast.parse(code)
            paths = []
            for node in ast.walk(tree):
                paths.append(node.__class__.__name__)
            return " -> ".join(paths[:50]) # Limit depth
        except:
            return "SyntaxError: invalid syntax"

    def predict(self, code: str) -> str:
        """
        Predict error type from code.
        """
        if not all([self.model, self.le, self.tfidf]):
            return "Unknown"
            
        ast_path = self.extract_ast_path(code)
        combined_feature = f"{code} [AST] {ast_path}"
        
        try:
            X = self.tfidf.transform([combined_feature]).toarray()
            y_pred = self.model.predict(X)
            return self.le.inverse_transform(y_pred)[0]
        except Exception as e:
            print(f"Prediction error: {e}")
            return "Unknown"
