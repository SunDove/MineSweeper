import numpy as np
import json
from engine.datagen import DataGenerator

class AIEngine:

    def __init__(self):
        pass

    def generate_data(self):
        data_set = DataGenerator().get_data_set()
        with open('dataset.json', 'w') as f:
            f.write(json.dumps(data_set))
