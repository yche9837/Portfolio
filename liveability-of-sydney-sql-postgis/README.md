# Liveability of Sydney — Spatial Data Analysis

*University of Sydney, 2022 · team of 3 (team lead) · High Distinction*

## Question
Which of Sydney's SA2 regions are the most liveable, and how does liveability relate to income?

## What we built
1. **Database design.** Cleaned 10 datasets and loaded them into PostgreSQL with PostGIS, using a defined schema: SA2 boundaries, businesses, transport stops, polling places, primary, secondary and future school catchments, population and income.
2. **Indexing.** Added GiST spatial indexes on geometry columns and B-tree indexes on SA2 codes, so spatial joins run quickly.
3. **Metrics in SQL.** Calculated per-region metrics for retail, health, transport stops, polling places and schools. Standardised each one as a z-score and combined them with a sigmoid function into a 0–1 liveability score.
4. **Extension.** Added three more data sources in different formats (safety cameras from JSON, playgrounds as spatial data, rain gardens from CSV) and recalculated the score.
5. **Analysis.** Mapped scores across Sydney and tested their correlation with median income (r = 0.15, a weak positive relationship).

## Tools
PostgreSQL · PostGIS · SQL · Python (pandas, GeoPandas, SQLAlchemy) · Jupyter

## Files
| File | Contents |
|---|---|
| `project.ipynb` | Cleaning, schema creation, indexing, metric SQL and visualisations |
| `Group5Report.pdf` | Final report |

> Database credentials are read from a local `Credentials.json`, which is not included in the repository.
