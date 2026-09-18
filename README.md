# Event Intelligence

**Global Financial Events & Market Intelligence**

A Streamlit-based institutional-style dashboard for monitoring:

- Federal Reserve / FOMC
- RBI / MPC
- ECB / BOJ / BOE
- US CPI / PPI / Employment
- US GDP / PCE / Personal Income & Outlays
- India and global central-bank events
- Nifty 50 / S&P 500 / Nasdaq / DXY / Gold / Brent / US 10Y / USDINR
- Previous / consensus / actual / unit / source fields
- Event-level source links
- Market-watch context

## Data philosophy

This project separates **scheduled event data** from **market-price data**.

### Primary / official sources

- Federal Reserve — FOMC calendar and releases
- RBI — policy rates and official releases
- ECB — monetary-policy calendar
- Bank of Japan — monetary-policy calendar
- Bank of England — MPC calendar
- BLS — CPI, PPI, Employment Situation
- BEA — GDP, PCE, Personal Income & Outlays
- MOSPI — Indian macro data

### Aggregation fallback

CentralBankWatch is used as an aggregation/checking layer for global central-bank meeting dates. The UI still exposes the official central-bank source for the relevant institution.

### Market prices

`yfinance` is used for market snapshots. Yahoo Finance data can be delayed and should not be represented as exchange-grade real-time data. The UI therefore describes the market layer as market data rather than guaranteed exchange real-time data.

## Run locally

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## GitHub

```bash
git init
git add .
git commit -m "Initial Event Intelligence dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/event-intelligence.git
git push -u origin main
```

## Streamlit Community Cloud
**Deployment Link :** https://event-intelligence-terminal-001.streamlit.app/
1. Push the repository to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub account.
4. Choose **Create app**.
5. Select the repository.
6. Branch: `main`
7. Main file: `app.py`
8. Deploy.

The repository should contain `app.py` and `requirements.txt` at the root.

## Important deployment note

Do **not** commit API keys or `.streamlit/secrets.toml`.

If you later add a paid market-data provider or FRED API key, put the key into Streamlit Community Cloud's Secrets settings and access it with `st.secrets`.

## Production upgrades

Recommended next steps:

1. Replace/augment yfinance with a licensed market-data provider if true real-time exchange data is required.
2. Add official RSS/ICS/API connectors wherever available.
3. Store normalized events in PostgreSQL/Supabase for history.
4. Add user watchlists and alerts.
5. Add historical market reaction calculations.
6. Add authentication if the dashboard becomes internal/B2B.
7. Add monitoring for failed source connectors.
