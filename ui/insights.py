import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ui import components as c
from ui import sample_data as d

PRIMARY, AMBER, TEXT = "#0F5C4D", "#E0A126", "#1A1F1C"


def _layout(fig: go.Figure, height: int) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT, size=13),
    )
    return fig


def _allocation_bar() -> go.Figure:
    rows = sorted(d.ALLOCATIONS, key=lambda r: r["amount_b"])  # largest ends on top
    fig = go.Figure(go.Bar(
        x=[r["amount_b"] for r in rows],
        y=[r["sector"] for r in rows],
        orientation="h",
        marker_color=PRIMARY,
        text=[f'KSh {r["amount_b"]:.1f}B · {r["share"]}%' for r in rows],
        textposition="outside",
        cliponaxis=False,
        hoverinfo="skip",
    ))
    fig.update_xaxes(visible=False, range=[0, 4.2])
    fig.update_yaxes(showgrid=False)
    fig.update_layout(margin=dict(l=0, r=100, t=8, b=8))
    return _layout(fig, 330)


def _split_donut() -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=[f"{n} · {s}%" for n, _, s in d.SPLIT],
        values=[s for _, _, s in d.SPLIT],
        hole=0.72,
        sort=False,
        marker=dict(colors=[PRIMARY, AMBER]),
        textinfo="none",
        hoverinfo="skip",
    ))
    fig.add_annotation(text=f"<b>KSh {d.TOTAL_BUDGET_B:.1f}B</b><br>Total budget",
                       showarrow=False, font=dict(size=15))
    fig.update_layout(margin=dict(l=0, r=0, t=8, b=8),
                      legend=dict(orientation="h", y=-0.05))
    return _layout(fig, 330)


def render() -> None:
    c.page_header("Follow the allocations", "Budget Insights",
                  "See the priorities in the budget, and the limits of what the numbers can tell us.")
    c.banner(d.NOTE)

    left, right = st.columns([3, 2])
    with left:
        with st.container(border=True):
            c.render('<div class="cl-h3">Where is the budget allocated?</div>'
                     '<div class="cl-muted">Sector allocations · KSh billions</div>')
            st.plotly_chart(_allocation_bar(), width="stretch", config={"displayModeBar": False})
            st.caption("Illustrative figures · verified from page 18")
    with right:
        with st.container(border=True):
            c.render('<div class="cl-h3">How is the budget split?</div>'
                     '<div class="cl-muted">Recurrent and development spending</div>')
            st.plotly_chart(_split_donut(), width="stretch", config={"displayModeBar": False})
            st.caption("Illustrative figures · verified from page 12")

    c.h2("Largest allocations")
    table = pd.DataFrame(
        [{"Sector": r["sector"], "Allocation": f'KSh {r["amount_b"]:.1f}B',
          "Budget share": f'{r["share"]}%', "Source": f'Page {r["page"]}'}
         for r in sorted(d.ALLOCATIONS, key=lambda r: -r["amount_b"])]
        + [{"Sector": "Total", "Allocation": f"KSh {d.TOTAL_BUDGET_B:.1f}B",
            "Budget share": "100%", "Source": "Page 18"}]
    )
    st.dataframe(table, hide_index=True, width="stretch")

    c.banner("Data limitations: allocations are planned amounts, not actual spending. "
             "These charts do not assess service quality, project completion or value for money.",
             kind="info")
    c.footer()
