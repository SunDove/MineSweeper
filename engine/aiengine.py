import numpy as np
import json
from engine.datagen import DataGenerator

class AIEngine:

    def __init__(self):
        pass

    def generate_data(self):
        data_set = DataGenerator().get_data_set()
        for d in data_set:
            print(len(d))
        with open('dataset.json', 'w') as f:
            f.write(json.dumps(data_set))
    
    def vectorize_data(self, data):
        if len(data) < 1:
            return
        
        feature_vectors = []
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
                        continue

                    if multi_dim_block[i,j] == 'Edge':
                        block_vector.append(-np.inf)
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
        return feature_vectors
    
    def vectorize_json(self, filename):
        with open(filename) as f:
            data = json.loads(f.read())
        
        features = self.vectorize_data(data)

        with open("vectorized" + filename, 'w') as f:
            f.write(json.dumps(features))
        