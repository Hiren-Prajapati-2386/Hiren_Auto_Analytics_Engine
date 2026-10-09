# Auto-Analytics Healthcare Engine

An automated insight generation engine that ingests small district-level healthcare performance datasets and identifies trends, outliers, and correlations to produce human-readable insights.

## Features

- **Data Validation**: Displays raw data, missing values, and DataFrame info.
- **Dynamic Filters**: Filter data by Districts, Months, and Indicators dynamically in the UI.
- **Configurable Thresholds**:
  - **Trend**: Flag significant percentage changes month-over-month.
  - **Outlier**: Flag statistical anomalies using Z-scores based on state means for a given month.
  - **Correlation**: Detect relationships between indicators using Pearson correlation matrices.
- **Automated Insights**: Generates structured, human-readable insights based on findings.
- **Visualizations**: Interactive charts for trends, insight severity distribution, and correlation heatmaps.

## Prerequisites

- Python 3.8+
- Required libraries are listed in `requirements.txt`.

## Setup & Execution

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

3. **Outputs**:
   - The web app will open automatically in your default browser.
   - The generated insights will be saved locally to `insights_output.csv`.
   - The correlation matrix will be saved locally to `correlation_matrix.csv`.

## Important Notes & Limitations

- **Fragile Correlations**: The provided sample dataset has only 2 months of data for 6 districts (12 rows). As per standard statistical rules, Pearson correlations on such a small sample size will be fragile/unstable. This limitation is noted within the UI.
- **State Mean calculation**: Outlier Z-scores are computed against the "State Mean" (the mean of all available districts) for that specific month, rather than across all months.
