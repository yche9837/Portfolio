# Fiona (Yi Fei) Chen — Data Science Portfolio

Master of Data Science student at the University of Sydney, with a Bachelor of Advanced Computing (Data Science) and Bachelor of Commerce (Business Analytics). I build reproducible data pipelines and models, and I write up the results for the people who have to act on them.

**Skills:** Python (pandas, scikit-learn, statsmodels) · SQL (PostgreSQL, PostGIS) · R · Java · AWS (Certified Cloud Practitioner) · Git · Jira

fionachen0811@gmail.com · [Portfolio site](https://yche9837.github.io/fiona-ds-ba.github.io/)

---

## Featured projects

| Project | What it shows | Tools | Result |
|---|---|---|---|
| Hotel Booking Cancellation Prediction (2026) | End-to-end, leakage-safe ML pipeline and a decision report for a non-technical manager | Python, scikit-learn, chi-squared tests | 19.22/20 (code on request) |
| Rice and Image Classification (2025) | Nine classical classifiers compared, then random forest vs MLP vs CNN on 40,000 images | Python, scikit-learn, TensorFlow, Keras Tuner | Full marks (code on request) |
| [Liveability of Sydney](liveability-of-sydney-sql-postgis/) | Relational and spatial data modelling: schema design, spatial indexing and SQL metrics | PostgreSQL, PostGIS, SQL, Python | High Distinction |
| [Solar Power Forecasting](solar-power-forecasting/) | Time series forecasting at three time scales | Python, statsmodels, ARIMA, Holt-Winters | High Distinction |
| [Wine Expenditure Prediction](wine-expenditure-prediction/) | Regression modelling with a fairness analysis | Python, scikit-learn | High Distinction |
| [Order Management (Agile)](order-management-java-agile/) · [Scroll Management (Scrum)](scroll-management-java-scrum/) | Team software delivery as Scrum Master and developer, with CI and unit tests | Java, Gradle, JUnit, Jenkins, Jira | Distinction |
| [Secure Messaging App](secure-messaging-app-flask/) | Web app with hashed passwords, HTTPS and admin moderation | Python, Flask, Socket.IO, SQLAlchemy | — |

---

### 1. Hotel Booking Cancellation Prediction (2026)
*COMP5310, University of Sydney · pair assignment · coursework repository is private, code available on request*

Predicts which confirmed hotel bookings will be cancelled or end in a no-show, so a revenue manager can follow up with at-risk guests before arrival.

- **My role:** built the data pipeline and the modelling notebook: missing-value analysis, cleaning, feature engineering, the data dictionary, cross-validation design, leakage checks, model tuning, threshold selection and the final evaluation.
- Cleaned ~120k raw bookings to 87,114 records, using chi-squared tests to decide how each column's missing values should be handled.
- Removed fields that would leak the outcome, and kept feature selection inside each cross-validation fold.
- Tuned logistic regression and random forest models that clearly outperformed the baselines on a held-out test set.
- Fully reproducible: pinned requirements, a fixed seed, and notebooks that regenerate every table and figure.

### 2. Liveability of Sydney (2022)
*Spatial data project · team of 3 (team lead)*

Scores the liveability of Sydney's SA2 regions by combining business, transport, school, polling-place, population and income data in a PostgreSQL/PostGIS database.

- Designed a schema of 10+ tables and loaded cleaned datasets into it.
- Added GiST spatial indexes and calculated metrics with spatial joins in SQL.
- Combined the metrics into a z-score and sigmoid liveability score, then extended it with three more datasets (JSON, spatial and CSV).

### 3. Solar Power Production Forecasting (2023)
Forecasts household solar production for the next 24 hours, 7 days and 12 months, comparing naive, Holt-Winters, damped Holt and ARIMA models by MAE.

### 4. Wine Expenditure Prediction (2023)
Predicts customer wine spending from 28 marketing variables. Compares linear regression, KNN and random forest, and checks the final model for fairness using statistical parity and disparate impact.

### 5. Agile & Scrum Software Development (2023)
Two Java command-line applications built by a team of 4 using Kanban and then Scrum. I was Scrum Master and a developer. The work included Jira, Gradle, Jenkins CI, JUnit tests and JaCoCo coverage.

### 6. Secure Messaging App
A Flask and Socket.IO messaging app with bcrypt password hashing, HTTPS, friend lists, discussion posts and admin muting.
