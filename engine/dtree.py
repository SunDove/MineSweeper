from engine.classifierwrapper import ClassifierWrapper
from sklearn.tree import DecisionTreeClassifier


class DecisionTreeWrapper(ClassifierWrapper):

    def __init__(self, max_depth=8):
        self._classifier = DecisionTreeClassifier(max_depth=max_depth)
        self._model = None

    def fit(self, x_vals, y_vals):
        self._model = self._classifier.fit(x_vals, y_vals)

    def predict(self, x_vals):
        if self._model:
            return self._classifier.predict_proba(x_vals)
        else:
            raise TypeError('Classifier model not fit yet.')
