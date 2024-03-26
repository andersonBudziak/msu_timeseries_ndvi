import numpy as np
import pandas as pd
from scipy import signal

class VosPosMetrics:
    """
    A class for analyzing NDVI data to identify key phenological stages.
    
    Attributes:
        ndvi_df (pd.DataFrame): DataFrame containing NDVI data.
        order_ndvi (int): Order parameter for finding extrema in NDVI data.
    """

    def __init__(self, ndvi_df, order_ndvi):
        """
        Inicializa o NDVIAnalyzer com o DataFrame e a ordem do NDVI.

        Args:
            ndvi_df (pd.DataFrame): DataFrame contendo os dados NDVI.
            order_ndvi (int): Ordem para encontrar extremos nos dados NDVI.
        """
        self.ndvi_df = ndvi_df
        self.order_ndvi = order_ndvi

    def find_peaks(self):
        """
        Encontra os picos (máximos) nos dados NDVI.

        Returns:
            np.ndarray: Índices dos picos encontrados nos dados NDVI.
        """
        return signal.argrelextrema(self.ndvi_df['savitzky_golay'].to_numpy(), 
                                    np.greater, order=self.order_ndvi)[0]

    def find_valleys(self):
        """
        Encontra os vales (mínimos) nos dados NDVI.

        Returns:
            np.ndarray: Índices dos vales encontrados nos dados NDVI.
        """
        return signal.argrelextrema(self.ndvi_df['savitzky_golay'].to_numpy(), 
                                    np.less, order=self.order_ndvi)[0]

    def analyze_phenology(self):
        """
        Analyzes phenology, identifying phenological stages and marking them in a new DataFrame.

        Returns:
            pd.DataFrame: A new DataFrame with phenological markings.
        """
        peak_indexes = self.find_peaks()
        max_peak_index = np.argmax(self.ndvi_df['savitzky_golay'].iloc[peak_indexes])
        
        valley_indexes = self.find_valleys()
        before_valley_index = max(valley_indexes[valley_indexes < peak_indexes[max_peak_index]])
        after_valley_index = min(valley_indexes[valley_indexes > peak_indexes[max_peak_index]])

        # Create rows for the new DataFrame
        vos_start_row = pd.DataFrame({
            'Date': [self.ndvi_df.loc[before_valley_index, 'date']],
            'Value': [self.ndvi_df.loc[before_valley_index, 'savitzky_golay']],
            'Phenologic': ['vos_start']
        })

        vos_end_row = pd.DataFrame({
            'Date': [self.ndvi_df.loc[after_valley_index, 'date']],
            'Value': [self.ndvi_df.loc[after_valley_index, 'savitzky_golay']],
            'Phenologic': ['vos_end']
        })

        pos_row = pd.DataFrame({
            'Date': [self.ndvi_df.loc[peak_indexes[max_peak_index], 'date']],
            'Value': [self.ndvi_df.loc[peak_indexes[max_peak_index], 'savitzky_golay']],
            'Phenologic': ['pos']
        })

        # Concatenate rows into a new DataFrame
        phenology_df = pd.concat([vos_start_row, vos_end_row, pos_row], ignore_index=True)

        return phenology_df

        """
        Analisa a fenologia, identificando os estágios fenológicos e marcando-os no DataFrame.

        Returns:
            pd.DataFrame: DataFrame com as marcações fenológicas adicionadas.
        
        peak_indexes = self.find_peaks()
        max_peak_index = np.argmax(self.ndvi_df['savitzky_golay'].iloc[peak_indexes])
        
        valley_indexes = self.find_valleys()
        before_valley_index = max(valley_indexes[valley_indexes < peak_indexes[max_peak_index]])
        after_valley_index = min(valley_indexes[valley_indexes > peak_indexes[max_peak_index]])

        self.ndvi_df["phenologic"] = np.nan
        self.ndvi_df.loc[before_valley_index, "phenologic"] = 'vos_start'
        self.ndvi_df.loc[after_valley_index, "phenologic"] = 'vos_end'
        self.ndvi_df.loc[peak_indexes[max_peak_index], "phenologic"] = 'pos'

        return self.ndvi_df
        """
