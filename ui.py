from __future__ import annotations

import html
import streamlit as st
import pandas as pd


def inject_css():
    st.markdown(
        """
        <style>
        :root {
            --bg:#07111c;
            --panel:#0c1a28;
            --panel2:#102233;
            --line:#1e3a52;
            --text:#edf5ff;
            --muted:#91a5b8;
            --blue:#1890ff;
            --green:#00d395;
            --red:#ff4d5f;
            --amber:#f5b642;
        }
        .stApp { background:var(--bg); color:var(--text); }
        [data-testid="stSidebar"] { background:#081522; border-right:1px solid var(--line); }
        [data-testid="stSidebar"] * { color:#dce8f4; }
        h1,h2,h3,h4 { color:#f5f9ff !important; letter-spacing:-.02em; }
        .block-container { padding-top:1.2rem; max-width:1600px; }
        div[data-testid="stMetric"] {
            background:linear-gradient(180deg,#102335,#0b1a28);
            border:1px solid #1e3c55;
            border-radius:10px;
            padding:.65rem .75rem;
        }
        div[data-testid="stMetricLabel"] { color:#9db0c3; }
        div[data-testid="stMetricValue"] { color:#f4f8fc; font-size:1.35rem; }
        .ei-top {
            display:flex; justify-content:space-between; align-items:center;
            padding:.35rem 0 .8rem; border-bottom:1px solid var(--line);
            margin-bottom:.9rem;
        }
        .ei-brand { font-size:1.45rem; font-weight:750; letter-spacing:.02em; }
        .ei-sub { color:#8fa4b8; font-size:.78rem; margin-top:2px; }
        .live-dot { display:inline-block; width:9px; height:9px; border-radius:50%;
                    background:#00d395; margin-right:7px; box-shadow:0 0 9px #00d395; }
        .source { color:#6f8ba2; font-size:.72rem; }
        .event-row {
            padding:.55rem .65rem; border-bottom:1px solid #183247;
            background:#0b1b29;
        }
        .event-row:hover { background:#10283b; }
        .impact-high { color:#ff6d7b; font-weight:700; }
        .impact-medium { color:#f4c04d; font-weight:700; }
        .impact-low { color:#20d9a0; font-weight:700; }
        .small { color:#8ea3b7; font-size:.78rem; }
        .panel {
            background:linear-gradient(180deg,#0c1b29,#0a1723);
            border:1px solid #1d3a51; border-radius:12px; padding:14px;
        }
        .panel-title { font-weight:700; font-size:1rem; margin-bottom:8px; }
        .detail-card {
            background:linear-gradient(180deg,#0d1e2d,#0a1723);
            border:1px solid #1d425c; border-radius:12px; padding:16px;
        }
        .tag { padding:3px 8px; border-radius:6px; font-size:.72rem; font-weight:700; }
        .tag-high { background:#3a1820; color:#ff7180; }
        .tag-medium { background:#3a2e16; color:#f3c253; }
        .tag-low { background:#12362e; color:#27d7a0; }
        footer { visibility:hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        """
        <div class="ei-top">
          <div>
            <div class="ei-brand">EVENT INTELLIGENCE</div>
            <div class="ei-sub">Global Financial Events &amp; Market Intelligence</div>
          </div>
          <div style="text-align:right">
            <span class="live-dot"></span><b>Live data layer</b>
            <div class="source">Sources are displayed per event</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_market_strip(market: pd.DataFrame):
    cols = st.columns(len(market))
    for col, (_, r) in zip(cols, market.iterrows()):
        with col:
            price = "—" if pd.isna(r["price"]) else f"{r['price']:,.2f}"
            if pd.isna(r["pct"]):
                delta = "Unavailable"
            else:
                sign = "+" if r["pct"] >= 0 else ""
                delta = f"{sign}{r['pct']:.2f}%"
            st.metric(r["name"], price, delta)


def _impact_class(value):
    return {
        "High": "impact-high",
        "Medium": "impact-medium",
        "Low": "impact-low",
    }.get(value, "small")


def render_event_table(df: pd.DataFrame):
    if df.empty:
        st.info("No events match the selected filters.")
        return None

    header = st.columns([1.0, .8, 2.3, 1.1, .8, .9, .9, .8, .7, 1.0, .9])
    labels = ["Date", "Time", "Event", "Category", "Impact", "Previous", "Consensus", "Actual", "Unit", "Source", "Status"]
    for c, label in zip(header, labels):
        c.markdown(f"**{label}**")

    selected = None
    for _, r in df.iterrows():
        cols = st.columns([1.0, .8, 2.3, 1.1, .8, .9, .9, .8, .7, 1.0, .9])
        cols[0].write(r["date"].strftime("%d %b"))
        cols[1].write(str(r["time_ist"]))
        if cols[2].button(r["event"], key=f"event-{r['id']}", use_container_width=True):
            selected = r["id"]
        cols[3].write(r["category"])
        cols[4].markdown(f"<span class='{_impact_class(r['impact'])}'>{r['impact']}</span>", unsafe_allow_html=True)
        cols[5].write(str(r["previous"]))
        cols[6].write(str(r["consensus"]))
        cols[7].write(str(r["actual"]))
        cols[8].write(str(r["unit"]))
        cols[9].write(str(r["source"]))
        cols[10].write(str(r["status"]))

    return selected


def render_event_detail(row, market: pd.DataFrame):
    st.markdown("---")
    left, right = st.columns([2.2, 1])

    with left:
        st.markdown(f"### {row['event']}")
        st.caption(
            f"{row['country']} · {row['category']} · {row['date'].strftime('%d %b %Y')} · {row['time_ist']}"
        )
        st.markdown(
            f"""
            <div class="detail-card">
              <span class="tag tag-{row['impact'].lower()}">{row['impact']} impact</span>
              <br><br>
              <b>Previous:</b> {html.escape(str(row['previous']))}
              &nbsp;&nbsp; <b>Consensus:</b> {html.escape(str(row['consensus']))}
              &nbsp;&nbsp; <b>Actual:</b> {html.escape(str(row['actual']))}
              &nbsp;&nbsp; <b>Unit:</b> {html.escape(str(row['unit']))}
              <br><br>
              <span class="source">Source: {html.escape(str(row['source']))}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if row.get("source_url"):
            st.link_button("Open official / source page", row["source_url"])

    with right:
        st.markdown("**Related market watch**")
        relevant = ["S&P 500", "Nifty 50", "DXY", "Gold", "Brent Crude", "US 10Y", "USDINR"]
        m = market[market["name"].isin(relevant)]
        for _, r in m.iterrows():
            if pd.isna(r["pct"]):
                st.write(f"{r['name']}: —")
            else:
                st.write(f"{r['name']}: {r['price']:,.2f} ({r['pct']:+.2f}%)")


def render_bottom_panels(rates, events, market, central_banks_only=False, macro_only=False):
    st.markdown("---")

    if central_banks_only:
        render_central_banks(rates)
        return

    if macro_only:
        render_macro(events)
        return

    c1, c2, c3, c4 = st.columns([1.2, 1.5, 1.4, 1.2])
    with c1:
        render_central_banks(rates)
    with c2:
        render_macro(events)
    with c3:
        render_impact(events)
    with c4:
        render_recent_upcoming(events)


def render_central_banks(rates):
    st.markdown('<div class="panel"><div class="panel-title">Central Bank Watch</div>', unsafe_allow_html=True)
    for _, r in rates.iterrows():
        st.markdown(
            f"**{r['bank']}**  \n"
            f"<span class='small'>{r['rate']} · next {r['next']} · {r['days']}d</span>",
            unsafe_allow_html=True,
        )
        st.divider()
    st.markdown("</div>", unsafe_allow_html=True)


def render_macro(events):
    macro = events[events["category"] == "Macro"].copy()
    st.markdown('<div class="panel"><div class="panel-title">Macro Release Monitor</div>', unsafe_allow_html=True)
    if macro.empty:
        st.write("No macro releases loaded.")
    else:
        show = macro.sort_values("date").head(10)
        for _, r in show.iterrows():
            st.write(f"**{r['event']}** · {r['date'].strftime('%d %b')} · {r['source']}")
    st.markdown("</div>", unsafe_allow_html=True)


def render_impact(events):
    st.markdown('<div class="panel"><div class="panel-title">Event Impact Map</div>', unsafe_allow_html=True)
    x = events.groupby(["category", "impact"]).size().unstack(fill_value=0)
    st.dataframe(x, use_container_width=True, height=270)
    st.markdown("</div>", unsafe_allow_html=True)


def render_recent_upcoming(events):
    st.markdown('<div class="panel"><div class="panel-title">Recent & Upcoming</div>', unsafe_allow_html=True)
    now = pd.Timestamp.now().normalize()
    upcoming = events[events["date"] >= now].sort_values("date").head(7)
    for _, r in upcoming.iterrows():
        st.write(f"**{r['date'].strftime('%d %b')}** · {r['event']} · {r['impact']}")
    st.markdown("</div>", unsafe_allow_html=True)
