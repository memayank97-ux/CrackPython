import pandas as pd
from src.analytics import scenario_analysis, monthly_trend

def test_scenario_analysis():
    df = pd.DataFrame({"revenue": [100, 200]})
    baseline, projected, delta = scenario_analysis(df, "revenue", 10)
    assert baseline == 300
    assert projected == 330
    assert delta == 30

def test_monthly_trend():
    df = pd.DataFrame({
        "date": ["2025-01-01", "2025-01-20", "2025-02-01"],
        "sales": [10, 20, 30]
    })
    result = monthly_trend(df, "date", "sales")
    assert len(result) == 2
    assert result["sales"].tolist() == [30, 30]
