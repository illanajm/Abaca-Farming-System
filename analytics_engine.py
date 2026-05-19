import numpy as np
import pandas as pd

# =========================
# DESCRIPTIVE STATISTICS
# =========================
def descriptive_stats(series):
    if series is None or series.empty:
        return None

    return {
        "mean": round(series.mean(), 2),
        "median": round(series.median(), 2),
        "mode": series.mode()[0] if not series.mode().empty else 0,
        "min": round(series.min(), 2),
        "max": round(series.max(), 2),
        "std": round(series.std(), 2),
        "var": round(series.var(), 2),
        "range": round(series.max() - series.min(), 2),
        "cv": round((series.std() / series.mean()) * 100, 2) if series.mean() != 0 else 0
    }


# =========================
# FREQUENCY TABLE
# =========================
def frequency_table(df, column):
    if df.empty or column not in df.columns:
        return None

    freq = df[column].value_counts().reset_index()
    freq.columns = [column, "Frequency"]

    freq["Percentage"] = round(
        (freq["Frequency"] / freq["Frequency"].sum()) * 100,
        2
    )

    freq["Cumulative %"] = freq["Percentage"].cumsum()

    return freq


# =========================
# CORRELATION ANALYSIS
# =========================
def correlation_analysis(df, col1, col2):
    if df.empty or col1 not in df.columns or col2 not in df.columns:
        return None

    return round(df[col1].corr(df[col2]), 4)


# =========================
# OUTLIER DETECTION (IQR METHOD)
# =========================
def detect_outliers(series):
    if series is None or series.empty:
        return None

    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = series[(series < lower) | (series > upper)]

    return {
        "outliers_count": len(outliers),
        "lower_bound": lower,
        "upper_bound": upper
    }


# =========================
# INSIGHT ENGINE
# =========================
def generate_insights(farm_stats, yield_stats, pest_count, corr_value):
    insights = []

    # Yield consistency
    if yield_stats["cv"] < 10:
        insights.append("Yield performance is highly consistent across farms.")
    elif yield_stats["cv"] < 30:
        insights.append("Yield performance shows moderate variability.")
    else:
        insights.append("Yield performance is highly unstable across farms.")

    # Correlation interpretation
    if corr_value is not None:
        if corr_value > 0.6:
            insights.append("Strong positive relationship between farm size and yield.")
        elif corr_value > 0.3:
            insights.append("Moderate relationship between farm size and yield.")
        else:
            insights.append("Weak relationship between farm size and yield.")

    # Pest warning
    if pest_count > 0:
        insights.append("Pest presence detected. Monitoring and control recommended.")

    return insights

# =========================
# 📈 YIELD PREDICTION MODEL (ML)
# =========================
def predict_yield(df):
    if df is None or len(df) < 2:
        return None

    df = df.dropna()

    X = df[["Farm Area"]]
    y = df["Yield"]

    model = LinearRegression()
    model.fit(X, y)

    df["Predicted Yield"] = model.predict(X)

    return df, model

# =========================
# 🧑‍🌾 FARMER PERFORMANCE RANKING
# =========================
def farmer_ranking(df):
    if df is None or df.empty:
        return None

    ranked = df.copy()
    ranked["Score"] = (ranked["Yield"] * 0.7) + (ranked["Farm Area"] * 0.3)
    ranked = ranked.sort_values("Score", ascending=False)
    return ranked

# =========================
# ⚠️ PEST RISK SCORE
# =========================
def pest_risk_score(pest_count, farm_count):
    if farm_count == 0:
        return 0

    return round((pest_count / farm_count) * 100, 2)