# Café Data Analytics Pipeline

A Python data analytics project built for a small café business.
Demonstrates end-to-end pipeline development: data ingestion, cleaning, cost
modeling, and sales visualization — all in plain Python/Pandas/Matplotlib.

## Project Structure

| File | Description |
|------|-------------|
| `analysis_showcase.ipynb` | Full narrative notebook — best starting point |
| `functions.py` | Reusable data loading & analysis functions |
| `inventory.py` | Inventory costs, recipe costing, menu pricing |
| `data_pipeline.py` | Data cleaning and transformation pipeline |
| `report_runner.py` | Report generation and scheduled analysis runner |
| `working_analysis.py` | Primary exploratory analysis script |

## Tech Stack

- **Python 3.10+**
- **Pandas / NumPy** — data manipulation
- **Matplotlib / Seaborn** — visualization
- **ipywidgets** — interactive controls in Jupyter

## Deepnote Module Note

This project was originally developed in [Deepnote](https://deepnote.com),
which supports running one notebook as a module inside another. These are
marked with `# DEEPNOTE MODULE IMPORT` comments. In a standard Python
environment, replace them with imports from the corresponding `.py` files
in this repo.

## Data

Sales and inventory data was exported from a Toast POS system as CSV files.
The pipeline handles:
- Monthly sales exports (`menu-breakdown-*.csv`)
- Itemized transaction data (`ItemSelectionDetails-*.csv`)
- Inventory/recipe Excel workbooks
