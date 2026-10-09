import plotly.express as px

def plot_severity_counts(insights_df):
    severity_counts = insights_df['severity'].value_counts().reset_index()
    severity_counts.columns = ['Severity', 'Count']
    return px.bar(severity_counts, x='Severity', y='Count', color='Severity')

def plot_correlation_heatmap(corr_matrix):
    return px.imshow(corr_matrix, text_auto=True, aspect="auto")

def plot_trend_line(df, indicator):
    return px.line(df, x='month', y=indicator, color='district', markers=True)