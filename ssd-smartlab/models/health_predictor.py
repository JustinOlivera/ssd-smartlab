from sklearn.ensemble import RandomForestClassifier

class SSDHealthModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=150)

    def train(self, X, y):
        self.model.fit(X, y)

    def predict_risk(self, X):
        return self.model.predict_proba(X)[:, 1]
