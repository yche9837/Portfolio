# Predicting Customer Wine Expenditure

*QBUS2820, University of Sydney, 2023 · High Distinction*

## Goal
Predict how much a customer spent on wine over the last two years, using a marketing dataset of 2,240 customers and 28 variables.

## Approach
- Cleaned the data, ran EDA (skewness, correlations, multicollinearity) and engineered features.
- Compared linear regression (with forward stepwise selection), KNN and random forest, tuning hyperparameters where possible.
- Selected the final model by MAE on held-out data.
- Checked the final model for fairness using statistical parity and disparate impact.
- Wrote up findings, limitations and recommendations in a report.

## Tools
Python · pandas · scikit-learn · seaborn · Jupyter

## Files
| File | Contents |
|---|---|
| `analysis.ipynb` | Main notebook |
| `ifood_marketing.csv` | Data |
| `report.pdf` | Final report |
| `images/` | Figures |
