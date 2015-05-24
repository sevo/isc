import numpy as np

class EuclideanOperator:
    def distance(self, a, b):
        return np.sqrt(np.sum((a - b)**2))
