# Hotel Booking Cancellation Prediction

*COMP5310, University of Sydney, 2026 · pair assignment · mark 19.22/20*

We predict whether a confirmed hotel booking will be cancelled or end in a no-show, so a hotel revenue manager can place at-risk bookings on a pre-arrival follow-up list.

**My role:** I built the data pipeline (`01`) and set up and ran the modelling notebook (`02`): the missing-value analysis with chi-squared tests, cleaning and feature engineering, the data dictionary, the train/test split and cross-validation, the leakage checks, model tuning, threshold selection, the final evaluation, error analysis and the time-based check. My teammate led the report writing and revised the feature-selection step so it is refitted inside every cross-validation fold.

| File | Contents |
|---|---|
| [`01_data_pipeline.ipynb`](01_data_pipeline.ipynb) | Missing-value analysis, cleaning, feature engineering, data dictionary |
| [`02_modelling_evaluation.ipynb`](02_modelling_evaluation.ipynb) | Split, cross-validation, baselines, models, evaluation, error analysis |
| [`report.pdf`](report.pdf) | Decision report for the hotel revenue manager |

Both notebooks are saved with their outputs, so every table and figure can be read on GitHub without running anything.

## Results

Two baselines and two candidate models were compared on the same 10 cross-validation folds. The final model was chosen by cross-validated F1 for the cancellation class and evaluated once on the held-out test set (17,423 bookings).

| Model | CV F1 | Test F1 | Test recall | Test precision |
|---|---|---|---|---|
| Majority class (baseline) | 0.000 | 0.000 | 0.000 | 0.000 |
| One-rule tree (baseline) | 0.486 | 0.490 | 0.932 | 0.332 |
| Logistic regression | 0.587 | 0.598 | 0.678 | 0.535 |
| **Random forest (final)** | **0.663** | **0.672** | **0.751** | **0.609** |

The recommendation was to pilot the random forest as a decision-support tool for staff follow-up, never for automatic action on reservations. The model misses most short-notice cancellations, and its F1 fell to 0.600 when trained on earlier arrivals and tested on 2017, so it needs subgroup monitoring and regular retraining.

## Method

**Data pipeline (`01`).** Only steps that do not learn from the data, so the output is safe to use before the split:

* missing values handled column by column, with chi-squared tests deciding whether missingness is linked to cancellation
* duplicates and invalid records removed, and bookings with no recorded adult excluded as a scope restriction
* columns that reveal the outcome removed (`reservation_status`, `assigned_room_type`, `booking_changes` and others)
* new features: `booked_via_agent`, `booked_via_company` and `country_group`
* result: 87,114 bookings and 30 columns, from 119,987 raw bookings

**Modelling and evaluation (`02`).**

* stratified 80/20 train/test split and 10-fold stratified cross-validation, defined before any EDA or fitting
* EDA on the training set only, used to fix the primary metric (F1 for the cancellation class)
* one scikit-learn `Pipeline` refitted in every fold: one-hot encoding and scaling, PCA-loading column selection (27 of 64 encoded columns), optional L1 selection, then the classifier
* logistic regression and random forest tuned with `GridSearchCV`, compared with paired t-tests across folds
* decision threshold chosen from out-of-fold training predictions, then one evaluation on the test set
* error analysis by booking group, model interpretation and a time-based robustness check

Random seed `5310` is used for the split, the folds and all models. Tested with Python 3.14 and scikit-learn 1.9.

## Data

Hotel booking demand data for a city hotel and a resort hotel, with arrivals from 2015 to 2017, as provided by the course. The data files are not included in this repository. To re-run the notebooks, place the course's `hotel_bookings.csv` in a `data/` folder here. Notebook `01` writes `data/hotel_bookings_cleaned.csv`, and `02` writes its tables and figures to `outputs/`. The original public dataset is described in:

> Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. *Data in Brief, 22*, 41–49. https://doi.org/10.1016/j.dib.2018.11.126

The course version differs slightly from the public release (119,987 rows), so counts may not match exactly if you use the public file.
