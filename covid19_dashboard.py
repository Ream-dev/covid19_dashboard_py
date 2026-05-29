import dash
from dash import dcc, html, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
 
# ── App init ────────────────────────────────────────────────────────────────
app = dash.Dash(__name__, title="COVID-19 Global Dashboard")
 
# ════════════════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════════════════
 
# --- Global summary metrics ---
metrics = {
    "Total Cases":     ("704.8M", "+0.3% this week",  "#2563eb"),
    "Total Deaths":    ("7.01M",  "CFR: 1.0%",        "#dc2626"),
    "Recovered":       ("676.1M", "Recovery rate 96%","#16a34a"),
    "Active Cases":    ("21.7M",  "+1.2% this week",  "#d97706"),
    "Vaccinated":      ("5.55B",  "70% of world",     "#7c3aed"),
}
 
# --- Monthly cases trend ---
months = [
    "Jan 20","Apr 20","Jul 20","Oct 20",
    "Jan 21","Apr 21","Jul 21","Oct 21",
    "Jan 22","Apr 22","Jul 22","Oct 22",
    "Jan 23","Apr 23","Jul 23","Oct 23",
]
cases_monthly = [0.5,1.2,2.0,4.2,3.8,5.6,8.3,10.1,
                 19.8,14.2,9.5,15.2,39.5,22.1,11.4,8.2]
 
# --- Outcomes (doughnut) ---
outcomes      = ["Recovered", "Active", "Deaths"]
outcome_vals  = [96.0, 3.0, 1.0]
outcome_colors= ["#16a34a", "#6b7280", "#dc2626"]
 
# --- Wave bar ---
quarters = ["Q1 20","Q2 20","Q3 20","Q4 20",
            "Q1 21","Q2 21","Q3 21","Q4 21",
            "Q1 22","Q2 22","Q3 22","Q4 22"]
wave_data = [1.2,3.4,6.8,14.2,12.1,16.5,24.3,28.7,89.4,46.2,38.1,30.5]
wave_colors = (["#1d4ed8"]*3 + ["#92400e"]*2 +
               ["#991b1b"]*3 + ["#6d28d9"]*4)
 
# --- Vaccination by region ---
regions  = ["Europe","North America","South America",
            "East Asia","South Asia","Middle East","Africa"]
vax_pct  = [74, 70, 65, 79, 54, 60, 28]
vax_cols = ["#1d4ed8" if v >= 70 else "#d97706" if v >= 55 else "#dc2626"
            for v in vax_pct]
 
# --- CFR by age ---
age_groups = ["0–9","10–19","20–29","30–39","40–49",
              "50–59","60–69","70–79","80+"]
cfr_vals   = [0.001,0.003,0.01,0.08,0.18,0.6,1.9,5.6,14.8]
 
# --- Countries table (Top 10 + Cambodia) ---
countries_data = pd.DataFrame([
    dict(rank=1,  country="🇺🇸 United States", cases="103.4M", deaths="1.12M", cfr="1.1%", vax="70%", status="Endemic"),
    dict(rank=2,  country="🇨🇳 China",          cases="99.2M",  deaths="122K",  cfr="0.1%", vax="90%", status="Endemic"),
    dict(rank=3,  country="🇮🇳 India",          cases="44.7M",  deaths="530K",  cfr="1.2%", vax="68%", status="Endemic"),
    dict(rank=4,  country="🇫🇷 France",         cases="38.9M",  deaths="162K",  cfr="0.4%", vax="78%", status="Endemic"),
    dict(rank=5,  country="🇩🇪 Germany",        cases="38.2M",  deaths="174K",  cfr="0.5%", vax="77%", status="Endemic"),
    dict(rank=6,  country="🇧🇷 Brazil",         cases="37.5M",  deaths="702K",  cfr="1.9%", vax="81%", status="Endemic"),
    dict(rank=7,  country="🇰🇷 South Korea",    cases="32.9M",  deaths="35K",   cfr="0.1%", vax="87%", status="Endemic"),
    dict(rank=8,  country="🇬🇧 United Kingdom", cases="24.8M",  deaths="232K",  cfr="0.9%", vax="74%", status="Endemic"),
    dict(rank=9,  country="🇮🇹 Italy",          cases="26.1M",  deaths="196K",  cfr="0.8%", vax="80%", status="Endemic"),
    dict(rank=10, country="🇷🇺 Russia",         cases="23.2M",  deaths="400K",  cfr="1.7%", vax="52%", status="Active"),
    dict(rank=11, country="🇰🇭 Cambodia",       cases="138,646",deaths="3,056", cfr="2.2%", vax="90%", status="Endemic"),
])
 
