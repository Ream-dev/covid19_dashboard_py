# 🦠 COVID-19 Global Dashboard

A comprehensive Dash application for tracking global COVID-19 statistics including cases, deaths, recoveries, vaccination progress, and regional breakdowns. Features a special spotlight section on Cambodia.

## Features

- **Global Summary Metrics**: Total cases, deaths, recoveries, active cases, and vaccination data
- **Monthly Case Trends**: 2020–2023 visualization of global confirmed cases
- **Wave Analysis**: Quarterly breakdown of major pandemic waves
- **Vaccination Progress**: Regional vaccination rates comparison
- **Case Fatality Rate by Age**: Log-scale visualization showing CFR across age groups
- **Variant Tracking**: Stacked bar chart showing variant prevalence over time
- **Cambodia Spotlight**: Country-specific metrics, case trends, vaccination rollout, and provincial breakdown

## Requirements

- Python 3.7+
- dash
- plotly
- pandas
- numpy

## Installation

```bash
pip install dash plotly pandas numpy
```

## Running

```bash
python covid19_dashboard.py
```

Open your browser at: http://127.0.0.1:8050

## Data Sources

- WHO (World Health Organization)
- Johns Hopkins CSSE
- Our World in Data

> ⚡ Data reflects cumulative statistics as of early 2024  
> Made with ❤️ by Ream