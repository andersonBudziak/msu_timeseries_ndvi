import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, ndvi, pheno_metrics, t_left_min, t_right_min, t_min):
        self.ndvi = ndvi
        self.pheno_metrics = pheno_metrics
        self.t_left_min = t_left_min
        self.t_right_min = t_right_min
        self.t_min = t_min

    def plot_metrics(self, a=0):
        df1 = self.ndvi.iloc[:, a]
        x = np.array(self.ndvi.iloc[int(np.array(self.ndvi.iloc[(self.ndvi.index == self.pheno_metrics.iloc[a, 0]), a].index)):int(np.array(self.ndvi.iloc[(self.ndvi.index == self.pheno_metrics.iloc[a, 2]), a].index)) + 1, a].index)
        y = np.array(self.ndvi.iloc[(self.ndvi.index >= self.pheno_metrics.iloc[a, 0]) & (self.ndvi.index <= self.pheno_metrics.iloc[a, 2]), a])

        plt.figure(num=None, figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')

        plt.plot(df1, marker=None, markerfacecolor='lightgreen', color='skyblue', label='NDVI Curve')
        plt.plot(self.pheno_metrics.iloc[a, 0], self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 0], a], marker='o', color='green')
        plt.text(self.pheno_metrics.iloc[a, 0] - 20, self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 0], a], 'Start', fontsize=12)

        plt.plot(self.pheno_metrics.iloc[a, 1], self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 1], a], marker='o', color='steelblue')
        plt.text(self.pheno_metrics.iloc[a, 1], self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 1], a], 'Peak', fontsize=12)

        plt.plot(self.pheno_metrics.iloc[a, 2], self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 2], a], marker='o', color='red')
        plt.text(self.pheno_metrics.iloc[a, 2], self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 2], a], 'End', fontsize=12)

        plt.plot(self.t_left_min.iloc[a, 0], self.t_left_min.iloc[a, 1], marker='o', color='orange')
        plt.text(self.t_left_min.iloc[a, 0], self.t_left_min.iloc[a, 1], 'Left Minima', fontsize=12)
        plt.plot(self.t_right_min.iloc[a, 0], self.t_right_min.iloc[a, 1], marker='o', color='orange')
        plt.text(self.t_right_min.iloc[a, 0], self.t_right_min.iloc[a, 1], 'Right Minima', fontsize=12)

        plt.fill_between(x, y, color='lemonchiffon', alpha=0.3, label='Large Integral')
        plt.fill_between(x, y, (self.t_min.iloc[a, 1] + self.t_min.iloc[a, 3]) / 2, color='mediumaquamarine', alpha=0.4, label='Small Integral')

        plt.text(self.pheno_metrics.iloc[a, 1] - 20, .4, 'Active Vegetation', rotation=20, fontsize=12)

        plt.axhline((self.t_min.iloc[a, 1] + self.t_min.iloc[a, 3]) / 2, color='red', linestyle='--', xmin=0.32, xmax=0.815, label='Base Level')
        plt.axvline(self.pheno_metrics.iloc[a, 0], color='tan', linestyle='--', ymin=0.16, ymax=0.88, label='Amplitude')

        plt.xlabel('Day of Year', fontsize=12)
        plt.ylabel('NDVI', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid()

        plt.show()

        return None
