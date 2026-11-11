import pandas as pd
from pathlib import Path

def load_data(source):
    name = getattr(source, "name", str(source)).lower()
    if name.endswith(".xlsx") or name.endswith(".xls"):
        return pd.read_excel(source)
    return pd.read_csv(source)

def prepare_data(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(how="all")
    for col in df.columns:
        if df[col].dtype == "object":
            cleaned = df[col].astype(str).str.replace(",", "", regex=False).str.strip()
            numeric = pd.to_numeric(cleaned, errors="coerce")
            if numeric.notna().mean() > 0.85:
                df[col] = numeric
    return df

def detect_date_column(df):
    for col in df.columns:
        if "date" in str(col).lower() or "time" in str(col).lower():
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().mean() > 0.6:
                return col
    for col in df.select_dtypes(include=["object"]).columns:
        parsed = pd.to_datetime(df[col], errors="coerce")
        if parsed.notna().mean() > 0.8:
            return col
    return None

def detect_numeric_columns(df):
    return list(df.select_dtypes(include="number").columns)
