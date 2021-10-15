
import numpy as np
import pandas as pd

from tsp import TSP
from data_generator import DataGenerator
from preprocess import Preprocess
# from plot import Plot

import warnings
warnings.simplefilter("ignore")

N = 10000
X = []
y = []
for i in range(N):
    if i % 10 == 0:
        print(f"Working on iteration {i}/{N}...", end="\r")
    n = 50
    data_gen = DataGenerator(n)

    # generate n random locations
    locations = data_gen.generate()

    # calculate distances between the locations
    distance = Preprocess.generate_dist_dict(locations)

    # put it into solver and run model
    tsp_solver = TSP()
    model = tsp_solver.run_model(distance=distance, n=n, verbose=False)

    # save it to X and y
    X.append(locations.flatten())
    y.append(Preprocess.results_to_df(model, n).values.flatten())

X = pd.DataFrame(np.array(X))
y = pd.DataFrame(np.array(y))

X.to_csv("X_big.csv", index=False, header=False)
y.to_csv("y_big.csv", index=False, header=False)


'''
n = 50
data_gen = DataGenerator(n)

# generate n random locations
locations = data_gen.generate()

# calculate distances between the locations
distance = Preprocess.generate_dist_dict(locations)

# put it into solver and run model
tsp_solver = TSP()
model = tsp_solver.run_model(distance=distance, n=n, verbose=False)

plotter = Plot()
plotter.plot_locations(locations, model)
'''