# ── Cambodia-specific data ────────────────────────────────────────────────
khm_months = [
    "Jan 20","Apr 20","Jul 20","Oct 20",
    "Jan 21","Apr 21","Jul 21","Oct 21",
    "Jan 22","Apr 22","Jul 22","Oct 22",
    "Jan 23","Apr 23","Jul 23","Oct 23",
]
khm_cases = [0, 0, 22, 290, 480, 12500, 8200, 3100, 4800, 2100, 900, 410, 220, 140, 90, 60]
 
khm_vax_labels = ["Jan 21","Apr 21","Jul 21","Oct 21","Jan 22","Apr 22","Jul 22","Oct 22","Jan 23"]
khm_vax_doses  = [0.05, 0.8, 4.2, 9.5, 13.2, 15.8, 17.1, 17.9, 18.1]
 
khm_provinces   = ["Phnom Penh","Siem Reap","Preah Sihanouk","Kandal",
                   "Battambang","Kampong Cham","Prey Veng","Banteay Meanchey"]
khm_prov_cases  = [62000, 14000, 11500, 9800, 7200, 6100, 4900, 3800]
khm_prov_colors = ["#dc2626","#d97706","#d97706","#2563eb",
                   "#2563eb","#16a34a","#16a34a","#16a34a"]
 
khm_metrics = {
    "Total Cases":   ("138,646", "As of early 2024",    "#2563eb"),
    "Total Deaths":  ("3,056",   "CFR: 2.2%",           "#dc2626"),
    "Recovered":     ("135,590", "Recovery rate 97.8%", "#16a34a"),
    "Vaccinated":    ("18.1M",   "~90% of population",  "#7c3aed"),
    "Booster Doses": ("9.8M",    "3rd dose coverage",   "#d97706"),
}
 
# --- Variants stacked bar ---
q_labels = ["Q1 20","Q2 20","Q3 20","Q4 20","Q1 21","Q2 21",
            "Q3 21","Q4 21","Q1 22","Q2 22","Q3 22","Q4 22","Q1 23"]
variants = {
    "Original":        [100,100,95,80,50,20, 5, 2, 0, 0, 0, 0, 0],
    "Alpha":           [  0,  0, 5,18,42,30, 5, 1, 0, 0, 0, 0, 0],
    "Delta":           [  0,  0, 0, 2, 8,50,90,60, 5, 2, 1, 0, 0],
    "Omicron BA.1":    [  0,  0, 0, 0, 0, 0, 0,37,90,35,10, 5, 3],
    "Omicron BA.4/5+": [  0,  0, 0, 0, 0, 0, 0, 0, 5,63,89,95,97],
}
variant_colors = ["#1d4ed8","#92400e","#991b1b","#6d28d9","#15803d"]
 
# ════════════════════════════════════════════════════════════════════════════
# FIGURES
# ════════════════════════════════════════════════════════════════════════════
PLOT_BG   = "#ffffff"
PAPER_BG  = "#ffffff"
FONT_COL  = "#374151"
GRID_COL  = "rgba(0,0,0,0.07)"
 
