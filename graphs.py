gateway-dashboard/graphs.py

import pandas as pd
import plotly.graph_objects as go

# ------------------------------------------------------
# FILE LOCATION
# ------------------------------------------------------

FILE = "Data/Gateway_Graphs.xlsx"

# ------------------------------------------------------
# CONSTRUCTION MATERIALS DIVERTED
# ------------------------------------------------------

construction = pd.read_excel(
    FILE,
    sheet_name="C&D Diversion Data"
)

construction = construction[
    ["Material", "Tons"]
].copy()

construction["Tons"] = pd.to_numeric(
    construction["Tons"],
    errors="coerce"
)

construction = construction.dropna(
    subset=["Material", "Tons"]
)

# Keep only Metal and larger.
metal_threshold = construction.loc[
    construction["Material"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("metal"),
    "Tons"
].iloc[0]

construction = construction[
    construction["Tons"] >= metal_threshold
].copy()

# Short, readable labels.
construction["Display Material"] = construction["Material"].replace({
    "Alternate Daily Cover (ADC)": "Alternate Daily Cover",
    "Mixed Recyclables": "Mixed Recyclables",
    "Clean Drywall": "Clean Drywall",
    "Drywall Clean": "Clean Drywall"
})

# Sort largest at top.
construction = construction.sort_values(
    "Tons",
    ascending=True
)

construction_fig = go.Figure()

construction_fig.add_trace(
    go.Bar(
        x=construction["Tons"],
        y=construction["Display Material"],
        orientation="h",

        marker=dict(
            color="#0B6E4F"
        ),

        text=construction["Tons"].map(
            lambda value: f"{value:,.0f}"
        ),

        textposition="outside",

        textfont=dict(
            family="Arial, sans-serif",
            size=12,
            color="#343743"
        ),

        cliponaxis=False,

        customdata=construction[["Material"]],

        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "%{x:,.2f} tons diverted"
            "<extra></extra>"
        )
    )
)

construction_fig.update_layout(
    title=dict(
        text=(
            "<b>Major Materials Diverted</b>"
            "<br>"
            "<span style='font-size:12px;color:#747B8D;'>"
            "Material streams at or above metal by weight"
            "</span>"
        ),
        x=0,
        xanchor="left",
        y=0.92,
        yanchor="top",
        font=dict(
            family="Arial, sans-serif",
            size=19,
            color="#343743"
        )
    ),

    height=300,

    margin=dict(
        l=145,
        r=70,
        t=80,
        b=48
    ),

    bargap=0.35,

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        family="Arial, sans-serif",
        color="#343743"
    ),

    showlegend=False,

    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#D8DCE5",
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#343743"
        )
    )
)

construction_fig.update_xaxes(
    title=None,

    tickformat=",.0f",

    tickfont=dict(
        size=11,
        color="#747B8D"
    ),

    showgrid=True,
    gridcolor="rgba(116,123,141,0.13)",

    showline=False,
    zeroline=False,

    range=[
        0,
        construction["Tons"].max() * 1.18
    ],

    fixedrange=True
)

construction_fig.update_yaxes(
    title=None,

    tickfont=dict(
        family="Arial, sans-serif",
        size=11,
        color="#5E6878"
    ),

    showgrid=False,
    showline=False,
    ticks="",

    automargin=False,

    fixedrange=True
)







import pandas as pd
import plotly.graph_objects as go


# ------------------------------------------------------
# FILE LOCATION
# ------------------------------------------------------

TRACKER_FILE = "Data/ZWR_C1_update.xlsx"


# ------------------------------------------------------
# LOAD RAW HAUL RECORDS
# ------------------------------------------------------

# The actual column headings begin on Excel row 8,
# so header=7 tells pandas to use that row as the header.
haul_data = pd.read_excel(
    TRACKER_FILE,
    sheet_name="Worksheet",
    header=7
)


# ------------------------------------------------------
# CLEAN REQUIRED COLUMNS
# ------------------------------------------------------

required_columns = [
    "Haul Date",
    "GM Reused Tons",
    "GM Recycled Tons",
    "GM Disposed Tons",
    "GM Total Tons"
]

haul_data = haul_data[required_columns].copy()

haul_data["Haul Date"] = pd.to_datetime(
    haul_data["Haul Date"],
    errors="coerce"
)

ton_columns = [
    "GM Reused Tons",
    "GM Recycled Tons",
    "GM Disposed Tons",
    "GM Total Tons"
]

