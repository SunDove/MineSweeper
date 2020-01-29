from abc import ABC, abstractmethod


class ClassifierWrapper(ABC):


    def __init__(self):
        pass

    @abstractmethod
    def fit(self, x_vals, y_vals):
        pass

    @abstractmethod
    def predict(self, x_vals):
        pass