def base_layout(**kw):
    defaults = dict(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(family="system-ui, sans-serif", color=FONT_COL, size=11),
        margin=dict(l=40, r=20, t=20, b=40),
    )
    defaults.update(kw)
    return defaults
 
 
# 1. Monthly trend line
fig_trend = go.Figure(go.Scatter(
    x=months, y=cases_monthly, mode="lines+markers",
    line=dict(color="#2563eb", width=2),
    marker=dict(size=4),
    fill="tozeroy", fillcolor="rgba(37,99,235,0.08)",
    name="New cases (M)",
    hovertemplate="%{x}<br>%{y:.1f}M cases<extra></extra>",
))
fig_trend.update_layout(**base_layout(),
    xaxis=dict(showgrid=False, tickangle=45),
    yaxis=dict(gridcolor=GRID_COL, ticksuffix="M"),
    showlegend=False,
)
 
# 2. Outcome doughnut
fig_donut = go.Figure(go.Pie(
    labels=outcomes, values=outcome_vals,
    marker_colors=outcome_colors,
    hole=0.65, textinfo="label+percent",
    hovertemplate="%{label}: %{value}%<extra></extra>",
))
fig_donut.update_layout(**base_layout(margin=dict(l=10,r=10,t=10,b=10)),
    showlegend=False,
)
 
# 3. Waves bar
fig_waves = go.Figure(go.Bar(
    x=quarters, y=wave_data,
    marker_color=wave_colors,
    marker=dict(cornerradius=3),
    hovertemplate="%{x}<br>%{y:.1f}M cases<extra></extra>",
))
fig_waves.update_layout(**base_layout(),
    xaxis=dict(showgrid=False, tickangle=45),
    yaxis=dict(gridcolor=GRID_COL, ticksuffix="M"),
    showlegend=False,
)
 
# 4. Vaccination horizontal bar
fig_vax = go.Figure(go.Bar(
    x=vax_pct, y=regions, orientation="h",
    marker_color=vax_cols,
    marker=dict(cornerradius=3),
    hovertemplate="%{y}: %{x}%<extra></extra>",
))
fig_vax.update_layout(**base_layout(),
    xaxis=dict(range=[0,100], ticksuffix="%", gridcolor=GRID_COL),
    yaxis=dict(showgrid=False),
    showlegend=False,
)
 
# 5. CFR by age (log scale)
cfr_colors = ["#16a34a" if v < 0.1 else "#d97706" if v < 1 else "#dc2626"
              for v in cfr_vals]
fig_cfr = go.Figure(go.Bar(
    x=age_groups, y=cfr_vals,
    marker_color=cfr_colors,
    marker=dict(cornerradius=3),
    hovertemplate="%{x}: %{y}% CFR<extra></extra>",
))
fig_cfr.update_layout(**base_layout(),
    xaxis=dict(showgrid=False),
    yaxis=dict(type="log", gridcolor=GRID_COL, ticksuffix="%"),
    showlegend=False,
)
 
# 6. Variants stacked bar
fig_variants = go.Figure()
for (name, data), color in zip(variants.items(), variant_colors):
    fig_variants.add_trace(go.Bar(
        name=name, x=q_labels, y=data,
        marker_color=color,
        hovertemplate=f"{name}: %{{y}}%<extra></extra>",
    ))
