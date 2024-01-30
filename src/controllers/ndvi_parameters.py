import numpy as np
import pandas as pd

class NDVIParameters:
    def __init__(self, ndvi):
        self.ndvi = ndvi

    def calculate_parameters(self):
        """
        Calculate various parameters related to NDVI.
        
        Returns:
        -------
        rolling_mean_forw : pandas DataFrame
            Rolling mean forward.
        rolling_mean_back : pandas DataFrame
            Rolling mean backward.
        t_min : pandas DataFrame
            DataFrame containing various calculated parameters.
        t_left_min : pandas DataFrame
            DataFrame containing left minimum values.
        t_right_min : pandas DataFrame
            DataFrame containing right minimum values.
        """
        t_left_min = np.zeros(shape=(self.ndvi.shape[1], 2))
        t_right_min = np.zeros(shape=(self.ndvi.shape[1], 2))

        for i in range(self.ndvi.shape[1]):
            if self.ndvi.iloc[:, i].mean() > 0:
                t_left_min[i, 1] = self.ndvi.iloc[100:int(self.ndvi.iloc[:, i].idxmax()), i].min()
                t_left_min[i, 0] = self.ndvi.iloc[100:int(self.ndvi.iloc[:, i].idxmax()), i].idxmin()

                t_right_min[i, 1] = self.ndvi.iloc[int(self.ndvi.iloc[:, i].idxmax()):330, i].min()
                t_right_min[i, 0] = self.ndvi.iloc[int(self.ndvi.iloc[:, i].idxmax()):330, i].idxmin()

        t_left_min = pd.DataFrame(t_left_min)
        t_right_min = pd.DataFrame(t_right_min)

        mstd_area = np.zeros(shape=(self.ndvi.shape[1], 2))
        for i in range(self.ndvi.shape[1]):
            if self.ndvi.iloc[:, i].mean() > 0:
                mstd_area[i, 0] = np.mean(
                    np.array(self.ndvi.iloc[(self.ndvi.index >= t_left_min.iloc[i, 0]) & (self.ndvi.index <= t_right_min.iloc[i, 0]), i].index))
                mstd_area[i, 1] = np.std(
                    np.array(self.ndvi.iloc[(self.ndvi.index >= t_left_min.iloc[i, 0]) & (self.ndvi.index <= t_right_min.iloc[i, 0]), i].index))
            else:
                mstd_area[i, 0] = 0
                mstd_area[i, 1] = 0
        mstd_area = pd.DataFrame(mstd_area)
        mstd_area.columns = ['mean', 'std']

        t_min = pd.concat([t_left_min, t_right_min], axis=1)
        t_min.columns = ['left_min_doy', 'left_min_val', 'right_min_doy', 'right_min_val']
        t_min = pd.concat([t_min, mstd_area], axis=1)
        t_min['SLE'] = np.round(t_min.iloc[:, 5] * 2, 0)
        t_min['lag'] = np.round(self.ndvi.shape[0] - t_min.iloc[:, 6], 0)

        self.ndvi = pd.concat([self.ndvi, self.ndvi, self.ndvi], axis=0)
        self.ndvi.index = range(0, self.ndvi.shape[0])

        rolling_mean_forw = np.zeros(shape=self.ndvi.shape)
        rolling_mean_back = np.zeros(shape=self.ndvi.shape)
        typew = 'boxcar'

        for i in range(self.ndvi.shape[1]):
            rolling_mean_forw[:, i] = self.ndvi.iloc[:, i].rolling(window=int(t_min.iloc[i, 7]), win_type=typew).mean()
            rolling_mean_back[:, i] = self.ndvi.iloc[:, i][::-1].rolling(window=int(t_min.iloc[i, 7])).mean()[
                ::-1].shift()

        rolling_mean_forw = pd.DataFrame(rolling_mean_forw)
        rolling_mean_back = pd.DataFrame(rolling_mean_back)

        self.ndvi = self.ndvi.iloc[365:730, :]
        self.ndvi.index = range(0, self.ndvi.shape[0])
        rolling_mean_forw = rolling_mean_forw.iloc[365:730, :]
        rolling_mean_forw.index = range(0, rolling_mean_forw.shape[0])
        rolling_mean_back = rolling_mean_back.iloc[365:730, :]
        rolling_mean_back.index = range(0, rolling_mean_back.shape[0])

        return rolling_mean_forw, rolling_mean_back, t_min, t_left_min, t_right_min