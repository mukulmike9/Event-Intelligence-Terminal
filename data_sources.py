from __future__ import annotations

import io
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin

import pandas as pd
import streamlit as st
import yfinance as yf


HEADERS = {
    "User-Agent": "EventIntelligence/1.0 (+https://streamlit.io)"
}

CB_WATCH_URL = "https://centralbank.watch/tools/economic-calendar/"
RBI_RATES_URL = "https://m.rbi.org.in/home.aspx"
FED_CALENDAR_URL = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
BLS_CPI_URL = "https://www.bls.gov/schedule/news_release/cpi.htm"
BLS_PPI_URL = "https://www.bls.gov/schedule/news_release/ppi.htm"
BLS_EMPLOYMENT_URL = "https://www.bls.gov/schedule/news_release/empsit.htm"
BEA_SCHEDULE_URL = "https://www.bea.gov/news/schedule"

OFFICIAL = {
    "Fed": "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm",
    "RBI": "https://www.rbi.org.in/",
    "ECB": "https://www.ecb.europa.eu/press/calendars/mgcgc/html/index.en.html",
    "BOJ": "https://www.boj.or.jp/en/mopo/mpmsche_minu/index.htm",
    "BOE": "https://www.bankofengland.co.uk/monetary-policy/upcoming-mpc-dates",
    "BLS": "https://www.bls.gov/schedule/",
    "BEA": "https://www.bea.gov/news/schedule",
    "MOSPI": "https://www.mospi.gov.in/",
}


def _safe_get(url: str, timeout: int = 15) -> str | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception:
        return None


def _clean(s) -> str:
    return re.sub(r"\s+", " ", str(s)).strip()



def _parse_fed_calendar() -> pd.DataFrame:
    """Parse future 2026 FOMC dates directly from the Federal Reserve site."""
    html = _safe_get(FED_CALENDAR_URL)
    if not html:
        return pd.DataFrame()

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    # The official Fed page presents 2026 meetings as month + day ranges.
    patterns = [
        ("January", r"January\s+(\d{1,2})\s*[–-]\s*(\d{1,2})"),
        ("March", r"March\s+(\d{1,2})\s*[–-]\s*(\d{1,2})"),
        ("April", r"April\s+(\d{1,2})\s*[–-]\s*(\d{1,2})"),
        ("June", r"June\s+(\d{1,2})\s*[–-]\s*(\d{1,2})"),
        ("July", r"July\s+(\d{1,2})\s*[–-]\s*(\d{1,2})"),
        ("September", r"September\s+(\d{1,2})\s*[–-]\s*(\d{1,2})"),
        ("October", r"October\s+(\d{1,2})\s*[–-]\s*(\d{1,2})"),
        ("December", r"December\s+(\d{1,2})\s*[–-]\s*(\d{1,2})"),
    ]

    rows = []
    year_text = text[text.find("2026 FOMC Meetings"):] if "2026 FOMC Meetings" in text else text

    for month, pattern in patterns:
        m = re.search(pattern, year_text)
        if not m:
            continue
        start_day, end_day = int(m.group(1)), int(m.group(2))
        start = pd.Timestamp(f"2026-{pd.Timestamp(f'2026-{month}-01').month:02d}-{start_day:02d}")
        end = pd.Timestamp(f"2026-{start.month:02d}-{end_day:02d}")
        for dt, label in [(start, "FOMC Meeting"), (end, "FOMC Meeting / Decision")]:
            rows.append({
                "date": dt,
                "time_ist": "See Fed release",
                "country": "United States",
                "event": label,
                "category": "Central Bank",
                "impact": "High",
                "previous": "—",
                "consensus": "—",
                "actual": "—",
                "unit": "—",
                "source": "Fed",
                "source_url": FED_CALENDAR_URL,
                "status": "Scheduled",
                "id": f"Fed-{dt.date()}-{label}",
            })

    return pd.DataFrame(rows).drop_duplicates("id") if rows else pd.DataFrame()


