
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import preprocess as prep

class Plot:

    @staticmethod
    def decision_map(model, n):
        df = prep.results_to_df(model, n)
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        ax = sns.heatmap(df)
        ax.xaxis.set_ticks_position('top')
        _ = ax.set_title("Decision Variables")
        plt.show()

    @staticmethod
    def subset_map(subset_constraints, n):
        subset_length = list(range(1, n))
        total_subset = []
        print(f"Number of restricted subset: {len(subset_constraints)} subsets")
        for i in range(1, n):
            total_subset.append(len([subset for subset in subset_constraints if len(subset) == i]))
        data = pd.DataFrame({"total_subset":total_subset}, index=subset_length)
        fig, ax = plt.subplots(1, 1, figsize = (14, 6))
        ax = sns.barplot(data.index, data["total_subset"])
        plt.show()

    @staticmethod
    def plot_locations(locations, model):
        locations_df = pd.DataFrame(locations, columns=["x", "y"])
        fig, ax = plt.subplots(1, 1, figsize = (10, 7))
        ax = sns.scatterplot(locations_df["x"], locations_df["y"], s = 100)

        # add arcs
        for i in model.i:
            for j in model.i:
                if model.SELECT[i, j].value == 1:
                    x_line = [locations_df.iloc[i-1,0], locations_df.iloc[j-1,0]]
                    y_line = [locations_df.iloc[i-1,1], locations_df.iloc[j-1,1]]
                    ax.plot(x_line, y_line, color = "red", linewidth=2)

        plt.show()
