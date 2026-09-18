import streamlit as st
from event_intelligence.data_sources import fetch_market_snapshot, build_event_calendar, fetch_policy_rates
from event_intelligence.ui import inject_css, render_sidebar, render_header, render_market_strip, render_event_workspace, render_bottom_panels

st.set_page_config(page_title="Event Intelligence", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
inject_css()
page, auto_refresh, refresh_seconds, manual_refresh = render_sidebar()
if manual_refresh:
    st.cache_data.clear()

@st.fragment(run_every=refresh_seconds if auto_refresh else None)
def dashboard():
    render_header()
    market = fetch_market_snapshot()
    render_market_strip(market)
    events = build_event_calendar()
    if page in ("Overview", "Event Calendar"):
        render_event_workspace(events, market)
        rates = fetch_policy_rates()
        render_bottom_panels(rates, events, market)
    elif page == "Central Banks":
        st.markdown("## Central Bank Watch")
        st.caption("Policy meetings, current policy-rate context and source attribution.")
        render_bottom_panels(fetch_policy_rates(), events, market, central_banks_only=True)
    else:
        st.markdown("## Macro Data Monitor")
        st.caption("Key scheduled macro releases with previous, consensus and actual fields where available.")
        render_bottom_panels(fetch_policy_rates(), events, market, macro_only=True)

dashboard()
