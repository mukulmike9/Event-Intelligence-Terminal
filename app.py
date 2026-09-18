import streamlit as st
import pandas as pd
from datetime import datetime, timezone

from event_intelligence.data_sources import (
    fetch_market_snapshot,
    build_event_calendar,
    fetch_policy_rates,
)
from event_intelligence.ui import (
    inject_css,
    render_header,
    render_market_strip,
    render_event_table,
    render_event_detail,
    render_bottom_panels,
)

st.set_page_config(
    page_title="Event Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# -----------------------------
# Runtime controls
# -----------------------------
with st.sidebar:
    st.markdown("## EVENT INTELLIGENCE")
    st.caption("Global Financial Events & Market Intelligence")
    st.divider()

    page = st.radio(
        "Workspace",
        ["Overview", "Event Calendar", "Central Banks", "Macro Data"],
        index=0,
        label_visibility="collapsed",
    )

    st.divider()
    auto_refresh = st.toggle("Auto-refresh", value=True)
    refresh_seconds = st.select_slider(
        "Refresh interval",
        options=[30, 60, 120, 300],
        value=60,
        format_func=lambda x: f"{x}s",
    )
    manual_refresh = st.button("↻ Refresh now", use_container_width=True)

    st.divider()
    st.caption("Primary sources")
    st.markdown(
        "Fed · RBI · ECB · BOJ · BOE · BLS · BEA · MOSPI"
    )
    st.caption("Market data: Yahoo Finance via yfinance")
    st.caption("Calendar aggregation: CentralBankWatch")

# Fragment reruns keep the app responsive and allow the market/event layer
# to refresh without requiring a full page reload.
@st.fragment(run_every=refresh_seconds if auto_refresh else None)
def dashboard():
    if manual_refresh:
        st.cache_data.clear()

    render_header()

    market = fetch_market_snapshot()
    render_market_strip(market)

    events = build_event_calendar()

    if page in ("Overview", "Event Calendar"):
        st.markdown("### Global Financial Events")
        st.caption("Scheduled releases and policy events. Times are displayed in IST.")

        c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 2])
        with c1:
            horizon = st.selectbox("Window", ["Today", "Next 7 Days", "Next 30 Days"], index=1)
        with c2:
            countries = ["All"] + sorted(events["country"].dropna().unique().tolist())
            country = st.selectbox("Country", countries)
        with c3:
            cats = ["All"] + sorted(events["category"].dropna().unique().tolist())
            category = st.selectbox("Category", cats)
        with c4:
            impacts = ["All", "High", "Medium", "Low"]
            impact = st.selectbox("Impact", impacts)
        with c5:
            query = st.text_input("Search", placeholder="CPI, FOMC, RBI, GDP, PCE...")

        filtered = events.copy()
        now = pd.Timestamp.now(tz="Asia/Kolkata").tz_localize(None)

        if horizon == "Today":
            filtered = filtered[filtered["date"].dt.date == now.date()]
        elif horizon == "Next 7 Days":
            filtered = filtered[
                (filtered["date"] >= now.normalize())
                & (filtered["date"] <= now.normalize() + pd.Timedelta(days=7))
            ]
        else:
            filtered = filtered[
                (filtered["date"] >= now.normalize())
                & (filtered["date"] <= now.normalize() + pd.Timedelta(days=30))
            ]

        if country != "All":
            filtered = filtered[filtered["country"] == country]
        if category != "All":
            filtered = filtered[filtered["category"] == category]
        if impact != "All":
            filtered = filtered[filtered["impact"] == impact]
        if query:
            mask = (
                filtered["event"].str.contains(query, case=False, na=False)
                | filtered["country"].str.contains(query, case=False, na=False)
                | filtered["source"].str.contains(query, case=False, na=False)
            )
            filtered = filtered[mask]

        filtered = filtered.sort_values(["date", "time_ist"]).head(80)

        selected_id = render_event_table(filtered)

        if selected_id:
            selected = filtered[filtered["id"] == selected_id]
            if not selected.empty:
                render_event_detail(selected.iloc[0], market)

        rates = fetch_policy_rates()
        render_bottom_panels(rates, events, market)

    elif page == "Central Banks":
        st.markdown("### Central Bank Watch")
        st.caption("Upcoming policy meetings from official schedules where available, with CentralBankWatch as an aggregation fallback.")
        rates = fetch_policy_rates()
        render_bottom_panels(rates, events, market, central_banks_only=True)

    elif page == "Macro Data":
        st.markdown("### Macro Data Monitor")
        st.caption("Key US and India indicators with source attribution and release dates.")
        rates = fetch_policy_rates()
        render_bottom_panels(rates, events, market, macro_only=True)

dashboard()