fig_variants.update_layout(**base_layout(),
    barmode="stack",
    xaxis=dict(showgrid=False, tickangle=45),
    yaxis=dict(gridcolor=GRID_COL, ticksuffix="%", range=[0,100]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
)
 
# ── Cambodia figures ─────────────────────────────────────────────────────
 
# 7. Cambodia monthly cases line
fig_khm_trend = go.Figure(go.Scatter(
    x=khm_months, y=khm_cases, mode="lines+markers",
    line=dict(color="#dc2626", width=2),
    marker=dict(size=4, color="#dc2626"),
    fill="tozeroy", fillcolor="rgba(220,38,38,0.08)",
    hovertemplate="%{x}<br>%{y:,} cases<extra></extra>",
))
fig_khm_trend.update_layout(**base_layout(),
    xaxis=dict(showgrid=False, tickangle=45),
    yaxis=dict(gridcolor=GRID_COL, tickformat=","),
    showlegend=False,
)
 
# 8. Cambodia vaccination doses line
fig_khm_vax = go.Figure(go.Scatter(
    x=khm_vax_labels, y=khm_vax_doses, mode="lines+markers",
    line=dict(color="#7c3aed", width=2),
    marker=dict(size=5, color="#7c3aed"),
    fill="tozeroy", fillcolor="rgba(124,58,237,0.08)",
    hovertemplate="%{x}<br>%{y:.1f}M doses<extra></extra>",
))
fig_khm_vax.update_layout(**base_layout(),
    xaxis=dict(showgrid=False, tickangle=45),
    yaxis=dict(gridcolor=GRID_COL, ticksuffix="M"),
    showlegend=False,
)
 
# 9. Cambodia cases by province bar
fig_khm_prov = go.Figure(go.Bar(
    x=khm_prov_cases, y=khm_provinces,
    orientation="h",
    marker_color=khm_prov_colors,
    marker=dict(cornerradius=3),
    hovertemplate="%{y}<br>%{x:,} cases<extra></extra>",
))
fig_khm_prov.update_layout(**base_layout(),
    xaxis=dict(gridcolor=GRID_COL, tickformat=","),
    yaxis=dict(showgrid=False, autorange="reversed"),
    showlegend=False,
)
 
# ════════════════════════════════════════════════════════════════════════════
# STYLES
# ════════════════════════════════════════════════════════════════════════════
CARD = {
    "background": "#ffffff",
    "borderRadius": "12px",
    "border": "1px solid #e5e7eb",
    "padding": "16px 20px",
}
METRIC_CARD = {
    "background": "#f9fafb",
    "borderRadius": "10px",
    "padding": "16px",
    "flex": "1",
    "minWidth": "120px",
}
 
# ════════════════════════════════════════════════════════════════════════════
# LAYOUT
# ════════════════════════════════════════════════════════════════════════════
def metric_box(label, value, delta, color):
    return html.Div([
        html.P(label, style={"margin":"0 0 6px","fontSize":"12px","color":"#6b7280"}),
        html.P(value, style={"margin":"0","fontSize":"24px","fontWeight":"500","color":"#111827"}),
        html.P(delta, style={"margin":"4px 0 0","fontSize":"11px","color":color}),
    ], style=METRIC_CARD)
 
app.layout = html.Div([
 
    # ── Header ───────────────────────────────────────────────────────────
    html.Div([
        html.H1("🦠 COVID-19 Global Dashboard",
                style={"margin":"0 0 4px","fontSize":"26px","fontWeight":"600","color":"#111827"}),
        html.P("Comprehensive global tracking — cases, deaths, recoveries, vaccination & regional breakdowns · Data as of 2024",
               style={"margin":"0","fontSize":"13px","color":"#6b7280"}),
    ], style={"marginBottom":"24px"}),
 
    # ── Metrics row ───────────────────────────────────────────────────────
    html.P("GLOBAL SUMMARY", style={"margin":"0 0 10px","fontSize":"11px",
           "fontWeight":"600","letterSpacing":"0.08em","color":"#9ca3af"}),
    html.Div([
        metric_box(label, val, delta, color)
        for label, (val, delta, color) in metrics.items()
    ], style={"display":"flex","gap":"10px","flexWrap":"wrap","marginBottom":"24px"}),
 
    # ── Row 1: trend + donut ──────────────────────────────────────────────
    html.Div([
        html.Div([
            html.P("Monthly new cases (2020–2023)", style={"margin":"0 0 4px","fontWeight":"500","fontSize":"14px"}),
            html.P("Global confirmed cases per month", style={"margin":"0 0 12px","fontSize":"12px","color":"#6b7280"}),
            dcc.Graph(figure=fig_trend, config={"displayModeBar":False}, style={"height":"220px"}),
        ], style={**CARD, "flex":"1", "minWidth":"280px"}),
 
        html.Div([
            html.P("Deaths vs recoveries", style={"margin":"0 0 4px","fontWeight":"500","fontSize":"14px"}),
            html.P("Cumulative global outcome split", style={"margin":"0 0 12px","fontSize":"12px","color":"#6b7280"}),
            dcc.Graph(figure=fig_donut, config={"displayModeBar":False}, style={"height":"220px"}),
        ], style={**CARD, "flex":"1", "minWidth":"200px"}),
    ], style={"display":"flex","gap":"12px","marginBottom":"12px","flexWrap":"wrap"}),
 
    # ── Wave chart ────────────────────────────────────────────────────────
    html.Div([
        html.P("Daily cases by major wave (quarterly totals)", style={"margin":"0 0 4px","fontWeight":"500","fontSize":"14px"}),
        html.P("Illustrating the four major global COVID-19 waves  🔵 Wave 1  🟤 Wave 2  🔴 Delta  🟣 Omicron",
               style={"margin":"0 0 12px","fontSize":"12px","color":"#6b7280"}),
        dcc.Graph(figure=fig_waves, config={"displayModeBar":False}, style={"height":"220px"}),
    ], style={**CARD, "marginBottom":"12px"}),
 
    # ── Row 2: vax + CFR ──────────────────────────────────────────────────
    html.Div([
        html.Div([
            html.P("Vaccination progress by region", style={"margin":"0 0 4px","fontWeight":"500","fontSize":"14px"}),
            html.P("% of population fully vaccinated", style={"margin":"0 0 12px","fontSize":"12px","color":"#6b7280"}),
            dcc.Graph(figure=fig_vax, config={"displayModeBar":False}, style={"height":"240px"}),
        ], style={**CARD, "flex":"1", "minWidth":"280px"}),
 
        html.Div([
            html.P("Case fatality rate by age group", style={"margin":"0 0 4px","fontWeight":"500","fontSize":"14px"}),
            html.P("CFR rises sharply in older populations (log scale)", style={"margin":"0 0 12px","fontSize":"12px","color":"#6b7280"}),
            dcc.Graph(figure=fig_cfr, config={"displayModeBar":False}, style={"height":"240px"}),
        ], style={**CARD, "flex":"1", "minWidth":"280px"}),
    ], style={"display":"flex","gap":"12px","marginBottom":"12px","flexWrap":"wrap"}),
 
    # ── Countries table ───────────────────────────────────────────────────
    html.Div([
        html.Div([
            html.P("Top 10 most-affected countries", style={"margin":"0","fontWeight":"500","fontSize":"14px"}),
            html.P("Sorted by total confirmed cases", style={"margin":"0","fontSize":"12px","color":"#6b7280"}),
        ], style={"display":"flex","justifyContent":"space-between","alignItems":"center","marginBottom":"12px"}),
        dash_table.DataTable(
            data=countries_data.to_dict("records"),
            columns=[{"name": c.replace("_"," ").title(), "id": c}
                     for c in countries_data.columns],
            style_table={"overflowX":"auto"},
            style_cell={"fontFamily":"system-ui,sans-serif","fontSize":"13px",
                        "padding":"10px 14px","border":"none","color":"#111827"},
            style_header={"background":"#f3f4f6","fontWeight":"600",
                          "fontSize":"11px","color":"#6b7280","border":"none"},
            style_data_conditional=[
                {"if":{"filter_query":"{status} = Endemic"},
                 "color":"#15803d"},
                {"if":{"filter_query":"{status} = Active"},
                 "color":"#d97706"},
                {"if":{"row_index":"odd"},"background":"#f9fafb"},
            ],
        ),
    ], style={**CARD, "marginBottom":"12px"}),
 
    # ── Variants chart ────────────────────────────────────────────────────
    html.Div([
        html.P("Variants of concern — case share over time (%)", style={"margin":"0 0 4px","fontWeight":"500","fontSize":"14px"}),
        html.P("Dominant global variant share by quarter", style={"margin":"0 0 12px","fontSize":"12px","color":"#6b7280"}),
        dcc.Graph(figure=fig_variants, config={"displayModeBar":False}, style={"height":"260px"}),
    ], style={**CARD, "marginBottom":"12px"}),
 
    # ── Cambodia section ──────────────────────────────────────────────────
    html.P("🇰🇭 CAMBODIA SPOTLIGHT", style={"margin":"24px 0 10px","fontSize":"11px",
           "fontWeight":"600","letterSpacing":"0.08em","color":"#9ca3af"}),
 
    # Cambodia metric cards
    html.Div([
        metric_box(label, val, delta, color)
        for label, (val, delta, color) in khm_metrics.items()
    ], style={"display":"flex","gap":"10px","flexWrap":"wrap","marginBottom":"12px"}),
 
    # Cambodia trend + vaccination
    html.Div([
        html.Div([
            html.P("Monthly confirmed cases — Cambodia", style={"margin":"0 0 4px","fontWeight":"500","fontSize":"14px"}),
            html.P("Jan 2020 – Oct 2023 · Peak during Delta wave (Apr–May 2021)", style={"margin":"0 0 12px","fontSize":"12px","color":"#6b7280"}),
            dcc.Graph(figure=fig_khm_trend, config={"displayModeBar":False}, style={"height":"220px"}),
        ], style={**CARD, "flex":"1", "minWidth":"280px"}),
 
        html.Div([
            html.P("Vaccination rollout — doses administered", style={"margin":"0 0 4px","fontWeight":"500","fontSize":"14px"}),
            html.P("Cambodia achieved 90% coverage — one of SEA's highest rates", style={"margin":"0 0 12px","fontSize":"12px","color":"#6b7280"}),
            dcc.Graph(figure=fig_khm_vax, config={"displayModeBar":False}, style={"height":"220px"}),
        ], style={**CARD, "flex":"1", "minWidth":"280px"}),
    ], style={"display":"flex","gap":"12px","marginBottom":"12px","flexWrap":"wrap"}),
 
    # Cambodia province bar
    html.Div([
        html.P("Cases by province (top 8)", style={"margin":"0 0 4px","fontWeight":"500","fontSize":"14px"}),
        html.P("Phnom Penh accounted for ~45% of all confirmed cases in Cambodia",
               style={"margin":"0 0 12px","fontSize":"12px","color":"#6b7280"}),
        dcc.Graph(figure=fig_khm_prov, config={"displayModeBar":False}, style={"height":"260px"}),
    ], style={**CARD, "marginBottom":"12px"}),
 
    # ── Footer ────────────────────────────────────────────────────────────
    html.P("ℹ️  Data sourced from WHO, Johns Hopkins CSSE, and Our World in Data. "
           "Figures reflect cumulative totals as of early 2024. CFR = Case Fatality Rate.",
           style={"fontSize":"11px","color":"#9ca3af","borderTop":"1px solid #e5e7eb",
                  "paddingTop":"12px","marginTop":"8px"}),
 
], style={"maxWidth":"1100px","margin":"0 auto","padding":"32px 20px",
          "fontFamily":"system-ui, -apple-system, sans-serif","background":"#f3f4f6",
          "minHeight":"100vh"})
 
# ════════════════════════════════════════════════════════════════════════════
# RUN
# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Starting COVID-19 Dashboard...")
    print("Open your browser at: http://127.0.0.1:8050")
    app.run(debug=True, host="0.0.0.0", port=8050)
 