def _parse_cb_watch() -> pd.DataFrame:
    """Parse CentralBankWatch's meeting tables.

    It is used as an aggregation layer for dates, not as a replacement
    for official central-bank releases. Each row is also assigned an
    official central-bank URL.
    """
    html = _safe_get(CB_WATCH_URL)
    rows = []
    if not html:
        return pd.DataFrame()

    soup = BeautifulSoup(html, "html.parser")
    current_bank = None

    bank_map = {
        "Federal Reserve": ("United States", "Fed", OFFICIAL["Fed"]),
        "European Central Bank": ("Euro Area", "ECB", OFFICIAL["ECB"]),
        "Bank of England": ("United Kingdom", "BOE", OFFICIAL["BOE"]),
        "Bank of Japan": ("Japan", "BOJ", OFFICIAL["BOJ"]),
        "Reserve Bank of India": ("India", "RBI", OFFICIAL["RBI"]),
        "Reserve Bank of Australia": ("Australia", "RBA", "https://www.rba.gov.au/monetary-policy/rba-board-minutes/"),
        "Bank of Canada": ("Canada", "BOC", "https://www.bankofcanada.ca/core-functions/monetary-policy/key-interest-rate/"),
        "Swiss National Bank": ("Switzerland", "SNB", "https://www.snb.ch/en/ifor/monpol/id/monpol_current"),
        "Reserve Bank of New Zealand": ("New Zealand", "RBNZ", "https://www.rbnz.govt.nz/monetary-policy/official-cash-rate"),
    }

    for table in soup.find_all("table"):
        prev_heading = table.find_previous(["h2", "h3"])
        heading = _clean(prev_heading.get_text(" ", strip=True)) if prev_heading else ""
        if heading not in bank_map:
            continue

        country, code, source = bank_map[heading]
        for tr in table.find_all("tr"):
            cells = [_clean(c.get_text(" ", strip=True)) for c in tr.find_all(["td", "th"])]
            if len(cells) < 2 or not re.match(r"^\d{4}-\d{2}-\d{2}$", cells[0]):
                continue

            try:
                dt = pd.Timestamp(cells[0])
            except Exception:
                continue

            rows.append(
                {
                    "date": dt,
                    "time_ist": "—",
                    "country": country,
                    "event": cells[1],
                    "category": "Central Bank",
                    "impact": "High",
                    "previous": "—",
                    "consensus": "—",
                    "actual": "—",
                    "unit": "—",
                    "source": code,
                    "source_url": source,
                    "status": "Scheduled",
                    "id": f"{code}-{cells[0]}-{cells[1]}",
                }
            )

    return pd.DataFrame(rows)


def _parse_bls_schedule(url: str, event_filter: str, label: str) -> pd.DataFrame:
    html = _safe_get(url)
    if not html:
        return pd.DataFrame()

    try:
        tables = pd.read_html(io.StringIO(html))
    except Exception:
        return pd.DataFrame()

    rows = []
    for table in tables:
        if table.shape[1] < 3:
            continue
        cols = [str(c) for c in table.columns]
        text = table.astype(str).agg(" ".join, axis=1)
        for idx, row in table.iterrows():
            vals = [str(x) for x in row.tolist()]
            joined = " ".join(vals)
            if event_filter.lower() not in joined.lower():
                continue

            date_match = re.search(
                r"([A-Z][a-z]+\.?\s+\d{1,2},\s+\d{4}|[A-Z][a-z]+\.?\s+\d{1,2}\s+\d{4})",
                joined,
            )
            time_match = re.search(r"(\d{1,2}:\d{2}\s*[AP]M)", joined)
            if not date_match:
                continue

            date_text = date_match.group(1).replace(".", "")
            try:
                dt = pd.to_datetime(date_text)
            except Exception:
                continue

            rows.append(
                {
                    "date": dt,
                    "time_ist": time_match.group(1) if time_match else "08:30 AM ET",
                    "country": "United States",
                    "event": label,
                    "category": "Macro",
                    "impact": "High",
                    "previous": "—",
                    "consensus": "—",
                    "actual": "—",
                    "unit": "—",
                    "source": "BLS",
                    "source_url": url,
                    "status": "Scheduled",
                    "id": f"BLS-{dt.date()}-{label}",
                }
            )

    return pd.DataFrame(rows).drop_duplicates("id") if rows else pd.DataFrame()


def _parse_bea_schedule() -> pd.DataFrame:
    html = _safe_get(BEA_SCHEDULE_URL)
    if not html:
        return pd.DataFrame()

    try:
        tables = pd.read_html(io.StringIO(html))
    except Exception:
        return pd.DataFrame()

    rows = []
    for table in tables:
        if table.shape[1] < 2:
            continue
        for _, row in table.iterrows():
            vals = [_clean(x) for x in row.tolist()]
            joined = " | ".join(vals)
            if not re.search(r"GDP|Personal Income and Outlays|Trade in Goods and Services", joined, re.I):
                continue

            date_match = re.search(r"([A-Z][a-z]+\s+\d{1,2})", joined)
            if not date_match:
                continue

            try:
                dt = pd.to_datetime(f"{date_match.group(1)} 2026")
            except Exception:
                continue

            event = "US GDP / BEA Release"
            if re.search("Personal Income and Outlays", joined, re.I):
                event = "US Personal Income & Outlays (PCE)"
            elif re.search("GDP", joined, re.I):
                event = "US GDP"
            elif re.search("Trade in Goods and Services", joined, re.I):
                event = "US Trade Balance"

            rows.append(
                {
                    "date": dt,
                    "time_ist": "08:30 AM ET",
                    "country": "United States",
                    "event": event,
                    "category": "Macro",
                    "impact": "High" if "GDP" in event or "PCE" in event else "Medium",
                    "previous": "—",
                    "consensus": "—",
                    "actual": "—",
                    "unit": "—",
                    "source": "BEA",
                    "source_url": BEA_SCHEDULE_URL,
                    "status": "Scheduled",
                    "id": f"BEA-{dt.date()}-{event}",
                }
            )

    return pd.DataFrame(rows).drop_duplicates("id") if rows else pd.DataFrame()


