
# NDVI Analysis Toolkit

## Overview

This repository contains a suite of Python tools for processing and analyzing Normalized Difference Vegetation Index (NDVI) data, particularly focusing on phenology—the study of cyclic and seasonal natural phenomena. Our toolkit allows users to process geographical data, analyze NDVI metrics from satellite imagery, and visualize these metrics to understand vegetation patterns over time.

## Getting Started

### Prerequisites

- Python 3.x
- Jupyter Notebook
- Required Python libraries: `pandas`, `geopandas`, `scipy`, `plotly`, `earthengine-api`

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/andersonBudziak/msu_timeseries_ndvi.git]
   ```
2. Navigate to the cloned directory and install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Code in a Jupyter Notebook

1. Open your Jupyter Notebook environment.
2. Import the necessary modules from the toolkit:
   ```python
   from src.controllers_v2.time_series_hls import HLS
   from src.controllers_v2.plotter import PhenologyVisualizer
   from src.controllers_v2.metrics_vos_pos import VosPosMetrics
   from src.controllers_v2.metrics_bos_eso import BosEosMetrics
   from src.controllers_v2.geometry import ProcessadorGeoDataFrame
   from scipy.signal import savgol_filter
   ```
3. Set up the analysis by defining your input data and parameters.
4. Execute the code blocks to process and analyze the NDVI data.

Example:
```python
# Initialize the GeoDataFrame processor with a file path
processador = ProcessadorGeoDataFrame('path/to/your/file.gpkg')

# Extract vertices and geometry for a polygon index
vertices, geometry = processador.extract_coordinates(polygon_index)

# Process HLS data
hsl = HLS(geometry, 'start_date', 'end_date')
ndvi_df = hsl.convert_to_dataframe()

# Apply Savitzky-Golay filter to smooth the NDVI data
ndvi_df['savitzky_golay'] = savgol_filter(ndvi_df['ndvi'], window_length, polynomial_order)

# Perform VOS and POS analysis
vos_pos_analyzer = VosPosMetrics(ndvi_df, ndvi_order)
phenology_df = vos_pos_analyzer.analyze_phenology()

# Perform BOS and EOS analysis
bos_eos_analyzer = BosEosMetrics(ndvi_df, phenology_df, threshold_value)
phenology_df = bos_eos_analyzer.execute_analysis()

# Visualize the phenology data
visualizer = PhenologyVisualizer(ndvi_df, phenology_df)
visualizer.convert_dates()
visualizer.create_plot()
```

### Understanding NDVI Metrics

NDVI is a standardized index that allows you to generate an image showing the relative biomass of an area. It is particularly useful in phenology to track plant health, vegetation cover, and seasonal changes.

- **VOS (Start of Season)** and **POS (Peak of Season)** metrics help identify the onset and peak of vegetation growth.
- **BOS (Beginning of Season)** and **EOS (End of Season)** metrics are derived to indicate the start and end of the active growth period.
- The toolkit applies the Savitzky-Golay filter to smooth the NDVI time series data, enhancing the accuracy of metric identification.

This analysis is pivotal in understanding vegetation dynamics, aiding in ecological research, agricultural planning, and environmental monitoring.

## Contributing

We welcome contributions to this project. Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the [GCERLab License](https://www.gcerlab.com/).
