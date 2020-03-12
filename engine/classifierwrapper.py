import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score
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

    @abstractmethod
    def label(self, predictions):
        # Method to label the classifier's predictions
        pass

    def accuracy(self, predicted, actual):
        return accuracy_score(predicted, actual)
    
    def precision(self, predicted, actual):
        return precision_score(predicted, actual)
    
    def recall(self, predicted, actual):
        return recall_score(predicted, actual)

    def cross_validate(self, x_vals, y_vals, fraction_training, iterations):
        x_vals = np.array(x_vals)
        y_vals = np.array(y_vals)
        length = len(x_vals)
        indices = list(range(length))
        accuracies = []
        n_training_samples = int(fraction_training * length)

        for _ in range(iterations):
            np.random.shuffle(indices)

            training_indices = indices[:n_training_samples]
            validation_indices = indices[n_training_samples:]

            train_x = x_vals[training_indices]
            train_y = y_vals[training_indices]

            valid_x = x_vals[validation_indices]
            valid_y = y_vals[validation_indices]

            self.fit(train_x, train_y)
            predicted = self.predict(valid_x)
            pred_labels = self.label(predicted)
            accuracies.append(self.accuracy(pred_labels, valid_y))
        
        return {'accuracies': accuracies, 
                'mean': np.mean(accuracies), 
                'std dev': np.std(accuracies)}
