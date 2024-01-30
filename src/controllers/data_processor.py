import pandas as pd

class DataProcessor:
    def __init__(self, df_data):
        self.df_data = df_data

    def _extract_inter_data(self):
        """
        Extracts the relevant data from the input DataFrame.
        """
        df_data_inter = (self.df_data.T)[4:]
        dates = df_data_inter.index
        df_data_inter = df_data_inter.reset_index(drop=True)
        return df_data_inter, dates

    def _rename_columns(self, df_data_inter):
        """
        Renames the columns of the DataFrame to 'Sample_i'.
        """
        new_column_names = [f'Sample_{i}' for i in range(df_data_inter.shape[1])]
        df_data_inter.columns = new_column_names
        return df_data_inter

    def _add_date_column(self, df_data_inter, dates):
        """
        Adds a 'Date' column to the DataFrame based on the extracted dates.
        """
        date_index = pd.to_datetime(dates)
        column_name = 'Date'
        df_data_inter.insert(0, column_name, date_index)
        return df_data_inter

    def process_data(self):
        """
        Main function to process the input data and return the resulting DataFrame.
        """
        df_data_inter, dates = self._extract_inter_data()
        df_data_inter = self._rename_columns(df_data_inter)
        df_data_processed = self._add_date_column(df_data_inter, dates)
        return df_data_processed