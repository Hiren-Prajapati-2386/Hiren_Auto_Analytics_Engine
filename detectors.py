import pandas as pd
import numpy as np

def get_severity(val, threshold):
    ratio = abs(val) / threshold
    if ratio >= 2.0: return "High"
    elif ratio >= 1.5: return "Medium"
    return "Low"

def detect_trends(df, districts, indicators, threshold):
    insights = []
    df_sorted = df.sort_values(by=['district', 'month'])
    
    for dist in districts:
        dist_data = df_sorted[df_sorted['district'] == dist].copy()
        for ind in indicators:
            dist_data[f'{ind}_pct_change'] = dist_data[ind].pct_change() * 100
            
            for _, row in dist_data.dropna(subset=[f'{ind}_pct_change']).iterrows():
                pct = row[f'{ind}_pct_change']
                if abs(pct) >= threshold:
                    insights.append({
                        "type": "trend",
                        "indicator": ind,
                        "entity": dist,
                        "period": row['month'].strftime('%Y-%m'),
                        "value": row[ind],
                        "prev_value": round(row[ind] / (1 + (pct/100)), 2),
                        "change_pct": round(pct, 2),
                        "severity": get_severity(pct, threshold),
                        "explanation": f"{ind} in {dist} changed by {pct:.1f}% compared to the previous month, exceeding the {threshold}% threshold."
                    })
    return insights

def detect_outliers(df, indicators, threshold):
    insights = []
    # Group by month to calculate the state mean for that specific month
    for ind in indicators:
        for month_val, month_df in df.groupby('month'):
            if len(month_df) > 1:
                mean_val = month_df[ind].mean()
                std_val = month_df[ind].std()
                
                if std_val > 0:
                    zscores = (month_df[ind] - mean_val) / std_val
                    outliers = month_df[abs(zscores) >= threshold]
                    
                    for idx, row in outliers.iterrows():
                        z_val = zscores.loc[idx]
                        insights.append({
                            "type": "outlier",
                            "indicator": ind,
                            "entity": row['district'],
                            "period": row['month'].strftime('%Y-%m'),
                            "value": row[ind],
                            "prev_value": round(mean_val, 2), 
                            "change_pct": None,
                            "severity": get_severity(z_val, threshold),
                            "explanation": f"{row['district']}'s {ind} of {row[ind]} is an extreme outlier (Z-Score: {z_val:.2f}) against the state mean of {mean_val:.1f} for {row['month'].strftime('%b %Y')}."
                        })
    return insights

def detect_correlations(df, indicators, threshold):
    insights = []
    if len(indicators) < 2:
        return insights, pd.DataFrame()
        
    corr_matrix = df[indicators].corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            r_val = corr_matrix.iloc[i, j]
            if abs(r_val) >= threshold:
                ind1, ind2 = corr_matrix.columns[i], corr_matrix.columns[j]
                insights.append({
                    "type": "correlation",
                    "indicator": f"{ind1}:{ind2}",
                    "entity": "All Selected",
                    "period": "Overall",
                    "value": round(r_val, 2),
                    "prev_value": None,
                    "change_pct": None,
                    "severity": "Medium",
                    "explanation": f"Strong correlation ({r_val:.2f}) detected between {ind1} and {ind2}."
                })
    return insights, corr_matrix