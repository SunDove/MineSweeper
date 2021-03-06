import numpy as np
import json
from engine.datagen import DataGenerator
from engine.dtree import DecisionTreeWrapper
from engine.rforest import RandomForestWrapper
import constants as C
Spaces = C.Spaces

class AIEngine:

    def __init__(self):
        pass

    def cross_validate_dtree(self, data, fraction_training, iterations, max_depth=10):
        self._wrapper = DecisionTreeWrapper(max_depth=max_depth)
        return self._wrapper.cross_validate(data[0], data[1], fraction_training, iterations)

    def train_decision_tree(self, data, max_depth=10):
        self._wrapper = DecisionTreeWrapper(max_depth=max_depth)
        self._wrapper.fit(data[0], data[1])

    def train_random_forest(self, data, max_depth=10):
        self._wrapper =RandomForestWrapper(max_depth=max_depth)
        self._wrapper.fit(data[0], data[1])

    def get_prediction(self, features):
        return self._wrapper.predict(features)

    def generate_data(self, n_observations=10):
        data_set = DataGenerator(n_observations=n_observations).get_data_set()
        with open('dataset.json', 'w') as f:
            f.write(json.dumps(data_set))

    def vectorize_data(self, data):
        if len(data) < 1:
            return

        feature_vectors = []
        labels = []

        n = len(data[0])
        block_width = int(np.sqrt(n))

        for block in data:
            multi_dim_block = np.reshape(block, (block_width, block_width))
            unknown_squares = (multi_dim_block == '').astype(int)
            block_vector = []
            center = block_width//2

            for i in range(1, block_width-1):
                for j in range(1, block_width-1):
                    if i == center and j == center:
                        isBomb = True if multi_dim_block[i,j] == "True" else False
                        labels.append(isBomb)
                        continue

                    if multi_dim_block[i,j] == 'Edge':
                        block_vector.append(10000)
                        continue

                    if multi_dim_block[i,j] == repr(Spaces.FLAG):
                        block_vector.append(-10000)
                        continue

                    value = 0

                    try:
                        value = int(multi_dim_block[i,j])
                    except ValueError:
                        pass

                    # Subtract the number of unknown squares from the tile's value
                    value -= np.sum(unknown_squares[i-1:i+2, j-1:j+2])
                    value = int(value)
                    block_vector.append(value)

            feature_vectors.append(block_vector)
        return {'x': feature_vectors, 'y': labels}

    def vectorize_json(self, filename):
        with open(filename) as f:
            data = json.loads(f.read())

        features = self.vectorize_data(data)

        with open("vectorized" + filename, 'w') as f:
            f.write(json.dumps(features))

        return features
