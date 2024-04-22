
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class PhenologyPlotter:
    def __init__(self, ndvi_df, phenology_df):
        self.ndvi_df = ndvi_df
        self.phenology_df = phenology_df

    def convert_dates(self):
        """Convert 'timestamps' and 'Date' in dataframes to datetime objects."""
        self.ndvi_df['timestamps'] = pd.to_datetime(self.ndvi_df['timestamps'])
        self.phenology_df['Date_dt'] = pd.to_datetime(self.phenology_df['Date'])

    def calculate_plot_range(self):
        """Calculate and adjust start and end dates for the plot based on phenology data."""
        vos_start_date = self.phenology_df[self.phenology_df['Phenologic'] == 'vos_start']['Date_dt'].min() - pd.Timedelta(days=3)
        vos_end_date = self.phenology_df[self.phenology_df['Phenologic'] == 'vos_end']['Date_dt'].max() + pd.Timedelta(days=3)
        return vos_start_date, vos_end_date

    def prepare_table(self):
        """Prepare a DataFrame for table visualization."""
        table_df = self.phenology_df[['Date_dt', 'Value', 'Phenologic']].copy()
        table_df['Date_dt'] = table_df['Date_dt'].dt.strftime('%Y-%m-%d').replace(np.nan, '–')
        table_df['Value'] = table_df['Value'].apply(lambda x: f"{x:,.3f}" if isinstance(x, float) else f"{x:,}" if isinstance(x, int) else '-')
        table_df = table_df.rename(columns={'Date_dt': 'Date', 'Value': 'Values', 'Phenologic': 'Phenologic Metrics'})
        return table_df

    def plot_data(self):
        """Create and display a Plotly graph with NDVI and phenology data."""
        self.convert_dates()
        vos_start_date, vos_end_date = self.calculate_plot_range()
        table_df = self.prepare_table()

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            specs=[[{"type": "scatter"}], [{"type": "table"}]]
        )

        # Colors and other styling
        base_color = '#642834'
        other_colors = ['#B19470', '#76453B', '#304D30', '#114232', '#F7F6BB', '#FF9800', '#90D26D']
        background_color = '#f5f5f5'

        # Adding traces
        fig.add_trace(go.Scatter(x=self.ndvi_df['timestamps'], y=self.ndvi_df['ndvi'], mode='lines', name='NDVI', line=dict(color=other_colors[3])), row=1, col=1)
        fig.add_trace(go.Scatter(x=self.ndvi_df['timestamps'], y=self.ndvi_df['savitzky_golay'], mode='lines', name='Savitzky-Golay', line=dict(color=base_color, dash='dash')), row=1, col=1)

        for i, metric in enumerate(['vos_start', 'vos_end', 'pos', 'bos_der', 'eos_der', 'bos_abs', 'eos_abs']):
            color = other_colors[i % len(other_colors)]
            metric_df = self.phenology_df[self.phenology_df['Phenologic'] == metric]
            fig.add_trace(go.Scatter(x=metric_df['Date_dt'], y=metric_df['Value'], mode='markers', name=metric, marker=dict(color=color, size=9)), row=1, col=1)

        fig.add_trace(go.Table(
            header=dict(values=['<b>Date</b>', '<b>Values</b>', '<b>Phenologic Metrics</b>'], fill_color=base_color, align='center', font=dict(color='white', size=12)),
            cells=dict(values=[table_df[col] for col in table_df.columns], fill_color=[['lightgrey', 'white']*len(self.phenology_df)], align='center', font=dict(color='darkslategray', size=11))
        ), row=2, col=1)

        df = self.ndvi_df.dropna(subset=["id"])

        fig.add_trace(go.Scatter(x=list(df['date']), y=list(df['ndvi']), mode='markers', name='HLS Images', marker=dict(color='#642834', size=5)), row=1, col=1)

        fig.update_layout(
            height=800,
            width=1000,
            title_text="GCERLab Phenologics Metrics and Expenses",
            xaxis_title="Date",
            yaxis_title="NDVI",
            xaxis_range=[vos_start_date, vos_end_date],
            plot_bgcolor=background_color,
            paper_bgcolor=background_color,
        )

        return fig
