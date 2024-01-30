# NDVI Time Series Project

This is a project for analyzing NDVI (Normalized Difference Vegetation Index) time series, an index used to monitor the health and vegetation cover of a particular area over time. This repository contains scripts, sample data, and related documentation for the project.

 - DataProcessor Class:

This class is responsible for processing raw data, typically related to vegetation indices like NDVI, stored in a DataFrame format. It likely includes methods for data cleaning, normalization, and any other necessary preprocessing steps. The process_data method mentioned in the code snippet probably encapsulates these operations.

Theoretical Background: Data preprocessing is a crucial step in any data analysis or machine learning task. It involves transforming raw data into a format suitable for further analysis. Techniques such as normalization, outlier removal, and feature scaling are commonly used. In the context of remote sensing and vegetation studies, preprocessing steps may also include handling missing data, cloud masking, and atmospheric correction to ensure the quality of the data used for calculating vegetation indices like NDVI.

- NDVIProcessor Class:

This class specializes in processing NDVI data derived from remote sensing imagery. It takes the processed data from the DataProcessor class and computes the NDVI values based on the formula: NDVI = (NIR - Red) / (NIR + Red), where NIR represents near-infrared reflectance and Red represents red reflectance. The process_ndvi method likely implements this calculation for each pixel in the image.

Theoretical Background: NDVI is a widely used vegetation index that quantifies vegetation density and health based on the reflectance of near-infrared and red light. Higher NDVI values indicate denser and healthier vegetation, while lower values suggest sparse or stressed vegetation. NDVI values close to 1 typically correspond to dense vegetation, while values close to 0 indicate non-vegetated or barren areas. NDVI is calculated using satellite or aerial imagery and is valuable for various applications, including agriculture, forestry, and environmental monitoring.

- NDVIParameters Class:

This class is responsible for calculating additional parameters related to the NDVI time series data. The parameters computed may include rolling means (forward and backward), minimum NDVI values, and associated time indices (e.g., t_min, t_left_min, t_right_min). These parameters provide insights into the temporal dynamics of vegetation changes captured by the NDVI time series.

Theoretical Background: The calculation of additional parameters beyond NDVI itself is crucial for understanding vegetation dynamics over time. Rolling means (also known as moving averages) are used to smooth out short-term fluctuations and reveal underlying trends in the NDVI time series. Minimum NDVI values and associated time indices help identify critical points such as the onset and end of vegetation growth cycles, which are essential for phenological analysis and ecological studies.

- PhenologicalMetrics Class:

This class focuses on computing phenological metrics using the processed NDVI data and calculated parameters. Phenological metrics characterize the timing and duration of vegetation growth cycles, including metrics such as cyclic fraction, permanence fraction, rate of increase, and rate of decrease. These metrics provide valuable information about the seasonal dynamics of vegetation and can be used for monitoring ecosystem health and agricultural productivity.

Theoretical Background: Phenology is the study of periodic plant and animal life cycle events and how these are influenced by seasonal and interannual variations in climate and other environmental factors. Phenological metrics derived from NDVI time series data capture key phenological events such as budburst, flowering, and senescence. These metrics are essential for understanding the response of vegetation to climate change, land use practices, and disturbances.

- Plotter Class:

This class is responsible for visualizing the processed NDVI data and computed phenological metrics. It likely generates plots or graphs to illustrate trends, patterns, and relationships in the data, facilitating interpretation and analysis by stakeholders and researchers.

Theoretical Background: Data visualization plays a crucial role in exploratory data analysis and communicating findings effectively. Visual representations of NDVI time series data and phenological metrics help researchers and decision-makers understand vegetation dynamics, identify anomalies, and assess the impact of environmental factors. Various types of plots, such as time series plots, scatter plots, and histograms, may be used to visualize different aspects of the data and derived metrics.

## Overview

NDVI is calculated from satellite data, typically in remote sensing images, and provides a measure of the "greenness" or "density" of vegetation in a specific area. This project aims to:

- Analyze NDVI time series to identify vegetation patterns over time.
- Develop algorithms and tools for processing and visualizing NDVI data.
- Demonstrate the use of NDVI time series in applications such as environmental, agricultural, and forestry monitoring.

## Repository Contents

- `/scripts`: Contains Python scripts for processing and analyzing NDVI data.
- `/data`: Examples of NDVI datasets for testing and demonstration.
- `/documentation`: Technical documentation, tutorials, and usage examples.

## How to Use

1. Clone this repository to your local machine.
2. Explore the different directories to access scripts, data, and documentation.
3. Follow the instructions in the `README.md` files in each directory to understand how to use and contribute to the project.

## Contributions

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Open an issue to discuss your idea or suggestion.
2. Fork the repository and make changes in your own branch.
3. Submit a pull request with your changes, referencing the relevant issue.

## License

This project is licensed under the [Mississippi State University (MSU)](https://www.gcerlab.com/lab-members).

## Contact
