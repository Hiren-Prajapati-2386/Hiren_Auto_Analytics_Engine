<div align="center">
  <h1>🏥 Auto-Analytics Healthcare Engine</h1>
  <p><i>An automated, premium insight generation engine that ingests district-level healthcare data to instantly identify trends, statistical outliers, and complex correlations.</i></p>
  
  <h3>🌍 <a href="https://hirenautoanalyticsengine-m2unhsckfwq4iciwu3zfwr.streamlit.app/">View Live Deployment Here</a></h3>
</div>

---

## 📸 Application Screenshots
*Click on the images to view them in full resolution.*

| Executive Insights Dashboard | Visual Analytics & Heatmaps |
|:---:|:---:|
| <img src="Screenshots/Screenshot%202026-10-09%20152708.png" width="400"> | <img src="Screenshots/Screenshot%202026-10-09%20152723.png" width="400"> |
| **Performance Trend Analysis** | **Data Validation & Previews** |
| <img src="Screenshots/Screenshot%202026-10-09%20152751.png" width="400"> | <img src="Screenshots/Screenshot%202026-10-09%20152815.png" width="400"> |

---

## 🏗️ Modular Architecture

This project is built using professional software engineering principles. Instead of a single monolithic script, the codebase is modular, making it scalable and easy to maintain by a team.

- 📁 **`app.py`** 
  - **Purpose**: The main Streamlit entry point. It controls the UI layout, state management, and tabbed dashboard logic.
- 📁 **`data_loader.py`** 
  - **Purpose**: Handles ingestion and cleaning. It uses `@st.cache_data` to ensure the dataset is only loaded into memory once for high performance.
- 📁 **`detectors.py`** 
  - **Purpose**: The mathematical core. Contains isolated algorithms for computing Month-over-Month (MoM) percentage change trends, grouping data to compute monthly State Means for accurate Z-Score outlier detection, and generating Pearson correlation matrices.
- 📁 **`plots.py`** 
  - **Purpose**: Visualization logic. Isolates all `plotly` graphing configurations (colors, layouts, legends) away from the main application state.
- 📁 **`main.py`** (Test Data Generator)
  - **Purpose**: A synthetic data generator built to stress-test the analytics engine. It creates 500 rows of complex district data with intentionally injected anomalies (sudden spikes and downward trends) to mathematically prove the detectors work at scale.

## 🚀 Setup & Execution

1. **Install Dependencies**:
   Ensure you have Python 3.8+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Test Data (Optional but Recommended)**:
   You can run the synthetic data generator to stress-test the application with 500 rows.
   ```bash
   python main.py
   ```

3. **Launch the Engine**:
   Start the interactive web dashboard. It will open automatically in your default browser.
   ```bash
   streamlit run app.py
   ```

## ✨ Key Features & Limitations

- **Dynamic Widescreen UI**: Custom HTML/CSS styling, KPI Metric cards, and tabbed navigation.
- **Statistical Accuracy**: Outliers are calculated against individual monthly state means to account for seasonal variations in healthcare, rather than standard global means.
- **Fragile Correlations**: The engine actively warns users when datasets are too small to provide mathematically sound Pearson correlations, demonstrating statistical rigor.
- **Automated Reporting**: Generates a completely autonomous `insights_output.csv` mimicking a human data analyst's findings.