def _fallback_macro_events() -> pd.DataFrame:
    """Fallback for environments where official schedule pages block scraping.

    Dates are intentionally limited to high-value releases and should be
    refreshed from the official source connectors whenever the network is
    available.
    """
    today = pd.Timestamp.now(tz="Asia/Kolkata").tz_localize(None).normalize()
    fallback = [
        ("2026-09-30", "US GDP (Third Estimate), Q2 2026", "BEA", "High", "https://www.bea.gov/news/schedule"),
        ("2026-09-30", "US Personal Income & Outlays / PCE", "BEA", "High", "https://www.bea.gov/news/schedule"),
        ("2026-10-02", "US Employment Situation", "BLS", "High", "https://www.bls.gov/schedule/news_release/empsit.htm"),
        ("2026-10-14", "US CPI", "BLS", "High", "https://www.bls.gov/schedule/news_release/cpi.htm"),
        ("2026-10-15", "US PPI", "BLS", "High", "https://www.bls.gov/schedule/news_release/ppi.htm"),
        ("2026-10-29", "US GDP (Advance), Q3 2026", "BEA", "High", "https://www.bea.gov/news/schedule"),
        ("2026-10-29", "US Personal Income & Outlays / PCE", "BEA", "High", "https://www.bea.gov/news/schedule"),
    ]
    rows = []
    for date, event, source, impact, url in fallback:
        dt = pd.Timestamp(date)
        rows.append(
            {
                "date": dt,
                "time_ist": "—",
                "country": "United States",
                "event": event,
                "category": "Macro",
                "impact": impact,
                "previous": "—",
                "consensus": "—",
                "actual": "—",
                "unit": "—",
                "source": source,
                "source_url": url,
                "status": "Scheduled",
                "id": f"{source}-{date}-{event}",
            }
        )
    return pd.DataFrame(rows)


@st.cache_data(ttl=300, show_spinner=False)
def build_event_calendar() -> pd.DataFrame:
    frames = []

    fed = _parse_fed_calendar()
    if not fed.empty:
        frames.append(fed)

    cb = _parse_cb_watch()
    if not cb.empty:
        frames.append(cb)

    for url, filt, label in [
        (BLS_CPI_URL, "CPI", "US CPI"),
        (BLS_PPI_URL, "PPI", "US PPI"),
        (BLS_EMPLOYMENT_URL, "Employment Situation", "US Employment Situation"),
    ]:
        x = _parse_bls_schedule(url, filt, label)
        if not x.empty:
            frames.append(x)

    bea = _parse_bea_schedule()
    if not bea.empty:
        frames.append(bea)

    if not frames:
        frames.append(_fallback_macro_events())

    out = pd.concat(frames, ignore_index=True)

    # Add high-value static central-bank meetings when the aggregator is
    # temporarily unavailable. These are linked to official calendars.
    official_fallback = [
        ("2026-10-27", "Federal Reserve", "FOMC Meeting", "Fed", OFFICIAL["Fed"]),
        ("2026-10-28", "Federal Reserve", "FOMC Meeting / Decision", "Fed", OFFICIAL["Fed"]),
        ("2026-10-07", "India", "RBI MPC Meeting", "RBI", OFFICIAL["RBI"]),
        ("2026-12-04", "India", "RBI MPC Meeting", "RBI", OFFICIAL["RBI"]),
        ("2026-10-29", "Euro Area", "ECB Governing Council Meeting", "ECB", OFFICIAL["ECB"]),
        ("2026-11-05", "United Kingdom", "BOE MPC Meeting", "BOE", OFFICIAL["BOE"]),
        ("2026-10-28", "Japan", "BOJ Monetary Policy Meeting", "BOJ", OFFICIAL["BOJ"]),
    ]

    existing = set(out["id"].tolist()) if not out.empty else set()
    extra = []
    for date, country, event, source, url in official_fallback:
        eid = f"{source}-{date}-{event}"
        if eid not in existing:
            extra.append(
                {
                    "date": pd.Timestamp(date),
                    "time_ist": "—",
                    "country": country,
                    "event": event,
                    "category": "Central Bank",
                    "impact": "High",
                    "previous": "—",
                    "consensus": "—",
                    "actual": "—",
                    "unit": "—",
                    "source": source,
                    "source_url": url,
                    "status": "Scheduled",
                    "id": eid,
                }
            )

    if extra:
        out = pd.concat([out, pd.DataFrame(extra)], ignore_index=True)

    # Deduplicate by event identity.
    out = out.drop_duplicates(subset=["id"]).copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out = out.dropna(subset=["date"]).sort_values(["date", "event"])
    return out.reset_index(drop=True)


