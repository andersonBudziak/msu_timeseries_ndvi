import pandas as pd
import plotly.graph_objects as go

class PhenologyVisualizer:
    """
    A class to visualize phenology data using NDVI and metrics data.
    
    Attributes:
        ndvi_df (pd.DataFrame): DataFrame containing NDVI data.
        phenology_df (pd.DataFrame): DataFrame containing phenology metrics data.
    """

    def __init__(self, ndvi_df, phenology_df):
        """
        Constructs all the necessary attributes for the PhenologyVisualizer object.

        Args:
            ndvi_df (pd.DataFrame): DataFrame containing NDVI data.
            phenology_df (pd.DataFrame): DataFrame containing phenology metrics data.
        """
        self.ndvi_df = ndvi_df
        self.phenology_df = phenology_df

    def convert_dates(self):
        """Converts the 'timestamps' and 'Date' columns in the dataframes to datetime objects."""
        self.ndvi_df['timestamps'] = pd.to_datetime(self.ndvi_df['timestamps'])
        self.phenology_df['Date_dt'] = pd.to_datetime(self.phenology_df['Date'])

    def calculate_plot_range(self):
        """
        Calculates and adjusts the start and end dates for the plot based on the phenology data.
        
        Returns:
            tuple: A tuple containing the start and end dates for the plot.
        """
        vos_start_date = self.phenology_df[self.phenology_df['Phenologic'] == 'vos_start']['Date'].min() - pd.Timedelta(days=3)
        vos_end_date = self.phenology_df[self.phenology_df['Phenologic'] == 'vos_end']['Date'].max() + pd.Timedelta(days=3)
        return vos_start_date, vos_end_date

    def create_plot(self):
        """
        Creates and displays a plot of NDVI and phenology metrics data.
        """
        vos_start_date, vos_end_date = self.calculate_plot_range()
        metric_colors = ['#B19470', '#76453B', '#304D30', '#114232', '#F7F6BB', '#FF9800', '#90D26D']
        fig = go.Figure()

        # Add NDVI and Savitzky-Golay plots
        fig.add_trace(go.Scatter(x=self.ndvi_df['timestamps'], y=self.ndvi_df['ndvi'], mode='lines', name='NDVI', line=dict(color='#114232')))
        fig.add_trace(go.Scatter(x=self.ndvi_df['timestamps'], y=self.ndvi_df['savitzky_golay'], mode='lines', name='Savitzky-Golay', line=dict(color='#4f131f', dash='dash')))

        # Add Metrics scatter plot
        for i, metric in enumerate(self.phenology_df['Phenologic'].unique()):
            color = metric_colors[i % len(metric_colors)]
            metric_df = self.phenology_df[self.phenology_df['Phenologic'] == metric]
            fig.add_trace(go.Scatter(x=metric_df['Date_dt'], y=metric_df['Value'], mode='markers', name=metric, marker=dict(color=color, size=12)))

        # Update layout
        fig.update_layout(
            height=600, width=1000,
            title_text="GCERLab Phenologics metrics",
            xaxis_title="Date", yaxis_title="NDVI",
            xaxis_range=[vos_start_date, vos_end_date],
            showlegend=True
        )

        # Show the figure
        fig.show()

