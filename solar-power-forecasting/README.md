# Forecasting Household Solar Power Production

*QBUS2820, University of Sydney, 2023 · High Distinction*

## Goal
Forecast household solar production at three time scales: the next 24 hours (half-hourly), the next 7 days (daily) and the next 12 months (monthly).

## Approach
- Converted half-hourly readings to a period index and aggregated them to daily and monthly series.
- Split the data into training, validation and test sets in time order.
- Ran EDA on trend and seasonality using time plots, decomposition, and ACF/PACF plots.
- Compared random walk, seasonal random walk, Holt-Winters (additive and multiplicative), damped Holt and ARIMA, selecting models by validation MAE.
- Ran residual diagnostics on the chosen models and discussed their limits. For example, some residual autocorrelation remained at lags 1–3.

## Tools
Python · pandas · statsmodels · matplotlib · Jupyter

## Files
| File | Contents |
|---|---|
| `analysis.ipynb` | Main notebook |
| `auxiliary.ipynb` | Supporting analysis |
| `forecast.py` | Helper functions |
| `solar_halfhour.csv` | Data |
| `report.pdf` | Final report |
