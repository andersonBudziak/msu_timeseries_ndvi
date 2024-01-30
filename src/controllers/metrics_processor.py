import numpy as np
import pandas as pd

class PhenologicalMetrics:
    def __init__(self, ndvi, rolling_mean_forw, rolling_mean_back, t_min, t_left_min, t_right_min):
        self.ndvi = ndvi
        self.rolling_mean_forw = rolling_mean_forw
        self.rolling_mean_back = rolling_mean_back
        self.t_min = t_min
        self.t_left_min = t_left_min
        self.t_right_min = t_right_min
        self.pheno_metrics = self._calculate_phenological_metrics()

    def _calculate_phenological_metrics(self):
        pheno_metrics = np.zeros(shape=(self.ndvi.shape[1], 3))

        for i in range(self.ndvi.shape[1]):
            if (self.ndvi.iloc[:, i].mean() > 0):
                int_f = np.argwhere(np.diff(np.sign(self.ndvi.iloc[:, i] - self.rolling_mean_forw.iloc[:, i]))).flatten()
                int_f = int_f[(int_f > 110) & (int_f < 200)]
                if (int_f.size != 0):
                    pheno_metrics[i, 0] = np.array(int_f[len(int_f) - 1])

                pheno_metrics[i, 1] = self.ndvi.iloc[:, i].idxmax()

                int_b = np.argwhere(np.diff(np.sign(self.ndvi.iloc[:, i] - self.rolling_mean_back.iloc[:, i]))).flatten()
                int_b = int_b[(int_b > 250) & (int_b < 360)]
                if (int_b.size != 0):
                    pheno_metrics[i, 2] = np.array(int_b[0])

        pheno_metrics = pd.DataFrame(pheno_metrics)
        pheno_metrics.columns = ['start', 'peak', 'end']
        pheno_metrics = pheno_metrics.replace(0, np.nan)
        pheno_metrics['len_seas'] = pheno_metrics.end - pheno_metrics.start
        pheno_metrics['amplitude'] = (self.t_min.left_min_val + self.t_min.right_min_val) / 2

        return pheno_metrics

    def _calculate_rate_inc(self, a):
        if ((np.isnan(self.pheno_metrics.start[a])) or (np.isnan(self.pheno_metrics.end[a]))):
            return np.nan
        else:
            return (np.array(self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 1], a]) - \
                   np.array(self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 0], a])) / \
                   (np.array(self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 1], a].index) - \
                   np.array(self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 0], a].index))

    def _calculate_rate_dec(self, a):
        if ((np.isnan(self.pheno_metrics.start[a])) or (np.isnan(self.pheno_metrics.end[a]))):
            return np.nan
        else:
            return np.abs(np.abs(np.array(self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 1], a]) - \
                                 np.array(self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 2], a])) / \
                                 (np.array(self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 1], a].index) - \
                                 np.array(self.ndvi.iloc[np.array(self.ndvi.iloc[:, a].index) == self.pheno_metrics.iloc[a, 2], a].index)))

    def _calculate_cycl_fr(self, a):
        if ((np.isnan(self.pheno_metrics.start[a])) or (np.isnan(self.pheno_metrics.end[a]))):
            return np.nan
        else:
            return np.round(np.trapz(self.ndvi.iloc[(self.ndvi.index >= self.pheno_metrics.iloc[a, 0]) & \
                                (self.ndvi.index <= self.pheno_metrics.iloc[a, 2]), a] - \
                                self.ndvi.iloc[(self.ndvi.index >= self.pheno_metrics.iloc[a, 0]) & \
                                (self.ndvi.index <= self.pheno_metrics.iloc[a, 2]), a].min()), 2)

    def _calculate_perm_fr(self, a):
        if ((np.isnan(self.pheno_metrics.start[a])) or (np.isnan(self.pheno_metrics.end[a]))):
            return np.nan
        else:
            return np.round(np.trapz(self.ndvi.iloc[(self.ndvi.index >= self.t_left_min.iloc[a, 0]) & \
                                (self.ndvi.index <= self.t_right_min.iloc[a, 0]), a] - \
                                self.ndvi.iloc[(self.ndvi.index >= self.t_left_min.iloc[a, 0]) & \
                                (self.ndvi.index <= self.t_right_min.iloc[a, 0]), a].min()), 2)

    def get_pheno_metrics(self):
        return self.pheno_metrics

    def get_rate_inc(self):
        return [self._calculate_rate_inc(a) for a in range(self.ndvi.shape[1])]

    def get_rate_dec(self):
        return [self._calculate_rate_dec(a) for a in range(self.ndvi.shape[1])]

    def get_cycl_fr(self):
        return [self._calculate_cycl_fr(a) for a in range(self.ndvi.shape[1])]

    def get_perm_fr(self):
        return [self._calculate_perm_fr(a) for a in range(self.ndvi.shape[1])]