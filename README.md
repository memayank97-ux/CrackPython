# AI-Powered Business Intelligence & Decision Engine

A portfolio-ready starter application for exploring business data, monitoring KPIs, forecasting trends, flagging unusual observations and running simple what-if scenarios.

## Features

- Upload CSV and Excel datasets
- Automatic numeric-column detection and basic data cleaning
- KPI summary: total, average, median and record count
- Monthly trend analysis and baseline linear forecast
- Multivariate anomaly detection using Isolation Forest
- Scenario sensitivity analysis
- Dataset-aware rule-based business Q&A
- Download cleaned data

## Quick start

Requires Python 3.10 or newer.

```bash
git clone https://github.com/YOUR_USERNAME/ai-business-intelligence-engine.git
cd ai-business-intelligence-engine

python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\\Scripts\\activate

pip install -r requirements.txt
streamlit run app.py
```

The app starts with a sample sales dataset. Upload your own CSV or Excel file from the sidebar.

## Expected data

The app works best with a tabular dataset containing:
- At least one numeric measure (e.g. revenue, cost, units, margin)
- Optionally, a date column
- Optionally, categorical dimensions (e.g. region, product, customer segment)

The primary measure and date/segment columns can be selected in the sidebar.

## Architecture

```text
Upload → Data ingestion → Cleaning/validation → Analytics
                                      ├── KPI engine
                                      ├── Trend + forecast
                                      ├── Anomaly detection
                                      ├── Scenario analysis
                                      └── Business Q&A
                                               ↓
                                         Streamlit UI
```

## Important limitations

This is a functional MVP, not an autonomous decision-maker:
- Forecasting uses a simple linear trend and does not model seasonality.
- Scenario analysis applies a percentage change directly to the selected measure; it does not estimate causal effects.
- Anomaly detection highlights unusual rows, not necessarily incorrect or harmful records.
- The business assistant uses transparent rule-based responses. It does not yet call an LLM or retrieve external company knowledge.
- Validate data quality, model assumptions and recommendations before using outputs for financial or operational decisions.

## Suggested next development milestones

1. Add unit tests and data-quality profiling.
2. Add a proper forecasting model with backtesting and confidence intervals.
3. Add an LLM-powered assistant with retrieval over company documentation.
4. Add user authentication, role-based access and audit logging.
5. Add a database layer and scheduled data refresh.
6. Add Docker deployment and CI checks with GitHub Actions.

## License

MIT
