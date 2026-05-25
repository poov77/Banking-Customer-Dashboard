# Banking-Customer-Dashboard

This Streamlit project analyzes the cleaned American banking customer dataset.

## Files

- `app.py` - Streamlit dashboard app.
- `save_assets.py` - Creates a static PNG dashboard image.
- `American Banking Data - Fully_Cleaned_Data.csv` - Main dataset used by the app.
- `assets/banking_dashboard.png` - Generated dashboard image.

## Run The Streamlit App

From this folder, run:

```powershell
C:\Users\poova\anaconda3\python.exe -m streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## Save Dashboard As PNG

Run:

```powershell
C:\Users\poova\anaconda3\python.exe save_assets.py
```

The image will be saved to:

```text
assets/banking_dashboard.png
```

## Dashboard Features

- Customer count, average balance, total balance, and loan default rate.
- Filters for state, job classification, gender, and age range.
- Charts for customers by state, average balance by job, and monthly joins.
- Data preview and filtered CSV download.
