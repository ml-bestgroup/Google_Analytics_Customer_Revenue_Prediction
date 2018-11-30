from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np

class StackedRegressor(BaseEstimator, ClassifierMixin):  
    def __init__(self, classifier=None, regressor=None):
        self.classifier = classifier
        self.regressor = regressor
        
    def fit(self, X, class_labels, regressor_labels):
        self.classifier.fit(X,class_labels)
        self.regressor.fit(X,regressor_labels)
        
    def predict(self, X, y=None):
        class_predict = self.classifier.predict(X)
        regressor_predict = self.regressor.predict(X)
        return np.multiply(class_predict,regressor_predict)
