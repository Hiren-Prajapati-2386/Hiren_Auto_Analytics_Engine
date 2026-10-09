import streamlit as st
import pandas as pd
from data_loader import load_and_clean_data
from detectors import detect_trends, detect_outliers, detect_correlations
from plots import plot_severity_counts, plot_correlation_heatmap, plot_trend_line
import io
st.title("🏥 Auto-Analytics Healthcare Engine")

# 1. Load Data
try:
    df = load_and_clean_data("healthcare_data.csv")
except FileNotFoundError:
    st.error("Data file 'healthcare_data.csv' not found. Please ensure it is in the same directory.")
    st.stop()

with st.expander("🔍 Data Validation Overview", expanded=False):
    st.markdown("### 1. Data Preview (First 5 Rows)")
    st.dataframe(df.head(), use_container_width=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 2. Missing Values")
        st.dataframe(df.isnull().sum().reset_index().rename(columns={'index': 'Column', 0: 'Missing Count'}), use_container_width=True)
    
    with col_b:
        st.markdown("### 3. Data Info")
        # Capture df.info() output
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.code(buffer.getvalue(), language="text")
    
# 2. UI Filters & Thresholds
st.sidebar.markdown("## 🎛️ Filters & Thresholds")
st.sidebar.markdown("---")

st.sidebar.markdown("### 📍 Select Data")
districts = st.sidebar.multiselect("Districts", options=df['district'].unique(), default=df['district'].unique())

# Extract formatted months for filter
df['month_str'] = df['month'].dt.strftime('%Y-%m')
months = st.sidebar.multiselect("Select Months", options=df['month_str'].unique(), default=df['month_str'].unique())

indicators = ['anc_coverage', 'institutional_delivery', 'immunization', 'high_risk_cases']
selected_indicators = st.sidebar.multiselect("Indicators", options=indicators, default=indicators)

filtered_df = df[df['district'].isin(districts) & df['month_str'].isin(months)].copy()

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Thresholds")
trend_threshold = st.sidebar.slider("Trend Threshold (%)", min_value=1.0, max_value=50.0, value=10.0)
zscore_threshold = st.sidebar.slider("Outlier Z-Score", min_value=1.0, max_value=5.0, value=3.0)
corr_threshold = st.sidebar.slider("Correlation Threshold (|r|)", min_value=0.5, max_value=1.0, value=0.7)

# 3. Execute Analysis
raw_insights = []
raw_insights.extend(detect_trends(filtered_df, districts, selected_indicators, trend_threshold))
raw_insights.extend(detect_outliers(filtered_df, selected_indicators, zscore_threshold))

corr_insights, corr_matrix = detect_correlations(filtered_df, selected_indicators, corr_threshold)
raw_insights.extend(corr_insights)

# Assign auto-numbered Insight IDs
for idx, insight in enumerate(raw_insights, 1):
    insight['insight_id'] = f"INS-{idx:04d}"

# Reorder dictionary to put insight_id first
ordered_insights = [{k: v for k, v in insight.items()} for insight in raw_insights]
for i in range(len(ordered_insights)):
    ordered_insights[i] = {"insight_id": ordered_insights[i].pop("insight_id"), **ordered_insights[i]}

insights_df = pd.DataFrame(ordered_insights)

# 4. Display Results & Visualizations
st.subheader("Correlation Analysis")
st.warning("Note: With only 2 months x 6 districts, true correlation is fragile. Results may be unstable.")

st.subheader("💡 Automated Insights")
if not insights_df.empty:
    st.dataframe(insights_df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 Insight Severity Counts")
    st.plotly_chart(plot_severity_counts(insights_df), use_container_width=True)
        
    st.markdown("---")
    st.subheader("🌡️ Correlation Heatmap")
    if not corr_matrix.empty:
        st.plotly_chart(plot_correlation_heatmap(corr_matrix), use_container_width=True)
        
    st.markdown("---")
    st.subheader("📈 District Performance Trends")
    selected_trend_ind = st.selectbox("Select Indicator for Trend Line", selected_indicators)
    if selected_trend_ind:
        st.plotly_chart(plot_trend_line(filtered_df, selected_trend_ind), use_container_width=True)

    # Export Outputs
    insights_df.to_csv("insights_output.csv", index=False)
    corr_matrix.to_csv("correlation_matrix.csv")
    st.success("Outputs successfully saved to 'insights_output.csv' and 'correlation_matrix.csv'")
else:
    st.info("No insights found based on current thresholds.")