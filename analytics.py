import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

def build_kpis(df, measure):
    total = df[measure].sum()
    mean = df[measure].mean()
    median = df[measure].median()
    records = len(df)
    return {
        f"Total {measure}": f"{total:,.2f}",
        f"Average {measure}": f"{mean:,.2f}",
        f"Median {measure}": f"{median:,.2f}",
        "Records": f"{records:,}",
    }

def monthly_trend(df, date_col, measure):
    temp = df[[date_col, measure]].copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
    temp = temp.dropna(subset=[date_col, measure])
    if temp.empty:
        return pd.DataFrame(columns=["period", measure])
    temp["period"] = temp[date_col].dt.to_period("M").dt.to_timestamp()
    return temp.groupby("period", as_index=False)[measure].sum().sort_values("period")

def forecast_series(trend, horizon, measure):
    hist = trend.copy().sort_values("period")
    x = np.arange(len(hist))
    y = hist[measure].astype(float).values
    slope, intercept = np.polyfit(x, y, 1)
    future_x = np.arange(len(hist), len(hist) + horizon)
    future_dates = pd.date_range(hist["period"].max() + pd.offsets.MonthBegin(1), periods=horizon, freq="MS")
    pred = slope * future_x + intercept
    return pd.DataFrame({"period": future_dates, measure: np.maximum(pred, 0)})

def detect_anomalies(df, numeric_cols, contamination=0.05):
    if len(df) < 10 or not numeric_cols:
        return pd.DataFrame()
    X = df[numeric_cols].replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median()).fillna(0)
    model = IsolationForest(contamination=contamination, random_state=42)
    labels = model.fit_predict(X)
    result = df.copy()
    result["is_anomaly"] = labels == -1
    return result

def scenario_analysis(df, measure, change_pct):
    baseline = float(df[measure].sum())
    projected = baseline * (1 + change_pct / 100)
    return baseline, projected, projected - baseline
