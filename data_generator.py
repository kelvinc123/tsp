
import numpy as np

class DataGenerator:

    def __init__(self, n):

        self.min_x = 0
        self.min_y = 0
        self.max_x = 100
        self.max_y = 100
        self.n = n

    def generate(self):

        return np.random.randint([self.min_x, self.min_y],
            [self.max_x, self.max_y], (self.n, 2))
