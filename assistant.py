def answer_question(question, df, measure, segment_col=None, date_col=None):
    q = question.lower()
    if segment_col and any(word in q for word in ["segment", "category", "region", "product", "highest", "top"]):
        grouped = df.groupby(segment_col, dropna=False)[measure].sum().sort_values(ascending=False)
        if grouped.empty:
            return "There is not enough segment data to answer that."
        name = grouped.index[0]
        share = grouped.iloc[0] / grouped.sum() * 100 if grouped.sum() else 0
        return f"{name} is the largest contributor, with {grouped.iloc[0]:,.2f} in {measure} ({share:.1f}% of the total)."
    if any(word in q for word in ["average", "mean"]):
        return f"The average {measure} per record is {df[measure].mean():,.2f}."
    if any(word in q for word in ["total", "revenue", "sales", "sum"]):
        return f"The total {measure} across {len(df):,} records is {df[measure].sum():,.2f}."
    if any(word in q for word in ["maximum", "highest", "largest", "best"]):
        idx = df[measure].idxmax()
        return f"The highest {measure} is {df.loc[idx, measure]:,.2f} (row index {idx})."
    if any(word in q for word in ["minimum", "lowest", "smallest", "worst"]):
        idx = df[measure].idxmin()
        return f"The lowest {measure} is {df.loc[idx, measure]:,.2f} (row index {idx})."
    return (f"I can currently answer questions about total, average, highest/lowest values"
            + (f", and performance by {segment_col}" if segment_col else "")
            + f". The selected measure is {measure}.")
