"""
Unemployment Analysis with Python

Run from the project root:
    python src/unemployment_analysis.py
"""

from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "unemployment_india.csv"
OUTPUT_DIR = ROOT / "outputs"
PLOT_DIR = OUTPUT_DIR / "plots"

OUTPUT_DIR.mkdir(exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)

RATE_COL = "Estimated Unemployment Rate (%)"
EMPLOYED_COL = "Estimated Employed"
PARTICIPATION_COL = "Estimated Labour Participation Rate (%)"


def load_and_clean():
    df = pd.read_csv(DATA_PATH)

    # Strip accidental whitespace from column names and text fields.
    df.columns = df.columns.str.strip()

    for col in ["Region", "Frequency", "Area"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Convert date and numeric fields.
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

    for col in [RATE_COL, EMPLOYED_COL, PARTICIPATION_COL]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Date", RATE_COL, "Region"]).copy()
    df = df.drop_duplicates()

    # Time features.
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%b")

    # COVID period indicator.
    df["COVID_Period"] = np.where(
        df["Date"] >= pd.Timestamp("2020-03-01"),
        "COVID period",
        "Pre-COVID reference",
    )

    return df


def save_monthly_summary(df):
    monthly = (
        df.groupby("Date", as_index=False)
        .agg(
            Average_Unemployment_Rate=(RATE_COL, "mean"),
            Average_Employed=(EMPLOYED_COL, "mean"),
            Average_Labour_Participation=(PARTICIPATION_COL, "mean"),
        )
        .sort_values("Date")
    )

    monthly.to_csv(OUTPUT_DIR / "monthly_national_summary.csv", index=False)
    return monthly


def save_region_summary(df):
    region = (
        df.groupby("Region", as_index=False)
        .agg(
            Average_Unemployment_Rate=(RATE_COL, "mean"),
            Average_Employed=(EMPLOYED_COL, "mean"),
            Average_Labour_Participation=(PARTICIPATION_COL, "mean"),
            Observations=(RATE_COL, "count"),
        )
        .sort_values("Average_Unemployment_Rate", ascending=False)
    )

    region.to_csv(OUTPUT_DIR / "region_summary.csv", index=False)
    return region


def plot_monthly_trend(monthly):
    plt.figure(figsize=(11, 6))
    plt.plot(
        monthly["Date"],
        monthly["Average_Unemployment_Rate"],
        marker="o",
        linewidth=2,
    )
    plt.axvline(
        pd.Timestamp("2020-03-01"),
        linestyle="--",
        label="COVID period begins",
    )
    plt.xlabel("Date")
    plt.ylabel("Average Unemployment Rate (%)")
    plt.title("Monthly Unemployment Rate Trend in India")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "monthly_unemployment_trend.png", dpi=160)
    plt.close()


def plot_covid_impact(df):
    period = (
        df.groupby("COVID_Period", as_index=False)[RATE_COL]
        .mean()
        .rename(columns={RATE_COL: "Average_Unemployment_Rate"})
    )

    # Keep a meaningful display order.
    order = ["Pre-COVID reference", "COVID period"]
    period["COVID_Period"] = pd.Categorical(
        period["COVID_Period"], categories=order, ordered=True
    )
    period = period.sort_values("COVID_Period")

    plt.figure(figsize=(8, 6))
    plt.bar(
        period["COVID_Period"].astype(str),
        period["Average_Unemployment_Rate"],
    )
    plt.xlabel("")
    plt.ylabel("Average Unemployment Rate (%)")
    plt.title("Unemployment Before and During COVID-19 Period")
    plt.xticks(rotation=10)
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "covid_impact.png", dpi=160)
    plt.close()

    return period


def plot_regional_unemployment(region):
    top = region.head(15)

    plt.figure(figsize=(10, 7))
    plt.barh(
        top["Region"],
        top["Average_Unemployment_Rate"],
    )
    plt.gca().invert_yaxis()
    plt.xlabel("Average Unemployment Rate (%)")
    plt.ylabel("Region")
    plt.title("Regions with Higher Average Unemployment Rates")
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "regional_unemployment.png", dpi=160)
    plt.close()


def plot_rural_urban(df):
    if "Area" not in df.columns:
        return None

    area = (
        df.groupby("Area", as_index=False)[RATE_COL]
        .mean()
        .rename(columns={RATE_COL: "Average_Unemployment_Rate"})
    )

    plt.figure(figsize=(8, 6))
    plt.bar(
        area["Area"].astype(str),
        area["Average_Unemployment_Rate"],
    )
    plt.xlabel("")
    plt.ylabel("Average Unemployment Rate (%)")
    plt.title("Average Unemployment Rate: Rural vs Urban")
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "rural_urban_unemployment.png", dpi=160)
    plt.close()

    return area