@st.cache_data(ttl=60, show_spinner=False)
def fetch_market_snapshot() -> pd.DataFrame:
    tickers = {
        "Nifty 50": "^NSEI",
        "S&P 500": "^GSPC",
        "Nasdaq": "^IXIC",
        "DXY": "DX-Y.NYB",
        "Gold": "GC=F",
        "Brent Crude": "BZ=F",
        "US 10Y": "^TNX",
        "USDINR": "USDINR=X",
    }

    rows = []
    for name, ticker in tickers.items():
        try:
            hist = yf.download(
                ticker,
                period="5d",
                interval="1d",
                progress=False,
                auto_adjust=False,
                threads=False,
            )
            if hist.empty:
                raise ValueError("No data")

            close = hist["Close"]
            if isinstance(close, pd.DataFrame):
                close = close.iloc[:, 0]
            close = close.dropna()

            last = float(close.iloc[-1])
            prev = float(close.iloc[-2]) if len(close) > 1 else last
            change = last - prev
            pct = (change / prev * 100) if prev else 0

            rows.append(
                {
                    "name": name,
                    "ticker": ticker,
                    "price": last,
                    "change": change,
                    "pct": pct,
                    "status": "Market data",
                }
            )
        except Exception as e:
            rows.append(
                {
                    "name": name,
                    "ticker": ticker,
                    "price": None,
                    "change": None,
                    "pct": None,
                    "status": "Unavailable",
                }
            )

    return pd.DataFrame(rows)


@st.cache_data(ttl=900, show_spinner=False)
def fetch_policy_rates() -> pd.DataFrame:
    """Fetch RBI's official current-rate page and combine it with known
    central-bank policy-rate metadata.

    RBI is parsed from the official page; other rates are optional and are
    intentionally marked as reference values when no official API is exposed.
    """
    rows = [
        {
            "bank": "Federal Reserve",
            "code": "Fed",
            "rate": "See latest FOMC",
            "next": "27–28 Oct 2026",
            "days": "—",
            "source": OFFICIAL["Fed"],
            "source_label": "Federal Reserve",
        },
        {
            "bank": "RBI",
            "code": "RBI",
            "rate": "Loading…",
            "next": "07 Oct 2026",
            "days": "—",
            "source": OFFICIAL["RBI"],
            "source_label": "RBI",
        },
        {
            "bank": "European Central Bank",
            "code": "ECB",
            "rate": "See ECB",
            "next": "29 Oct 2026",
            "days": "—",
            "source": OFFICIAL["ECB"],
            "source_label": "ECB",
        },
        {
            "bank": "Bank of Japan",
            "code": "BOJ",
            "rate": "See BOJ",
            "next": "28 Oct 2026",
            "days": "—",
            "source": OFFICIAL["BOJ"],
            "source_label": "BOJ",
        },
        {
            "bank": "Bank of England",
            "code": "BOE",
            "rate": "See BOE",
            "next": "05 Nov 2026",
            "days": "—",
            "source": OFFICIAL["BOE"],
            "source_label": "BOE",
        },
    ]

    html = _safe_get(RBI_RATES_URL)
    if html:
        text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
        match = re.search(r"Policy\s+Repo\s+Rate\s*[:|]?\s*(\d+(?:\.\d+)?)%", text, re.I)
        if match:
            rows[1]["rate"] = f"{match.group(1)}%"

    df = pd.DataFrame(rows)

    now = pd.Timestamp.now(tz="Asia/Kolkata").tz_localize(None).normalize()
    next_dates = {
        "Fed": "2026-10-27",
        "RBI": "2026-10-07",
        "ECB": "2026-10-29",
        "BOJ": "2026-10-28",
        "BOE": "2026-11-05",
    }
    df["days"] = [
        max(0, (pd.Timestamp(next_dates[c]) - now).days)
        for c in df["code"]
    ]
    return df
