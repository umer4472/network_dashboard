import plotly.graph_objects as go
from plotly.subplots import make_subplots
import colorsys
import streamlit as st
import pandas as pd

def adjust_color_brightness(hex_color, factor):
    """Adjusts brightness of a HEX color; factor <1 = darker, >1 = lighter."""
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    l = max(0, min(1, l * factor))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"

def plot_all_together(df):
    # Ensure YEARWEEK is string
    df["YEARWEEK"] = df["YEARWEEK"].astype(str)

    # Map YEARWEEK to Month + Year for x-axis
    df["Year"] = df["YEARWEEK"].str[:4].astype(int)
    df["Week"] = df["YEARWEEK"].str[4:].str.zfill(2).astype(int)
    df["WeekStartDate"] = pd.to_datetime(df["Year"].astype(str) + df["Week"].astype(str) + '1', format='%G%V%u')
    df["MonthYear"] = df["WeekStartDate"].dt.strftime('%b %Y')
    df["Month"] = df["WeekStartDate"].dt.strftime('%b')

    # Complaints grouped
    cc_grouped = df.groupby(["YEARWEEK", "City", "Technology"], as_index=False)["ComplaintCount"].sum()

    # -----------------------------
    # Mobily color scheme
    # -----------------------------
    mobily_colors = {
        "2G": "#00B5E2",  # Accent Light Blue
        "3G": "#FF6F61",  # Coral
        "4G": "#0066CC",  # Mobily Blue
        "5G": "#0066CC"   # Mobily Blue
    }

    fig = make_subplots(
        rows=5, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.01)

    # -------------------
    # 1. Cell Availability (Line)
    # -------------------
    for tech in df["Technology"].unique():
        df_tech = df[df["Technology"] == tech]
        fig.add_trace(
            go.Scatter(
                x=df_tech["YEARWEEK"],
                y=df_tech["Cell Availability Rate %"],
                mode='lines+markers',
                customdata=df_tech[["Technology"]].values,
                hovertemplate=(
                    "<b>Technology:</b> %{customdata[0]}<br>"
                    "<b>Availability %:</b> %{y}<extra></extra>"
                ),
                name=f"{tech} Availability"
            ),
            row=1, col=1
        )

    # -------------------
    # Utility: Dynamic colors
    # -------------------
    def get_dynamic_colors(values, base_color):
        max_val = max(values)
        min_val = min(values)
        colors = []
        for v in values:
            norm = (v - min_val) / (max_val - min_val + 1e-6)
            factor = 1.0 - 0.7 * norm  # high value → darker
            colors.append(adjust_color_brightness(base_color, factor))
        return colors

    # -------------------
    # 2. Complaints (Bar)
    # -------------------
    for tech in df["Technology"].unique():
        df_tech = cc_grouped[cc_grouped["Technology"] == tech]
        colors = get_dynamic_colors(df_tech["ComplaintCount"], mobily_colors.get(tech, "#888888"))
        fig.add_trace(
            go.Bar(
                x=df_tech["YEARWEEK"],
                y=df_tech["ComplaintCount"].round(0).astype(int),
                text=df_tech["ComplaintCount"].round(0).astype(int),
                textposition="inside",
                marker=dict(color=colors),
                customdata=df_tech[["Technology", "City"]].values,
                hovertemplate=(
                    "<b>Technology:</b> %{customdata[0]}<br>"
                    "<b>City:</b> %{customdata[1]}<br>"
                    "<b>Complaints:</b> %{y}<extra></extra>"
                ),
                name=f"{tech} Complaints"
            ),
            row=2, col=1
        )

    # -------------------
    # 3. Site Unavailability (Bar)
    # -------------------
    for tech in df["Technology"].unique():
        df_tech = df[df["Technology"] == tech]
        colors = get_dynamic_colors(df_tech["Site_Unavail_TotalHours"], mobily_colors.get(tech, "#888888"))
        fig.add_trace(
            go.Bar(
                x=df_tech["YEARWEEK"],
                y=df_tech["Site_Unavail_TotalHours"].round(0).astype(int),
                text=df_tech["Site_Unavail_TotalHours"].round(0).astype(int),
                textposition="inside",
                customdata=df_tech[["Technology"]].values,
                marker=dict(color=colors),
                hovertemplate=(
                    "<b>Technology:</b> %{customdata[0]}<br>"
                    "<b>Site Unavailable Hours:</b> %{y}<extra></extra>"
                ),
                name=f"{tech} Site Unavail"
            ),
            row=3, col=1
        )

    # -------------------
    # 4. Site Count (Bar)
    # -------------------
    for tech in df["Technology"].unique():
        df_tech = df[df["Technology"] == tech]
        colors = get_dynamic_colors(df_tech["siteCount"], mobily_colors.get(tech, "#888888"))
        fig.add_trace(
            go.Bar(
                x=df_tech["YEARWEEK"],
                y=df_tech["siteCount"].round(0).astype(int),
                text=df_tech["siteCount"].round(0).astype(int),
                textposition="inside",
                customdata=df_tech[["Technology"]].values,
                marker=dict(color=colors),
                hovertemplate=(
                    "<b>Technology:</b> %{customdata[0]}<br>"
                    "<b>Site Count:</b> %{y}<extra></extra>"
                ),
                name=f"{tech} Site Count"
            ),
            row=4, col=1
        )

    # -------------------
    # 5. Fault Types (Bar stacked by FaultType)
    # -------------------
    fault_type_columns = [
        "ClientFarEndFaults", "DecomissionedFaults", "EnvironmentFaults", "HardwareFaults",
        "ISPFaults", "LinkFaults", "MgmtLossFaults", "MDTViolationFaults",
        "OSPFaults", "PerformanceFaults", "PowerFaults", "SoftwareFaults"
    ]
    fault_type_columns = [col for col in fault_type_columns if col in df.columns]

    # Fixed distinct colors for fault types
    palette = [
        "#636EFA", "#EF553B", "#00CC96", "#AB63FA",
        "#FFA15A", "#19D3F3", "#FF6692", "#B6E880",
        "#FF97FF", "#FECB52", "#8C564B", "#E377C2"
    ]
    fault_color_map = {fault: palette[i % len(palette)] for i, fault in enumerate(fault_type_columns)}

    # Aggregate fault counts across all technologies (sum)
    df_faults = df.groupby("YEARWEEK")[fault_type_columns].sum().reset_index()

    # Add traces
    for fault in fault_type_columns:
        fig.add_trace(
            go.Bar(
                x=df_faults["YEARWEEK"],
                y=df_faults[fault],
                name=fault,
                marker=dict(color=fault_color_map[fault]),
                hovertemplate=f"<b>Fault:</b> {fault}<br>Count: %{{y}}<extra></extra>"
            ),
            row=5, col=1
        )

    # --- Layout adjustments ---
    unique_weeks = df["YEARWEEK"].unique()
    month_year_first_occurrence = df.drop_duplicates("MonthYear").set_index("MonthYear")["YEARWEEK"]

    ticktext = []
    for yw in unique_weeks:
        my = df.loc[df["YEARWEEK"] == yw, "MonthYear"].values[0]
        if month_year_first_occurrence[my] == yw:
            ticktext.append(my)
        else:
            ticktext.append("")

    fig.update_layout(
        height=900,
        width=1700,
        showlegend=True,
        barmode='stack',
        yaxis1=dict(title="Cell Availability Rate %"),
        yaxis2=dict(title="Complaints Count"),
        yaxis3=dict(title="Site Unavail Total Hours"),
        yaxis4=dict(title="Site Count"),
        yaxis5=dict(title="SIR")
    )

    fig.update_xaxes(
        tickvals=unique_weeks,
        ticktext=ticktext,
        row=5, col=1
    )

    st.plotly_chart(fig, use_container_width=True)
