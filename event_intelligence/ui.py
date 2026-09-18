from __future__ import annotations
import html
import streamlit as st
import pandas as pd


def inject_css():
    st.markdown(r'''<style>
:root{--bg:#050c14;--panel:#0a1521;--line:#1b3449;--line2:#23445d;--text:#f3f7fb}
.stApp{background:radial-gradient(circle at 85% 0%,rgba(40,100,150,.10),transparent 30%),var(--bg);color:var(--text)}
[data-testid="stSidebar"]{background:#07111b;border-right:1px solid #183247}[data-testid="stSidebar"] *{color:#dce8f3}
.block-container{max-width:1720px;padding-top:1.05rem;padding-bottom:2rem}h1,h2,h3,h4{color:#f7faff!important;letter-spacing:-.025em}
.ei-header{display:flex;justify-content:space-between;align-items:flex-start;padding:.15rem 0 .85rem;border-bottom:1px solid var(--line);margin-bottom:.8rem}
.ei-brand{font-size:1.65rem;line-height:1;font-weight:800;letter-spacing:.08em;color:#f6f9fd}.ei-sub{margin-top:.42rem;color:#8ea6bb;font-size:.78rem}.ei-live{text-align:right;color:#dce8f3;font-size:.78rem}
.live-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#15d89a;box-shadow:0 0 10px rgba(21,216,154,.7);margin-right:6px}
.market-card{min-height:91px;background:linear-gradient(180deg,#0d2030,#091723);border:1px solid #1d4058;border-radius:10px;padding:11px 12px 9px;box-sizing:border-box}
.market-name{font-size:.73rem;color:#a5b7c8;font-weight:650;margin-bottom:6px}.market-price{font-size:1.18rem;font-weight:760;color:#f5f8fc;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.market-delta{display:inline-block;margin-top:6px;padding:3px 7px;border-radius:999px;font-size:.69rem;font-weight:700}.delta-up{color:#39e1ad;background:rgba(24,211,154,.12)}.delta-down{color:#ff7382;background:rgba(255,91,110,.12)}.delta-flat{color:#a9b8c7;background:rgba(169,184,199,.10)}
.section-bar{display:flex;align-items:end;margin:1rem 0 .55rem}.section-title{font-size:1.05rem;font-weight:780;color:#f3f7fb}.section-sub{font-size:.72rem;color:#7f96aa}
.event-shell{background:linear-gradient(180deg,#081521,#07111a);border:1px solid var(--line);border-radius:12px;overflow:hidden}
.event-head,.event-row{display:grid;grid-template-columns:70px 58px minmax(210px,2.15fr) 100px 65px 78px 78px 72px 48px 82px 75px;align-items:center}
.event-head{background:#0d1e2d;border-bottom:1px solid var(--line2);color:#9fb4c6;font-size:.63rem;font-weight:750;text-transform:uppercase;letter-spacing:.04em;padding:10px 11px}
.event-row{padding:9px 11px;border-bottom:1px solid #132b3d;min-height:47px;font-size:.70rem;color:#dce7f0}.event-row:last-child{border-bottom:0}.event-row:hover{background:#0c1d2b}
.event-name{color:#f2f6fa;font-weight:650;line-height:1.2}.event-muted{color:#8fa4b7}.impact-high{color:#ff6577;font-weight:800}.impact-medium{color:#f2c55a;font-weight:800}.impact-low{color:#27d8a0;font-weight:800}
.status-upcoming{color:#58adff;font-weight:750}.status-scheduled{color:#a8b8c7;font-weight:700}.status-released{color:#32d7a5;font-weight:750}
.detail-card{background:linear-gradient(180deg,#0d1d2b,#091621);border:1px solid #21445d;border-radius:12px;padding:15px;min-height:310px}
.detail-kicker{color:#78a9cf;font-size:.67rem;text-transform:uppercase;letter-spacing:.08em;font-weight:800}.detail-title{font-size:1.16rem;font-weight:800;margin:.25rem 0 .2rem;color:#f5f8fc}.detail-meta{color:#91a7b9;font-size:.72rem;margin-bottom:12px}
.tag{display:inline-block;padding:4px 8px;border-radius:6px;font-size:.66rem;font-weight:800;text-transform:uppercase;letter-spacing:.04em}.tag-high{color:#ff7280;background:#3a1820}.tag-medium{color:#f2c65a;background:#392d15}.tag-low{color:#31d9a5;background:#12362e}
.stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin:12px 0}.stat{background:#09131e;border:1px solid #1a3448;border-radius:7px;padding:8px}.stat-label{color:#748ca1;font-size:.62rem}.stat-value{color:#edf4fa;font-size:.83rem;font-weight:760;margin-top:3px}.detail-copy{color:#aebdca;font-size:.73rem;line-height:1.5}.source-line{color:#657d91;font-size:.64rem;margin-top:9px}
.panel{background:linear-gradient(180deg,#0a1723,#08131d);border:1px solid #1a3549;border-radius:11px;padding:13px;min-height:220px}.panel-title{color:#eef4f9;font-size:.86rem;font-weight:800;margin-bottom:10px}.panel-sub{color:#71889b;font-size:.66rem;margin-top:-6px;margin-bottom:10px}
.cb-row,.macro-row,.recent-row{padding:7px 0;border-bottom:1px solid #142b3c;font-size:.72rem}.cb-row:last-child,.macro-row:last-child,.recent-row:last-child{border-bottom:0}.row-main{color:#e5edf4;font-weight:680}.row-meta{color:#7f95a8;font-size:.65rem;margin-top:2px}
.heatmap{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}.heat-cell{border:1px solid #1c384d;border-radius:7px;padding:8px;background:#0c1b28}.heat-label{color:#8fa4b7;font-size:.62rem}.heat-value{color:#eef4f8;font-size:.82rem;font-weight:800;margin-top:3px}
div[data-testid="stTabs"] button{font-size:.76rem;font-weight:700}div[data-testid="stSelectbox"] label,div[data-testid="stTextInput"] label{color:#8ea5b8!important;font-size:.68rem!important}
div[data-testid="stSelectbox"]>div>div{background:#0b1723;border-color:#1d3a50}div[data-testid="stTextInput"] input{background:#0b1723;border:1px solid #1d3a50;color:#eef4f9}.stButton>button{background:#0d2030;border:1px solid #23465e;color:#eaf2f8;font-size:.72rem}footer{visibility:hidden}
@media(max-width:1200px){.event-head,.event-row{grid-template-columns:62px 50px minmax(170px,2fr) 88px 60px 70px 70px 65px 45px 75px 68px;font-size:.62rem}.market-price{font-size:1.02rem}}
</style>''', unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("## EVENT INTELLIGENCE")
        st.caption("Global Financial Events & Market Intelligence")
        st.divider()
        page=st.radio("Workspace",["Overview","Event Calendar","Central Banks","Macro Data"],index=0,label_visibility="collapsed")
        st.divider(); auto=st.toggle("Auto-refresh",True); secs=st.select_slider("Refresh interval",[30,60,120,300],60,format_func=lambda x:f"{x}s")
        manual=st.button("↻ Refresh now",use_container_width=True)
        st.divider(); st.caption("DATA LAYERS"); st.markdown("Fed · RBI · ECB · BOJ · BOE"); st.markdown("BLS · BEA · MOSPI"); st.caption("Market: Yahoo Finance / yfinance"); st.caption("Calendar fallback: CentralBankWatch")
    return page,auto,secs,manual


def render_header():
    st.markdown('<div class="ei-header"><div><div class="ei-brand">EVENT INTELLIGENCE</div><div class="ei-sub">Global Financial Events &amp; Market Intelligence</div></div><div class="ei-live"><span class="live-dot"></span><b>LIVE DATA LAYER</b><div style="margin-top:4px;color:#6f879a;font-size:.66rem">Source attribution shown at event level</div></div></div>',unsafe_allow_html=True)


def render_market_strip(market):
    cols=st.columns(8,gap="small")
    for col,(_,r) in zip(cols,market.head(8).iterrows()):
        with col:
            price="—" if pd.isna(r["price"]) else f'{r["price"]:,.2f}'; pct=r["pct"]
            cls,delta=("delta-flat","—") if pd.isna(pct) else (("delta-up",f"+{pct:.2f}%") if pct>=0 else ("delta-down",f"{pct:.2f}%"))
            st.markdown(f'<div class="market-card"><div class="market-name">{html.escape(str(r["name"]))}</div><div class="market-price">{html.escape(price)}</div><span class="market-delta {cls}">{html.escape(delta)}</span></div>',unsafe_allow_html=True)


def _fmt(v):
    if v is None:return "—"
    try:
        if pd.isna(v):return "—"
    except Exception:pass
    s=str(v); return "—" if s.lower() in ("nan","none","") else s


def _impact_class(v): return {"High":"impact-high","Medium":"impact-medium","Low":"impact-low"}.get(str(v),"event-muted")
def _status_class(v): return {"Upcoming":"status-upcoming","Scheduled":"status-scheduled","Released":"status-released"}.get(str(v),"event-muted")


def _event_table_html(df):
    parts=['<div class="event-shell"><div class="event-head"><div>Date</div><div>Time</div><div>Event</div><div>Category</div><div>Impact</div><div>Previous</div><div>Consensus</div><div>Actual</div><div>Unit</div><div>Source</div><div>Status</div></div>']
    for _,r in df.iterrows():
        parts.append(f'''<div class="event-row"><div>{html.escape(pd.Timestamp(r["date"]).strftime("%d %b"))}</div><div class="event-muted">{html.escape(_fmt(r["time_ist"]))}</div><div class="event-name">{html.escape(_fmt(r["event"]))}</div><div class="event-muted">{html.escape(_fmt(r["category"]))}</div><div class="{_impact_class(r["impact"])}">{html.escape(_fmt(r["impact"]))}</div><div>{html.escape(_fmt(r["previous"]))}</div><div>{html.escape(_fmt(r["consensus"]))}</div><div>{html.escape(_fmt(r["actual"]))}</div><div class="event-muted">{html.escape(_fmt(r["unit"]))}</div><div class="event-muted">{html.escape(_fmt(r["source"]))}</div><div class="{_status_class(r["status"])}">{html.escape(_fmt(r["status"]))}</div></div>''')
    st.markdown("".join(parts)+"</div>",unsafe_allow_html=True)


def _filter_events(events,horizon,country,category,impact,query):
    f=events.copy()
    if f.empty:return f
    now=pd.Timestamp.now(tz="Asia/Kolkata").tz_localize(None).normalize()
    if horizon=="Today": f=f[f["date"].dt.normalize()==now]
    elif horizon=="Tomorrow": f=f[f["date"].dt.normalize()==now+pd.Timedelta(days=1)]
    elif horizon=="Next 7 Days": f=f[(f["date"]>=now)&(f["date"]<=now+pd.Timedelta(days=7))]
    elif horizon=="Next 30 Days": f=f[(f["date"]>=now)&(f["date"]<=now+pd.Timedelta(days=30))]
    if country!="All": f=f[f["country"]==country]
    if category!="All": f=f[f["category"]==category]
    if impact!="All": f=f[f["impact"]==impact]
    if query:
        q=query.strip(); mask=(f["event"].astype(str).str.contains(q,case=False,na=False)|f["country"].astype(str).str.contains(q,case=False,na=False)|f["source"].astype(str).str.contains(q,case=False,na=False)|f["category"].astype(str).str.contains(q,case=False,na=False)); f=f[mask]
    return f.sort_values(["date","time_ist"]).head(100)


def render_event_workspace(events,market):
    st.markdown('<div class="section-bar"><div><div class="section-title">Upcoming Events</div><div class="section-sub">Macro releases, policy decisions and market-moving scheduled events</div></div></div>',unsafe_allow_html=True)
    tabs=st.tabs(["TODAY","TOMORROW","NEXT 7 DAYS","NEXT 30 DAYS","ALL EVENTS"]); horizons=["Today","Tomorrow","Next 7 Days","Next 30 Days","All Events"]
    countries=["All"]+sorted(events["country"].dropna().astype(str).unique().tolist()) if not events.empty else ["All"]
    categories=["All"]+sorted(events["category"].dropna().astype(str).unique().tolist()) if not events.empty else ["All"]
    for i,tab in enumerate(tabs):
        with tab:
            c1,c2,c3,c4=st.columns([1,1,1,2])
            with c1: country=st.selectbox("Country",countries,key=f"country-{i}")
            with c2: category=st.selectbox("Category",categories,key=f"category-{i}")
            with c3: impact=st.selectbox("Impact",["All","High","Medium","Low"],key=f"impact-{i}")
            with c4: query=st.text_input("Search",placeholder="CPI, FOMC, RBI, GDP, PCE...",key=f"search-{i}")
            filtered=_filter_events(events,horizons[i],country,category,impact,query)
            if filtered.empty: st.info("No events match the selected filters."); continue
            labels=[f'{pd.Timestamp(r["date"]).strftime("%d %b")} · {_fmt(r["time_ist"])} · {_fmt(r["country"])} · {_fmt(r["event"])}' for _,r in filtered.iterrows()]
            selected_label=st.selectbox("Event intelligence focus",labels,index=0,key=f"event-focus-{i}",label_visibility="collapsed"); selected=filtered.iloc[labels.index(selected_label)]
            left,right=st.columns([1.62,1],gap="medium")
            with left:
                _event_table_html(filtered); st.markdown(f'<div class="source-line">Showing {len(filtered)} event(s) · Missing consensus/actual values are shown as —.</div>',unsafe_allow_html=True)
            with right: render_event_detail(selected,market)


def render_event_detail(row,market):
    impact=str(row.get("impact","")); tag_cls={"High":"tag-high","Medium":"tag-medium","Low":"tag-low"}.get(impact,"tag-medium")
    title=html.escape(_fmt(row.get("event"))); meta=f'{html.escape(_fmt(row.get("country")))} · {html.escape(_fmt(row.get("category")))} · {pd.Timestamp(row["date"]).strftime("%d %b %Y")} · {html.escape(_fmt(row.get("time_ist")))}'
    st.markdown(f'''<div class="detail-card"><div class="detail-kicker">EVENT INTELLIGENCE</div><div class="detail-title">{title}</div><div class="detail-meta">{meta}</div><span class="tag {tag_cls}">{html.escape(impact)} IMPACT</span><div class="stat-grid"><div class="stat"><div class="stat-label">PREVIOUS</div><div class="stat-value">{html.escape(_fmt(row.get("previous")))}</div></div><div class="stat"><div class="stat-label">CONSENSUS</div><div class="stat-value">{html.escape(_fmt(row.get("consensus")))}</div></div><div class="stat"><div class="stat-label">ACTUAL</div><div class="stat-value">{html.escape(_fmt(row.get("actual")))}</div></div><div class="stat"><div class="stat-label">UNIT</div><div class="stat-value">{html.escape(_fmt(row.get("unit")))}</div></div></div><div class="detail-copy"><b>Market relevance:</b> Compare the release with the prior print and consensus, then monitor rates, FX, equities and commodities for the immediate response.</div><div class="source-line">Source: {html.escape(_fmt(row.get("source")))}</div></div>''',unsafe_allow_html=True)
    if row.get("source_url"): st.link_button("Open source",row["source_url"],use_container_width=True)
    st.markdown("**Related market watch**"); relevant=["S&P 500","Nifty 50","Nasdaq","DXY","Gold","Brent Crude","US 10Y","USDINR"]; m=market[market["name"].isin(relevant)]; rc=st.columns(2)
    for idx,(_,r) in enumerate(m.iterrows()):
        with rc[idx%2]: st.metric(r["name"],"—" if pd.isna(r["price"]) else f'{r["price"]:,.2f}',"—" if pd.isna(r["pct"]) else f'{r["pct"]:+.2f}%')


def render_bottom_panels(rates,events,market,central_banks_only=False,macro_only=False):
    st.markdown('<div class="section-bar"><div><div class="section-title">Market Intelligence</div><div class="section-sub">Policy, macro, event concentration and upcoming catalysts</div></div></div>',unsafe_allow_html=True)
    if central_banks_only: render_central_banks(rates); return
    if macro_only: render_macro(events); return
    c1,c2,c3,c4=st.columns([1.15,1.25,1.2,1.15],gap="medium")
    with c1: render_central_banks(rates)
    with c2: render_macro(events)
    with c3: render_impact(events)
    with c4: render_recent_upcoming(events)


def render_central_banks(rates):
    rows=[f'<div class="cb-row"><div class="row-main">{html.escape(_fmt(r["bank"]))}</div><div class="row-meta">Rate: {html.escape(_fmt(r["rate"]))} · Next: {html.escape(_fmt(r["next"]))} · {html.escape(_fmt(r["days"]))}d</div></div>' for _,r in rates.iterrows()]
    body="".join(rows) or '<div class="row-meta">No central-bank data loaded.</div>'; st.markdown('<div class="panel"><div class="panel-title">Central Bank Watch</div><div class="panel-sub">Policy-rate context and next scheduled meeting</div>'+body+'</div>',unsafe_allow_html=True)


def render_macro(events):
    macro=events[events["category"].astype(str).str.contains("Macro",case=False,na=False)].sort_values("date").head(8); rows=[f'<div class="macro-row"><div class="row-main">{html.escape(_fmt(r["event"]))}</div><div class="row-meta">{pd.Timestamp(r["date"]).strftime("%d %b")} · {html.escape(_fmt(r["country"]))} · {html.escape(_fmt(r["source"]))}</div></div>' for _,r in macro.iterrows()]; body="".join(rows) or '<div class="row-meta">No macro releases loaded.</div>'
    st.markdown('<div class="panel"><div class="panel-title">Key Macro Releases</div><div class="panel-sub">Upcoming scheduled indicators</div>'+body+'</div>',unsafe_allow_html=True)


def render_impact(events):
    if events.empty: body='<div class="row-meta">No event data.</div>'
    else:
        x=events.groupby(["category","impact"]).size().unstack(fill_value=0); cells=[]
        for category in x.index:
            total=int(x.loc[category].sum()); high=int(x.loc[category].get("High",0)); cells.append(f'<div class="heat-cell"><div class="heat-label">{html.escape(str(category))}</div><div class="heat-value">{total} events · {high} high</div></div>')
        body='<div class="heatmap">'+''.join(cells[:9])+'</div>'
    st.markdown('<div class="panel"><div class="panel-title">Event Impact Heatmap</div><div class="panel-sub">Event concentration by category</div>'+body+'</div>',unsafe_allow_html=True)


def render_recent_upcoming(events):
    now=pd.Timestamp.now(tz="Asia/Kolkata").tz_localize(None).normalize(); upcoming=events[events["date"]>=now].sort_values("date").head(8)
    rows=[f'<div class="recent-row"><div class="row-main">{pd.Timestamp(r["date"]).strftime("%d %b")} · {html.escape(_fmt(r["event"]))}</div><div class="row-meta">{html.escape(_fmt(r["country"]))} · <span class="{_impact_class(r["impact"])}">{html.escape(_fmt(r["impact"]))}</span></div></div>' for _,r in upcoming.iterrows()]; body="".join(rows) or '<div class="row-meta">No upcoming events.</div>'
    st.markdown('<div class="panel"><div class="panel-title">Recent & Upcoming</div><div class="panel-sub">Next catalysts in the event queue</div>'+body+'</div>',unsafe_allow_html=True)
