
import numpy as np
import pandas as pd

class Preprocess:

    # function to get euclidian distance between two vectors
    @staticmethod
    def euc_dist(v1, v2):
        return round(np.linalg.norm(v1 - v2), 8)

    # functino to generate dictionary
    @staticmethod
    def generate_dist_dict(arr):
        '''
        Generate dictionary using 1 as the first index
        '''
        n = len(arr)
        dist_dict = {}
        for i in range(n):
            for j in range(n):
                dist_dict[(i+1, j+1)] = Preprocess.euc_dist(arr[i], arr[j])
        return dist_dict

    @staticmethod
    def results_to_df(model, n):
        '''
        Function to convert optimal solution to data frame
        '''
        df = np.zeros((n, n))
        for i in model.i.ordered_data():
            for j in model.i.ordered_data():
                df[i-1, j-1] = model.SELECT[i, j].value
        df = pd.DataFrame(df).astype('int32')
        df.columns = model.i.ordered_data()
        df.index = model.i.ordered_data()
        return df

    