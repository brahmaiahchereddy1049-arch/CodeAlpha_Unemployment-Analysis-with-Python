# Unemployment Analysis with Python

An exploratory data analysis project that studies unemployment trends in India using monthly unemployment-rate data, with special focus on the COVID-19 period in 2020.

## Project Objectives

- Clean and prepare unemployment data
- Explore unemployment rates across Indian states/regions
- Analyze unemployment trends over time
- Investigate changes around the COVID-19 period
- Examine regional differences
- Identify monthly/seasonal patterns
- Visualize unemployment, employment, and labour participation
- Produce data-driven observations that can inform economic and social discussions

> **Important:** This is an observational analysis. Changes during COVID-19 are described as associations in the data, not as proof that COVID-19 alone caused a particular change.

## Dataset

The project includes two CSV files from the uploaded dataset archive:

1. `data/unemployment_india.csv`
2. `data/unemployment_rate_upto_11_2020.csv`

The main analysis uses `unemployment_india.csv`, which contains state/region-level monthly observations and an `Area` field (Rural/Urban).

### Main columns

| Column | Description |
|---|---|
| `Region` | Indian state/region |
| `Date` | Observation date |
| `Frequency` | Data frequency |
| `Estimated Unemployment Rate (%)` | Estimated unemployment rate |
| `Estimated Employed` | Estimated number of employed people |
| `Estimated Labour Participation Rate (%)` | Estimated labour-force participation rate |
| `Area` | Rural or Urban |

## COVID-19 Analysis

The analysis uses:

- **Pre-COVID reference period:** May 2019 to February 2020 (based on the available main dataset)
- **COVID period:** March 2020 to June 2020 (the available COVID-period observations in the main dataset)

March 2020 is treated as the beginning of the COVID-affected period for the project because the dataset contains monthly observations and major nationwide COVID-related disruptions began around that time. The main file used here ends in June 2020, so the COVID comparison does not cover the entire year.

The script also calculates the national monthly average and the change between the pre-COVID reference average and the COVID-period average.

## Key Questions

1. How did unemployment change over time?
2. Which regions had higher or lower unemployment rates?
3. How did unemployment change around March-April-May 2020?
4. Did rural and urban unemployment behave differently?
5. Which months show higher/lower unemployment levels in the months available in the dataset?
6. How are employment and labour participation related to unemployment in this dataset?

## Project Structure

```text
unemployment_analysis_python/
│
├── data/
│   ├── unemployment_india.csv
│   └── unemployment_rate_upto_11_2020.csv
│
├── outputs/
│   ├── analysis_summary.txt
│   ├── monthly_national_summary.csv
│   ├── region_summary.csv
│   └── plots/
│       ├── monthly_unemployment_trend.png
│       ├── covid_impact.png
│       ├── regional_unemployment.png
│       ├── rural_urban_unemployment.png
│       ├── monthly_pattern.png
│       └── unemployment_vs_labour_participation.png
│
├── src/
│   └── unemployment_analysis.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/unemployment-analysis-python.git
cd unemployment-analysis-python
```

Create a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Analysis

```bash
python src/unemployment_analysis.py
```

The script generates CSV summaries, a text summary, and six plots in the `outputs/` directory.

## Visualizations

### 1. Monthly Unemployment Trend
Shows the overall monthly unemployment-rate movement and highlights the COVID period.

### 2. COVID-19 Impact
Compares the average unemployment rate before and during the COVID-affected period.

### 3. Regional Unemployment
Shows average unemployment rates by state/region.

### 4. Rural vs Urban
Compares average unemployment rates between rural and urban observations.

### 5. Monthly Pattern
Shows average unemployment by calendar month, which can reveal recurring monthly patterns.

### 6. Unemployment vs Labour Participation
Explores the relationship between unemployment rate and labour-force participation rate.

## Key Findings

Run the project to generate exact values in:

```text
outputs/analysis_summary.txt
outputs/monthly_national_summary.csv
outputs/region_summary.csv
```

The analysis is designed to report findings such as:

- Peak unemployment months in the available period
- Regional differences
- Pre-COVID versus COVID-period changes
- Rural/urban differences
- Monthly patterns
- Relationship between unemployment and labour participation

The numerical findings should be interpreted within the coverage and definitions of the supplied dataset.

## Policy-Relevant Interpretation

The results can help frame questions for economic and social policy, including:

- employment-support programs during economic shocks
- targeted support for regions with persistently high unemployment
- rural and urban employment interventions
- labour-market monitoring during crises
- skills and re-employment programs
- timely employment data collection

These are areas for policy consideration rather than recommendations derived solely from this dataset.

## Limitations

- The dataset covers a limited historical period.
- COVID-19 is a major event during the period, but the analysis does not establish causality.
- State-level estimates may not capture all labour-market differences.
- Monthly averages can hide short-term variation.
- The dataset's measurement methodology should be checked against the original source before using the analysis for formal policy decisions.
- The calendar-month analysis is not a full seasonal study because the available main dataset does not contain a complete set of years for every month.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Skills Demonstrated

- Data cleaning
- Date/time processing
- Exploratory data analysis
- GroupBy aggregation
- Feature creation
- Comparative analysis
- COVID-period analysis
- Trend analysis
- Data visualization
- Interpretation of real-world economic data

## Author

**Brahmaiah Chereddy**

Data Analyst / Python Data Analysis Project

GitHub: `https://github.com/brahmaiahchereddy1049-arch`

LinkedIn: `https://www.linkedin.com/in/brahmaiah-chereddy-5b0050346/`

## License

This repository is intended for educational and portfolio use. Verify the original dataset's source and license before redistributing the raw data.
