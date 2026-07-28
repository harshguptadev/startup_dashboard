# Startup Funding Analysis Dashboard

An interactive Streamlit dashboard for exploring Indian startup funding data - overall market trends, startup-wise deep dives, and investor-wise analysis.

🔗 **Live App:** https://harshguptadev-startup-dashboard-app-ohfbzl.streamlit.app/

## Features

- **Overall Analysis**
  - Total funding amount, peak funding month, max single-startup funding, and total startups funded at a glance
  - Month-over-month funding trend chart for any selected year
- **Startup Analysis**
  - Vertical, sub-vertical, and city lookup for any startup
  - Last 5 funding rounds received
- **Investor Analysis**
  - Last 5 investments made
  - Biggest bets by startup (bar chart + table)
  - Sector-wise investment split (pie chart + table)
  - Preferred investment sectors
  - Funding round type breakdown (pie chart + table)

## Tech Stack

- [Streamlit](https://streamlit.io/) - app framework
- [Pandas](https://pandas.pydata.org/) - data manipulation
- [NumPy](https://numpy.org/) - numerical operations
- [Matplotlib](https://matplotlib.org/) - charts

## Dataset

The dataset (`startup_funding_cleaned.csv`) contains cleaned records of Indian startup funding, including startup name, investor(s), funding round, sector/vertical, city, amount (in Cr), and date. *(Add the original source link here, e.g. Kaggle, if applicable.)*

## Project Structure

```
startup_dashboard/
├── app.py                          # Main Streamlit app
├── startup_funding_cleaned.csv     # Dataset
├── notebooks/
│   └── test.ipynb                  # EDA and logic development notebook
├── requirements.txt                # Python dependencies
└── README.md
```

The core data-cleaning and grouping logic was first developed and validated in `notebooks/test.ipynb` before being ported into `app.py`.

## Run Locally

```bash
git clone https://github.com/harshguptadev/startup_dashboard.git
cd startup_dashboard
pip install -r requirements.txt
streamlit run app.py
```

## Future Work

- A few startup-page fields are still being added
- No caching yet for filtered/grouped views beyond the base dataset load
- Deployment polish (favicon, page config tweaks) pending

## Author

Built by [Harsh Gupta](https://github.com/harshguptadev)
