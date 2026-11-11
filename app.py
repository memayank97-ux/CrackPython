import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from src.data import load_data, prepare_data, detect_date_column, detect_numeric_columns
from src.analytics import build_kpis, monthly_trend, forecast_series, detect_anomalies, scenario_analysis
from src.assistant import answer_question

st.set_page_config(page_title="AI Business Intelligence Engine", page_icon="📊", layout="wide")
st.title("📊 AI-Powered Business Intelligence & Decision Engine")
st.caption("Upload business data, explore performance, forecast trends and test strategic scenarios.")

with st.sidebar:
    st.header("Data")
    uploaded = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    st.markdown("---")
    st.subheader("Demo mode")
    use_demo = st.checkbox("Use sample sales dataset", value=uploaded is None)

if uploaded is not None:
    try:
        raw = load_data(uploaded)
    except Exception as exc:
        st.error(f"Could not read file: {exc}")
        st.stop()
elif use_demo:
    raw = load_data(Path("data/sample_sales.csv"))
else:
    st.info("Upload a CSV/Excel file or enable demo mode in the sidebar.")
    st.stop()

df = prepare_data(raw)
if df.empty:
    st.error("The dataset is empty.")
    st.stop()

date_col = detect_date_column(df)
numeric_cols = detect_numeric_columns(df)
if not numeric_cols:
    st.warning("No numeric columns found. Add numeric business measures such as revenue, cost, units or profit.")
    st.dataframe(df.head(20), use_container_width=True)
    st.stop()

with st.sidebar:
    st.subheader("Analysis settings")
    measure = st.selectbox("Primary measure", numeric_cols, index=0)
    date_options = ["(No date column)"] + list(df.columns)
    selected_date = st.selectbox("Date column", date_options, index=(date_options.index(date_col) if date_col in date_options else 0))
    date_col = None if selected_date == "(No date column)" else selected_date
    segment_options = [c for c in df.columns if c != measure and c != date_col]
    segment_col = st.selectbox("Segment (optional)", ["(None)"] + segment_options)
    segment_col = None if segment_col == "(None)" else segment_col

kpis = build_kpis(df, measure)
cols = st.columns(4)
for col, (label, value) in zip(cols, kpis.items()):
    col.metric(label, value)

st.markdown("---")
tab_overview, tab_forecast, tab_anomalies, tab_scenarios, tab_assistant, tab_data = st.tabs(
    ["Overview", "Forecast", "Anomalies", "Scenario planner", "Business assistant", "Data"]
)

with tab_overview:
    left, right = st.columns([2, 1])
    if date_col:
        trend = monthly_trend(df, date_col, measure)
        if not trend.empty:
            with left:
                st.subheader(f"{measure} over time")
                st.plotly_chart(px.line(trend, x="period", y=measure, markers=True), use_container_width=True)
        else:
            st.info("Not enough valid date values to create a time trend.")
    if segment_col:
        segment = df.groupby(segment_col, dropna=False)[measure].sum().reset_index().sort_values(measure, ascending=False).head(15)
        with right:
            st.subheader(f"{measure} by {segment_col}")
            st.plotly_chart(px.bar(segment, x=segment_col, y=measure), use_container_width=True)
    st.subheader("Key observations")
    st.write(f"- Dataset contains **{len(df):,} rows** and **{len(df.columns)} columns**.")
    st.write(f"- Total **{measure}** is **{df[measure].sum():,.2f}**.")
    st.write(f"- Average **{measure}** per record is **{df[measure].mean():,.2f}**.")
    if segment_col:
        top = df.groupby(segment_col)[measure].sum().idxmax()
        st.write(f"- Highest contributing **{segment_col}**: **{top}**.")

with tab_forecast:
    st.subheader("Forecast the primary measure")
    if not date_col:
        st.info("Select a date column in the sidebar to enable forecasting.")
    else:
        trend = monthly_trend(df, date_col, measure)
        horizon = st.slider("Forecast horizon (months)", 1, 12, 3)
        if len(trend) < 3:
            st.warning("At least three monthly observations are recommended.")
        else:
            forecast = forecast_series(trend, horizon, measure)
            combined = pd.concat([
                trend[["period", measure]].assign(type="Historical"),
                forecast[["period", measure]].assign(type="Forecast")
            ])
            st.plotly_chart(px.line(combined, x="period", y=measure, color="type", markers=True,
                                    title=f"{measure}: historical trend and baseline forecast"), use_container_width=True)
            st.dataframe(forecast, use_container_width=True)
            st.caption("Baseline linear-trend forecast for demonstration; validate with seasonality-aware models before business use.")

with tab_anomalies:
    st.subheader("Unusual observations")
    contamination = st.slider("Expected anomaly share", 0.01, 0.20, 0.05, 0.01)
    anomalies = detect_anomalies(df, numeric_cols, contamination)
    if anomalies.empty:
        st.info("Not enough numeric data to detect anomalies.")
    else:
        st.metric("Potential anomalies", int(anomalies["is_anomaly"].sum()))
        st.dataframe(anomalies[anomalies["is_anomaly"]].head(100), use_container_width=True)
        st.caption("Isolation Forest flags unusual multivariate records. An anomaly is not necessarily an error or a negative outcome.")

with tab_scenarios:
    st.subheader("What-if scenario")
    st.write("Estimate the direct effect of changing the selected measure. This is a sensitivity calculation, not a causal forecast.")
    change = st.slider("Assumed change in measure (%)", -50, 100, 10)
    baseline, projected, delta = scenario_analysis(df, measure, change)
    c1, c2, c3 = st.columns(3)
    c1.metric("Baseline total", f"{baseline:,.2f}")
    c2.metric("Scenario total", f"{projected:,.2f}")
    c3.metric("Change", f"{delta:+,.2f}", f"{change:+}%")

with tab_assistant:
    st.subheader("Ask the business assistant")
    st.caption("Answers are generated from the currently loaded dataset using transparent, rule-based analysis. Connect an LLM provider to enable richer natural-language reasoning.")
    question = st.text_input("Ask a question", placeholder="Which segment contributes the most?")
    if st.button("Analyse", type="primary") and question.strip():
        st.write(answer_question(question, df, measure, segment_col, date_col))

with tab_data:
    st.subheader("Dataset preview")
    st.write(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    st.dataframe(df.head(500), use_container_width=True)
    st.download_button("Download cleaned dataset", df.to_csv(index=False).encode("utf-8"), "cleaned_data.csv", "text/csv")