def plot_monthly_pattern(df):
    monthly_pattern = (
        df.groupby(["Month", "Month_Name"], as_index=False)[RATE_COL]
        .mean()
        .sort_values("Month")
    )

    plt.figure(figsize=(10, 6))
    plt.bar(
        monthly_pattern["Month_Name"].astype(str),
        monthly_pattern[RATE_COL],
    )
    plt.xlabel("Month")
    plt.ylabel("Average Unemployment Rate (%)")
    plt.title("Average Unemployment by Calendar Month")
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "monthly_pattern.png", dpi=160)
    plt.close()

    return monthly_pattern


def plot_relationship(df):
    sample = df.dropna(
        subset=[RATE_COL, PARTICIPATION_COL]
    )

    plt.figure(figsize=(9, 6))
    for label, group in sample.groupby("COVID_Period"):
        plt.scatter(
            group[PARTICIPATION_COL],
            group[RATE_COL],
            alpha=0.6,
            label=label,
        )
    plt.legend()
    plt.xlabel("Labour Participation Rate (%)")
    plt.ylabel("Unemployment Rate (%)")
    plt.title("Unemployment vs Labour Participation")
    plt.tight_layout()
    plt.savefig(
        PLOT_DIR / "unemployment_vs_labour_participation.png",
        dpi=160,
    )
    plt.close()


def create_summary(df, monthly, region, period, area, monthly_pattern):
    peak_month = monthly.loc[
        monthly["Average_Unemployment_Rate"].idxmax()
    ]
    low_month = monthly.loc[
        monthly["Average_Unemployment_Rate"].idxmin()
    ]

    pre = period[
        period["COVID_Period"] == "Pre-COVID reference"
    ]["Average_Unemployment_Rate"]
    covid = period[
        period["COVID_Period"] == "COVID period"
    ]["Average_Unemployment_Rate"]

    pre_value = float(pre.iloc[0]) if len(pre) else float("nan")
    covid_value = float(covid.iloc[0]) if len(covid) else float("nan")
    change = covid_value - pre_value

    highest_region = region.iloc[0]
    lowest_region = region.iloc[-1]

    lines = [
        "UNEMPLOYMENT ANALYSIS SUMMARY",
        "=" * 60,
        f"Rows analyzed: {len(df):,}",
        f"Regions: {df['Region'].nunique()}",
        f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}",
        "",
        "COVID PERIOD COMPARISON",
        "-" * 60,
        f"Pre-COVID reference average: {pre_value:.2f}%",
        f"COVID-period average: {covid_value:.2f}%",
        f"Difference (COVID - pre-COVID): {change:+.2f} percentage points",
        "",
        "MONTHLY EXTREMES",
        "-" * 60,
        (
            f"Highest average month: {peak_month['Date'].strftime('%Y-%m')} "
            f"({peak_month['Average_Unemployment_Rate']:.2f}%)"
        ),
        (
            f"Lowest average month: {low_month['Date'].strftime('%Y-%m')} "
            f"({low_month['Average_Unemployment_Rate']:.2f}%)"
        ),
        "",
        "REGIONAL DIFFERENCES",
        "-" * 60,
        (
            f"Highest average region in this dataset: {highest_region['Region']} "
            f"({highest_region['Average_Unemployment_Rate']:.2f}%)"
        ),
        (
            f"Lowest average region in this dataset: {lowest_region['Region']} "
            f"({lowest_region['Average_Unemployment_Rate']:.2f}%)"
        ),
        "",
        "MONTHLY PATTERN",
        "-" * 60,
        (
            f"Highest average calendar month: "
            f"{monthly_pattern.iloc[monthly_pattern[RATE_COL].idxmax()]['Month_Name']}"
        ),
        (
            f"Lowest average calendar month: "
            f"{monthly_pattern.iloc[monthly_pattern[RATE_COL].idxmin()]['Month_Name']}"
        ),
        "",
        "INTERPRETATION NOTE",
        "-" * 60,
        "The COVID comparison is descriptive and does not establish causality.",
        "Regional and monthly differences may reflect many economic and measurement factors.",
    ]

    if area is not None and len(area):
        lines.extend(
            [
                "",
                "RURAL / URBAN",
                "-" * 60,
                area.to_string(index=False),
            ]
        )

    (OUTPUT_DIR / "analysis_summary.txt").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main():
    df = load_and_clean()

    monthly = save_monthly_summary(df)
    region = save_region_summary(df)
    period = plot_covid_impact(df)
    area = plot_rural_urban(df)
    monthly_pattern = plot_monthly_pattern(df)

    plot_monthly_trend(monthly)
    plot_regional_unemployment(region)
    plot_relationship(df)

    create_summary(
        df,
        monthly,
        region,
        period,
        area,
        monthly_pattern,
    )

    print("=" * 60)
    print("Unemployment Analysis Completed")
    print("=" * 60)
    print(f"Rows analyzed: {len(df):,}")
    print(f"Regions: {df['Region'].nunique()}")
    print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(f"Outputs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