for column in ton_columns:
    haul_data[column] = pd.to_numeric(
        haul_data[column],
        errors="coerce"
    ).fillna(0)

haul_data = haul_data.dropna(
    subset=["Haul Date"]
)


# ------------------------------------------------------
# USE THE ENTIRE CONSTRUCTION PROJECT
# ------------------------------------------------------

# Create one month value for every haul record.
haul_data["Month"] = (
    haul_data["Haul Date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

# Keep every valid haul record in the workbook.
project_data = haul_data.copy()


# ------------------------------------------------------
# AGGREGATE PROJECT DATA BY MONTH
# ------------------------------------------------------

monthly_diversion = (
    project_data
    .groupby("Month", as_index=False)
    .agg(
        Reused_Tons=("GM Reused Tons", "sum"),
        Recycled_Tons=("GM Recycled Tons", "sum"),
        Disposed_Tons=("GM Disposed Tons", "sum"),
        Total_Tons=("GM Total Tons", "sum")
    )
)

# Create a complete monthly timeline so months do not disappear.
first_month = monthly_diversion["Month"].min()
last_month = monthly_diversion["Month"].max()

all_months = pd.DataFrame({
    "Month": pd.date_range(
        start=first_month,
        end=last_month,
        freq="MS"
    )
})

monthly_diversion = all_months.merge(
    monthly_diversion,
    on="Month",
    how="left"
)

monthly_diversion[
    [
        "Reused_Tons",
        "Recycled_Tons",
        "Disposed_Tons",
        "Total_Tons"
    ]
] = monthly_diversion[
    [
        "Reused_Tons",
        "Recycled_Tons",
        "Disposed_Tons",
        "Total_Tons"
    ]
].fillna(0)

monthly_diversion["Diverted_Tons"] = (
    monthly_diversion["Reused_Tons"]
    + monthly_diversion["Recycled_Tons"]
)

monthly_diversion["Diversion_Rate"] = (
    monthly_diversion["Diverted_Tons"]
    / monthly_diversion["Total_Tons"]
    * 100
)

# Do not show months with no haul records as 0% diversion.
monthly_diversion.loc[
    monthly_diversion["Total_Tons"] == 0,
    "Diversion_Rate"
] = None


# ------------------------------------------------------
# CALCULATE FULL-PROJECT DIVERSION RATE
# ------------------------------------------------------

project_total_tons = monthly_diversion[
    "Total_Tons"
].sum()

project_diverted_tons = monthly_diversion[
    "Diverted_Tons"
].sum()

project_disposed_tons = monthly_diversion[
    "Disposed_Tons"
].sum()

project_diversion_rate = (
    project_diverted_tons
    / project_total_tons
    * 100
)


# ------------------------------------------------------
# CREATE FULL-PROJECT HERO GRAPH
# ------------------------------------------------------

diversion_rate_fig = go.Figure()

diversion_rate_fig.add_trace(
    go.Scatter(
        x=monthly_diversion["Month"],
        y=monthly_diversion["Diversion_Rate"],

        mode="lines+markers",

        name="Monthly diversion",

        line=dict(
            color="#0B6E4F",
            width=3.5
        ),

        marker=dict(
            color="#0B6E4F",
            size=8,
            line=dict(
                color="white",
                width=2
            )
        ),

        customdata=monthly_diversion[
            [
                "Diverted_Tons",
                "Disposed_Tons",
                "Total_Tons"
            ]
        ],

        hovertemplate=(
            "<b>%{x|%B %Y}</b><br>"
            "Diversion rate: %{y:.1f}%<br>"
            "Diverted: %{customdata[0]:,.1f} tons<br>"
            "Landfilled: %{customdata[1]:,.1f} tons<br>"
            "Total tracked: %{customdata[2]:,.1f} tons"
            "<extra></extra>"
        ),

        connectgaps=False
    )
)


# ------------------------------------------------------
# FULL-PROJECT WEIGHTED RATE LINE
# ------------------------------------------------------

diversion_rate_fig.add_hline(
    y=project_diversion_rate,
    line_dash="dash",
    line_width=2.0,
    line_color="#64748B"
)


diversion_rate_fig.add_annotation(
    x=monthly_diversion["Month"].iloc[-2],
    y=project_diversion_rate,

    text=(
        f"<b>Project average</b><br>"
        f"{project_diversion_rate:.1f}%"
    ),

    showarrow=False,

    xanchor="left",
    yanchor="bottom",

    font=dict(
        family="Arial, sans-serif",
        size=11,
        color="#64748B"
    ),

    bgcolor="rgba(255,255,255,0.90)",
    bordercolor="rgba(100,116,139,0.25)",
    borderwidth=1,
    borderpad=4
)

# ------------------------------------------------------
# GRAPH LAYOUT
# ------------------------------------------------------




# MAKE THE GRAPH SHORTER so it does not spill into the next section
diversion_rate_fig.update_layout(
    height=330,
    margin=dict(
        l=55,
        r=20,
        t=80,
        b=55
    ),
    autosize=True
)

# Keep the x-axis compact
diversion_rate_fig.update_xaxes(
    automargin=True,
    title=None
)

diversion_rate_fig.update_yaxes(
    automargin=True,
    title_text="Diversion rate",
    range=[0, 105]
)



# ------------------------------------------------------
# X AXIS
# ------------------------------------------------------

diversion_rate_fig.update_xaxes(
    title=None,

    type="date",

    # Show approximately one label every three months.
    dtick="M3",
    tickformat="%b<br>%Y",

    tickfont=dict(
        family="Arial, sans-serif",
        size=11,
        color="#747B8D"
    ),

    showgrid=False,

    showline=True,
    linecolor="#C8CDD6",
    linewidth=1,

    ticks="outside",
    tickcolor="#C8CDD6",

    fixedrange=True
)


# ------------------------------------------------------
# Y AXIS
# ------------------------------------------------------

diversion_rate_fig.update_yaxes(
    title=dict(
        text="% Diversion from Landfill",
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#343743"
        ),
        standoff=10
    ),

    range=[0, 105],

    tickvals=[0, 20, 40, 60, 80, 100],
    ticksuffix="%",

    tickfont=dict(
        family="Inter, Segoe UI, Arial, sans-serif",
        size=12,
        color="#5E6878"
    ),

    showgrid=True,
    gridcolor="rgba(116,123,141,0.15)",
    gridwidth=1,

    showline=False,
    zeroline=False,

    fixedrange=True
)

# ------------------------------------------------------
# FINAL TITLE AND SPACING
# Keep this at the very end so later layout updates
# cannot overwrite the title.
# ------------------------------------------------------

diversion_rate_fig.update_layout(
    title=dict(
        text=(
            "<b>Construction Diversion Rate</b>"
            "<br>"
            "<span style='font-size:12px;color:#747B8D;'>"
            "Monthly diversion performance"
            "</span>"
        ),
        x=0,
        xanchor="left",
        y=0.94,
        yanchor="top",
        font=dict(
            family="Arial, sans-serif",
            size=19,
            color="#343743"
        )
    ),

    height=360,

    margin=dict(
        l=55,
        r=20,
        t=60,
        b=55
    )
)

# ------------------------------------------------------
# FINANCIAL IMPACT — TRUE VS. CONVENTIONAL HAULING
# ------------------------------------------------------

from pathlib import Path

import openpyxl
import plotly.graph_objects as go


def create_financial_comparison_fig():
    """
    Compare estimated construction hauling costs with and without
    Gateway's TRUE source-separation strategies.
    """

    project_root = Path(__file__).resolve().parent

    data_path = (
        project_root
        / "Data"
        / "Cost_Benefit_Analysis.xlsx"
    )

    if not data_path.exists():
        raise FileNotFoundError(
            f"Financial data workbook was not found at:\n{data_path}"
        )

    workbook = openpyxl.load_workbook(
        data_path,
        data_only=True,
        read_only=True
    )

    sheet_name = "Entire Project Overiew"

    if sheet_name not in workbook.sheetnames:
        workbook.close()
        raise KeyError(
            f"Could not find the sheet '{sheet_name}' "
            f"in {data_path.name}."
        )

    sheet = workbook[sheet_name]

    true_cost = sheet["D4"].value
    conventional_cost = sheet["D5"].value
    documented_savings = sheet["D6"].value

    workbook.close()

    values_to_check = {
        "TRUE cost": true_cost,
        "Conventional cost": conventional_cost,
        "Documented savings": documented_savings
    }

    for label, value in values_to_check.items():
        if not isinstance(value, (int, float)):
            raise ValueError(
                f"{label} is not a calculated number. "
                "Open the workbook in Excel, allow formulas to calculate, "
                "save it, and rerun the app."
            )

    savings_percent = (
        documented_savings / conventional_cost * 100
        if conventional_cost
        else 0
    )

    categories = [
        "With TRUE<br>strategies",
        "Without TRUE<br>strategies"
    ]

    costs = [
        true_cost,
        conventional_cost
    ]

    # Keep the axis close to the values so the height difference is obvious.
    y_axis_max = conventional_cost * 1.13

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=categories,
            y=costs,

            width=0.40,

            marker=dict(
                color=[
                    "#0B6E4F",
                    "#D8DCE5"
                ],
                line=dict(
                    width=0
                )
            ),

            text=[
                f"${true_cost / 1_000_000:.2f}M",
                f"${conventional_cost / 1_000_000:.2f}M"
            ],

            textposition="outside",

            textfont=dict(
                family="Arial, sans-serif",
                size=12,
                color="#343743"
            ),

            cliponaxis=False,

            customdata=[
                ["With TRUE strategies"],
                ["Without TRUE strategies"]
            ],

            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Estimated hauling cost: $%{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    # --------------------------------------------------
    # SAVINGS DIFFERENCE BRACKET
    # --------------------------------------------------

    # Place the bracket in the space between the two bars.
    bracket_x = 0.50

    fig.add_shape(
        type="line",
        xref="x",
        yref="y",

        x0=bracket_x,
        x1=bracket_x,

        y0=true_cost,
        y1=conventional_cost,

        line=dict(
            color="#747B8D",
            width=1.5
        )
    )

    # Bottom cap
    fig.add_shape(
        type="line",
        xref="x",
        yref="y",

        x0=bracket_x - 0.045,
        x1=bracket_x + 0.045,

        y0=true_cost,
        y1=true_cost,

        line=dict(
            color="#747B8D",
            width=1.5
        )
    )

    # Top cap
    fig.add_shape(
        type="line",
        xref="x",
        yref="y",

        x0=bracket_x - 0.045,
        x1=bracket_x + 0.045,

        y0=conventional_cost,
        y1=conventional_cost,

        line=dict(
            color="#747B8D",
            width=1.5
        )
    )

    # Place the savings annotation above the bracket,
    # rather than over either bar.
    fig.add_annotation(
        x=bracket_x,
        y=conventional_cost + conventional_cost * 0.035,

        xref="x",
        yref="y",

        text=(
            f"<b>${documented_savings / 1_000_000:.2f}M avoided</b>"
            f"<br>"
            f"<span style='font-size:11px;color:#747B8D;'>"
            f"{savings_percent:.0f}% lower cost"
            f"</span>"
        ),

        showarrow=False,

        xanchor="center",
        yanchor="bottom",

        align="center",

        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="#0B6E4F"
        )
    )

    # --------------------------------------------------
    # LAYOUT
    # --------------------------------------------------

    fig.update_layout(
        title=dict(
            text=(
                "<b>Hauling Cost Comparison</b>"
                "<br>"
                "<span style='font-size:12px;color:#747B8D;'>"
                "Estimated cost for documented project materials"
                "</span>"
            ),

            x=0,
            xanchor="left",

            y=0.92,
            yanchor="top",

            font=dict(
                family="Arial, sans-serif",
                size=19,
                color="#343743"
            )
        ),

        height=300,

        margin=dict(
            l=55,
            r=55,
            t=80,
            b=48
        ),

        bargap=0.35,

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Arial, sans-serif",
            color="#343743"
        ),

        showlegend=False,

        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#D8DCE5",

            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="#343743"
            )
        )
    )

    fig.update_xaxes(
        title=None,

        tickfont=dict(
            family="Arial, sans-serif",
            size=11,
            color="#5E6878"
        ),

        showgrid=False,
        showline=False,
        zeroline=False,

        ticks="",

        fixedrange=True
    )

    fig.update_yaxes(
        title=None,

        range=[
            0,
            y_axis_max
        ],

        tickvals=[
            0,
            2_000_000,
            4_000_000,
            6_000_000,
            8_000_000
        ],

        ticktext=[
            "$0",
            "$2M",
            "$4M",
            "$6M",
            "$8M"
        ],

        tickfont=dict(
            family="Arial, sans-serif",
            size=11,
            color="#747B8D"
        ),

        showgrid=True,
        gridcolor="rgba(116,123,141,0.13)",

        showline=False,
        zeroline=False,

        fixedrange=True
    )

    return fig


financial_comparison_fig = create_financial_comparison_fig()
