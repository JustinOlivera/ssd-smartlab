from sklearn.ensemble import IsolationForest

class SSDAnomalyDetector:
    def __init__(self):
        self.detector = IsolationForest(contamination=0.03)

    def fit(self, X):
        self.detector.fit(X)

    def detect(self, X):
        return self.detector.predict(X)
