from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np

class StackedRegressor(BaseEstimator, ClassifierMixin):
    def __init__(self, classifier, regressor):
        self.classifier = classifier
        self.regressor = regressor

    def fit(self, X, y):
        class_labels = pd.Series(np.where(y>0,1,0))

        self.classifier.fit(X,class_labels)

        pred_class_labels = self.classifier.predict(X)
        pred_class_labels_df = pd.DataFrame(
            pred_class_labels, columns = ['pred_class_label'])

        X = X.reset_index(drop=True)
        pred_class_labels_df = pred_class_labels_df.reset_index(drop=True)
        X = X.join(pred_class_labels_df)
        self.regressor.fit(X,y)

        print(self.classifier.__class__.__name__, ",",
              self.regressor.__class__.__name__)

    def predict(self, X):

        class_predict = self.classifier.predict(X)
        class_predict_df = pd.DataFrame(
             class_predict, columns = ['pred_class_label'])
        X = X.reset_index(drop=True)
        class_predict_df = class_predict_df.reset_index(drop=True)
        X = X.join(class_predict_df)
        regressor_predict = self.regressor.predict(X)
        regressor_predict = np.where(regressor_predict<0,0,regressor_predict)

        return regressor_predict

    def score(self, X, y):
        return np.sqrt(np.mean((y - self.predict(X))**2))

    def clf_score(self, X, y):
        y_true = pd.Series(np.where(y>0,1,0))
        y_pred = self.classifier.predict(X)
        return precision_recall_fscore_support(y_true, y_pred,
                                               average='macro')
