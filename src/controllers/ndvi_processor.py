import numpy as np
import pandas as pd
from tsmoothie.smoother import LowessSmoother

class NDVIProcessor:
    def __init__(self, df, sample="Sample_0", date='2021-01-01'):
        self.df = df
        self.sample = sample
        self.date = date

    def _calculate_moving_average(self):
        """
        Calculates the moving average of the specified sample column.
        """
        df_example = self.df.loc[:, ['Date', self.sample]]
        df1 = pd.DataFrame()
        df1['Moving Average'] = df_example[self.sample].rolling(window=2, center=True).mean()
        return df1, df_example

    def _identify_and_remove_outliers(self, df1, df_example):
        """
        Identifies and removes outliers based on the specified threshold.
        """
        df1['Ddfation'] = df_example[self.sample] - df1['Moving Average']
        threshold = 0.6 * df1['Ddfation'].std()
        df1['Outlier'] = abs(df1['Ddfation']) > threshold
        df_filtered = df_example[~df1['Outlier']].copy()
        return df_filtered

    def _smooth_and_resample(self, df_filtered):
        """
        Smooths the data and resamples it using interpolation.
        """
        aa = np.array(df_filtered[self.sample], dtype=np.float64)
        smoother = LowessSmoother(smooth_fraction=0.1, iterations=1)
        smoother.smooth(aa)
        low, up = smoother.get_intervals('prediction_interval')
        smooth_cotton = smoother.smooth_data
        df_filtered[f'{self.sample}_smooth'] = smooth_cotton.flatten()
        df_filtered.set_index('Date', inplace=True)
        df_resampled = df_filtered[f'{self.sample}_smooth'].resample('D', origin=self.date).asfreq()
        data_resampled_interpolated = df_resampled.interpolate(method='polynomial', order=7)
        return data_resampled_interpolated

    def process_ndvi(self):
        """
        Main function to process NDVI data and return the resulting DataFrame.
        """
        df1, df_example = self._calculate_moving_average()
        df_filtered = self._identify_and_remove_outliers(df1, df_example)
        data_resampled_interpolated = self._smooth_and_resample(df_filtered)
        ndvi = np.array(data_resampled_interpolated.reset_index(drop=True))
        ndvi_n = {'Value1': ndvi, 'Value2': ndvi}
        ndvi_df = pd.DataFrame(ndvi_n)
        return ndvi_df