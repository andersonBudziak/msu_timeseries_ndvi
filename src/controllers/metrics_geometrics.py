import pandas as pd

class PhenologyMetrics:
    def __init__(self, phenology_df, ndvi_df ):
        self.phenology_df = phenology_df
        self.ndvi_df = ndvi_df

    def days_between(self, start_event, end_event):
        """Calculate the number of days between two phenological events."""
        start_date = self.phenology_df.loc[self.phenology_df['Phenologic'] == start_event, 'Date'].values[0]
        end_date = self.phenology_df.loc[self.phenology_df['Phenologic'] == end_event, 'Date'].values[0]
        return (end_date - start_date ).astype('timedelta64[D]').astype(int)

    def vertical_difference(self, start_event, end_event):
        """Calculate the vertical difference (in NDVI value) between two events."""
        start_value = self.phenology_df.loc[self.phenology_df['Phenologic'] == start_event, 'Value'].values[0]
        end_value = self.phenology_df.loc[self.phenology_df['Phenologic'] == end_event, 'Value'].values[0]
        return end_value - start_value

    def horizontal_difference(self, start_event, end_event):
        """Calculate the horizontal difference (in days) between two events."""
        return self.days_between(start_event, end_event)
    
    def percentil_difference(self):
        start_date = self.phenology_df.loc[self.phenology_df['Phenologic'] == 'bos_abs', 'Date'].values[0]
        end_date = self.phenology_df.loc[self.phenology_df['Phenologic'] == 'eos_abs', 'Date'].values[0]

        # Filtrar as linhas entre as datas especificadas
        mask = (self.ndvi_df['date'] >= pd.to_datetime(start_date)) & (self.ndvi_df['date'] <= pd.to_datetime(end_date))
        filtered_data = self.ndvi_df.loc[mask]

        # Calcular o valor do percentil na coluna NDVI
        percentile_value = filtered_data['savitzky_golay'].quantile(85 / 100)

        # Contar quantos valores de NDVI estão acima do valor do percentil
        return (filtered_data['savitzky_golay'] > percentile_value).sum()
    
    def derivate_metrics(self):
        # Assuming phenology_metrics is an instance of a class with these methods
        df_metrics = pd.DataFrame([
            {'Value': self.days_between('vos_start', 'vos_end'),
            'Phenologic': 'Days between vos_end and vos_start'},

            {'Value': self.days_between('bos_abs', 'eos_abs'),
            'Phenologic': 'Days between bos_abs and eos_abs'},

            {'Value': self.vertical_difference('eos_abs', 'pos'),
            'Phenologic': 'Vertical difference between eos_abs and pos'},

            {'Value': self.horizontal_difference('pos', 'eos_abs'),
            'Phenologic': 'Horizontal difference between pos and eos_abs'},

            {'Value': self.horizontal_difference('vos_start', 'eos_abs'),
            'Phenologic': 'Horizontal difference between vos_start and eos_abs'},

            {'Value': self.vertical_difference('vos_start', 'eos_abs'),
            'Phenologic': 'Vertical difference between vos_start and eos_abs'},

            {'Value': self.horizontal_difference('bos_abs', 'vos_end'),
            'Phenologic': 'Horizontal difference between vos_end and bos_abs'},

            {'Value': self.vertical_difference('vos_start', 'bos_abs'),
            'Phenologic': 'Vertical difference between vos_start and bos_abs'},

            {'Value': self.percentil_difference(),
            'Phenologic': 'Count 85% percentiles days between bos_abs and eos_abs'}
        ])

        # Concatenate rows into a new DataFrame
        self.phenology_df = pd.concat([self.phenology_df, df_metrics], ignore_index=True)

        return self.phenology_df

