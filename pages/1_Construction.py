# pages/1_Construction.py

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
from graphs import diversion_rate_fig, construction_fig, financial_comparison_fig

FILE = "Data/Gateway_Graphs.xlsx"

plastic = pd.read_excel(FILE, sheet_name="Plastic Graph")
disposables = pd.read_excel(FILE, sheet_name="Disposables Graph")
construction = pd.read_excel(FILE, sheet_name="C&D Diversion Data")

from styles import apply_global_style


# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Building Gateway | Gateway Systems Dashboard",
    page_icon="🏗️",
    layout="wide"
)

apply_global_style()


# ======================================================
# PAGE-SPECIFIC COMPACT STYLING
# This keeps the Construction page readable without
# making every section feel oversized or overly long.
# ======================================================

st.markdown(
    """
    <style>

    /* Main page title */
    h1 {
        font-size: 2.25rem !important;
        margin-bottom: 0.35rem !important;
    }

    /* Major section headings */
    h2 {
        font-size: 1.55rem !important;
        margin-top: 1.15rem !important;
        margin-bottom: 0.35rem !important;
    }

    /* Card and subsection headings */
    h3 {
        font-size: 1.08rem !important;
        margin-top: 0.1rem !important;
        margin-bottom: 0.3rem !important;
    }

    /* Body text */
    p,
    li,
    div[data-testid="stMarkdownContainer"] p {
        font-size: 0.92rem !important;
        line-height: 1.4 !important;
    }

    /* Smaller captions */
    div[data-testid="stCaptionContainer"] p {
        font-size: 0.78rem !important;
    }

    /* More compact bordered cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0.72rem 0.82rem !important;
    }

    /* More compact metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.45rem !important;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.78rem !important;
    }

    /* Reduce excess space between blocks */
    div[data-testid="stVerticalBlock"] {
        gap: 0.65rem;
    }

    /* Slightly tighter expanders */
    details summary p {
        font-size: 0.9rem !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ======================================================
# FILE PATHS
# Put all photos, graphs, and diagrams in the project-level
# Figures folder.
# ======================================================

FIGURES_FOLDER = Path("Figures")


# ======================================================
# HELPER FUNCTIONS
# ======================================================

def show_media(
    filename,
    instructions,
    caption=None,
    title=None,
    bordered_placeholder=True
):
    """
    Display an image or graph if the file exists.

    Until the file is added, show a labeled placeholder with
    the exact filename to use.

    Set title=None when you do not want a visible heading above
    the image or placeholder.
    """

    file_path = FIGURES_FOLDER / filename

    if file_path.exists():
        st.image(
            str(file_path),
            caption=caption,
            use_container_width=True
        )

    else:
        placeholder = st.container(border=bordered_placeholder)

        with placeholder:
            if title:
                st.subheader(title)

            st.info(
                f"**Visual placeholder**\n\n"
                f"{instructions}\n\n"
                f"Save the finished file as:\n\n"
                f"`Figures/{filename}`"
            )


def bullet_card(title, bullets, metric=None, metric_label=None):
    """
    Create a compact bordered card using short, scannable facts.
    """

    with st.container(border=True):
        st.subheader(title)

        if metric:
            st.metric(
                label=metric_label or "",
                value=metric
            )

        for bullet in bullets:
            st.markdown(f"- {bullet}")


def compact_metric(value, label, note=None):
    """
    Create a headline metric with an optional short note.
    """

    st.metric(
        label=label,
        value=value
    )

    if note:
        st.caption(note)


# ======================================================
# PAGE INTRODUCTION
# ======================================================

import base64
from pathlib import Path
import streamlit as st


def get_base64_image(image_path):
    image_bytes = Path(image_path).read_bytes()
    return base64.b64encode(image_bytes).decode()


hero_image = get_base64_image(
    "images/gateway_construction_hero.jpg"
)

st.markdown(
    f"""
    <style>
    .construction-hero {{
        position: relative;
        width: 100%;
        min-height: 400px;
        border-radius: 22px;
        overflow: hidden;
        margin-bottom: 0.05rem;

        background-image:
            linear-gradient(
                90deg,
                rgba(5, 18, 14, 0.88) 0%,
                rgba(5, 18, 14, 0.62) 38%,
                rgba(5, 18, 14, 0.15) 72%,
                rgba(5, 18, 14, 0.05) 100%
            ),
            url("data:image/jpeg;base64,{hero_image}");

        background-size: cover;
        background-position: center;
        display: flex;
        align-items: flex-end;
    }}

    .construction-hero-content {{
        max-width: 750px;
        padding: 3rem;
        color: white;
    }}

    .construction-hero h1 {{
        margin: 0;
        color: white;
        font-size: clamp(2.7rem, 6vw, 5rem);
        line-height: 0.95;
        font-weight: 750;
        letter-spacing: -0.04em;
    }}

    .construction-hero-line {{
        width: 210px;
        height: 3px;
        margin: 1.3rem 0;
        background: #3F8F43;
        border-radius: 999px;
    }}

    .construction-hero p {{
        margin: 0;
        max-width: 560px;
        color: rgba(255, 255, 255, 0.92);
        font-size: 1.1rem;
        line-height: 1.55;
    }}

    @media (max-width: 700px) {{
        .construction-hero {{
            min-height: 330px;
            background-position: 60% center;
        }}

        .construction-hero-content {{
            padding: 2rem;
        }}

        .construction-hero h1 {{
            font-size: 2.8rem;
        }}

        .construction-hero p {{
            font-size: 1rem;
        }}
    }}
    </style>

    <div class="construction-hero">
        <div class="construction-hero-content">
            <h1>Construction<br>Systems</h1>
            <div class="construction-hero-line"></div>
            <p>
                Designing out waste, building in circularity, and delivering
                measurable impact from the ground up.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ======================================================
# CONSTRUCTION AT A GLANCE
# Prioritize outcomes that are understandable immediately.
# Replace the financial placeholder when the final savings
# analysis is complete.
# ======================================================

st.header("Construction at a Glance")

metric_1, metric_2, metric_3, metric_4 = st.columns(4)

with metric_1:
    compact_metric(
        value="92.1%",
        label="Diversion Rate",
        note="Average of entire project"
    )

with metric_2:
    compact_metric(
        value="7,945+",
        label="Tons Recovered",
        note="Earthwork excluded"
    )

with metric_3:
    compact_metric(
        value="$1.85 Million",
        label="Financial Savings",
        note="From pursuing TRUE"
    )

with metric_4:
    compact_metric(
        value="TRUE Platinum",
        label="Construction Status",
        note="Precertified; full certification pursued"
    )


# ======================================================
# MATERIAL RECOVERY AND VALUE
# This is the main section because it is the clearest and
# most relatable part of the zero-waste story.
# ======================================================

st.header("Material Recovery and Value")

st.write(
    "Documented project data demonstrates the environmental and financial impacts "
    "of Gateway's construction waste-management strategy."
)


# ------------------------------------------------------
# ROW 1 — HERO PERFORMANCE + TRUE CARD
# ------------------------------------------------------

hero_graph, true_panel = st.columns(
    [2, 1],
    gap="large"
)

with hero_graph:
    st.plotly_chart(
        diversion_rate_fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True
        }
    )

with true_panel:
    bullet_card(
        title="TRUE Zero Waste for Construction",
        bullets=[
            "Requires at least 90% diversion from landfill, along with more than 80 additional certification requirements.",
            "Gateway pursued full TRUE certification through Turner Construction's first TRUE project.",
            (
                "Turner led implementation and documentation"
                " in partnership with UC Berkeley's Cal Zero Waste and project partners."
            )
        ]
    )

# Force the next row below the entire first row
st.markdown(
    "<div style='clear: both; height: 24px;'></div>",
    unsafe_allow_html=True
)

# ------------------------------------------------------
# ROW 2 — MATERIALS + FINANCIAL VISUALS
# ------------------------------------------------------

materials_col, finance_col = st.columns(
    2,
    gap="large"
)

with materials_col:
    st.plotly_chart(
        construction_fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
            "scrollZoom": False
        }
    )

    bullet_card(
        title="Source Separation",
        bullets=[
            "Major construction materials were collected in dedicated source-separated containers rather than commingled C&D debris.",
            "GroundForce coordinated hauling logistics to maximize material recovery and consistant source separation."
        ]
    )


with finance_col:
    st.plotly_chart(
        financial_comparison_fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
            "scrollZoom": False,
        },
    )

    # Keep your existing Financial Impact card directly below this.

    bullet_card(
        title="Financial Methodology",
        bullets=[
            "Estimated using 1,207 documented hauling records, project material quantities, and contractor pricing.",
            "Compared against a conventional mixed C&D disposal scenario to quantify avoided hauling costs and recovered material value."
          
        ]
    )
# ------------------------------------------------------
# DETAILED MATERIAL DATA
# A useful secondary detail, appropriately placed in one
# expander rather than shown by default.
# ------------------------------------------------------

with st.expander("View detailed construction material data"):

    stream_1, stream_2, stream_3 = st.columns(3)

    with stream_1:
        with st.container(border=True):
            st.markdown(
                """
                ### Highest-Volume Materials

                - **Concrete:** 4,903.85 tons
                - **Clean drywall:** 939.57 tons
                - **Clean wood:** 751.47 tons
                - **Asphalt:** 380.42 tons
                """
            )

    with stream_2:
        with st.container(border=True):
            st.markdown(
                """
                ### Additional Recovery

                - **Alternative daily cover:** 354.43 tons
                - **Mixed recyclables:** 302.32 tons
                - **Metal:** 244.37 tons
                - **Miscellaneous debris:** 24.34 tons
                """
            )

    with stream_3:
        with st.container(border=True):
            st.markdown(
                """
                ### Smaller Streams

                - **Painted drywall:** 20.45 tons
                - **Cardboard and paper:** 10.01 tons
                - **Sorted trash recovery:** 9.10 tons
                - **Plastics and packaging:** 3.62 tons
                - **Compost:** 0.75 tons
                """
            )

    left, center, right = st.columns([0.15, 0.3, 0.15])

with center:
    show_media(
        filename="construction_source_separation.jpg",
        title="Construction Source Separation",
        instructions=(
            "Add a photograph of labeled dumpsters, separated material piles, "
            "jobsite recovery containers, or waste signage."
        )
    )


# ======================================================
# REUSABLE CONSTRUCTION SYSTEMS
# Focus on the image and measurable impacts.
# ======================================================

st.header("Reusable Construction Systems")

st.write(
    "Multiple trades replaced disposable shipping materials with reusable "
    "transportation and installation systems."
)

curtainwall_photo, curtainwall_metrics = st.columns([1.35, 1])

with curtainwall_photo:
    show_media(
        filename="permasteelisa_curtainwall_bunks.JPEG",
        title=None,
        instructions=(
            "Add a large photograph of Permasteelisa's reusable hybrid "
            "curtainwall bunks at Gateway."
        )
    )

with curtainwall_metrics:
    with st.container(border=True):
        st.subheader("Permasteelisa Curtainwall Bunks")

        impact_1, impact_2 = st.columns(2)

        with impact_1:
            st.metric(
                label="Timber Saved",
                value="110–120"
            )
            st.caption("metric tons")

        with impact_2:
            st.metric(
                label="Landfill Waste Avoided",
                value="60–70"
            )
            st.caption("metric tons")

        st.metric(
            label="Curtainwall Units Using Reusable Bunks",
            value="≈98%"
        )

        st.markdown(
            "- Supported transportation and installation\n"
            "- Replaced disposable wooden crates and pallets"
        )


with st.expander("View additional reusable shipping systems"):

    shipping_1, shipping_2 = st.columns(2)

    with shipping_1:
        bullet_card(
            title="ACCO Ductwork Bunkers",
            bullets=[
                "Reusable transportation system",
                "Protected ductwork during handling"
            ]
        )

    with shipping_2:
        bullet_card(
            title="Cupertino Electrical Containers",
            bullets=[
                "Reusable containers for electrical components",
                "Extended reusable logistics across trades"
            ]
        )

    left, center, right = st.columns([0.15, 0.3, 0.15])

with center:
    show_media(
        filename="reusable_shipping_systems.JPEG",
        title="Reusable Shipping Systems",
        instructions=...
    )


# ======================================================
# CIRCULAR CONSTRUCTION
# Keep visible because these stories are memorable and
# highly relatable to building occupants.
# ======================================================

st.header("Circular Construction")

st.write(
    "Construction practices transformed biological materials and food scraps into lasting resources for the Gateway project and UC Berkeley."
)

circular_text, circular_photo = st.columns([1, 1.2])

with circular_text:
    # Two cards instead of three
    circular_1, circular_2 = st.columns(2)

    with circular_1:
        bullet_card(
            title="Vermicomposting",
            bullets=[
                "Food scraps generated during construction were diverted to UC Berkeley's vermicomposting program.",
                "Worms converted the material into nutrient-rich compost, supporting campus research.",
              
            ]
        )

    with circular_2:
        bullet_card(
            title="From Tree to Table",
            bullets=[
                "Gateway's original site tree was given a second life instead of becoming construction waste.",
                "Recovered wood was crafted into custom tables by Bay Area Redwood, giving the tree a home in the completed building.",
                
            ]
        )

with circular_photo:
    show_media(
        filename="salvaged_tree_furniture.png",
        title=None,
        instructions=(
            "Add a photograph of the finished furniture made from the salvaged tree. "
            "A before-and-after comparison would also work well."
        )
    )


# ======================================================
# INNOVATIVE CONSTRUCTION
# Combine electric equipment, energy, and water under one
# occupant-friendly innovation section.
# ======================================================

st.header("Innovative Construction")

st.write(
    "Gateway tested new equipment and used live resource monitoring to improve "
    "jobsite performance."
)


# ------------------------------------------------------
# BOBCAT ELECTRIC SKID STEER
# ------------------------------------------------------

bobcat_photo, bobcat_text = st.columns([1.15, 1])

with bobcat_photo:
    show_media(
        filename="bobcat_t7x_gateway.jpg",
        title=None,
        instructions=(
            "Add a photograph of the Bobcat T7X operating at the Gateway construction site."
        )
    )

with bobcat_text:
    with st.container(border=True):
        st.subheader("Bobcat T7X All-Electric Loader")

        st.metric(
            label="Battery Remaining After Longest Recorded Shift",
            value="30%"
        )

        st.markdown(
            "- First U.S. construction-project pilot of the all-electric skid steer\n"
            "- Approximately 6 consecutive hours of operation\n"
            "- Operational feedback shared with Bobcat and Sunbelt Rentals"
        )


# ------------------------------------------------------
# WATER MONITORING
# Keep visible because the leak story is concrete and easy
# to understand.
# ------------------------------------------------------

water_text, water_photo = st.columns([1, 1.15])

with water_text:
    with st.container(border=True):
        st.subheader("Water Monitoring")

        st.metric(
            label="Estimated Leak Identified",
            value="≈30,000 gal/month"
        )

        st.markdown(
            "- Multiple construction water sources were metered\n"
            "- Consumption was reviewed regularly\n"
            "- Restroom leak identified through monitoring\n"
            "- Leak repaired within one week"
        )

with water_photo:
    show_media(
        filename="construction_water_monitoring.jpg",
        title=None,
        instructions=(
            "Add a photograph of a water meter, temporary water system, restroom "
            "facilities, or an available consumption graph."
        )
    )


# ------------------------------------------------------
# ADDITIONAL ENERGY STRATEGIES
# This is one of the few appropriate uses of an expander
# because these are supporting details within one category.
# ------------------------------------------------------

with st.expander("View additional jobsite energy strategies"):

    energy_1, energy_2, energy_3 = st.columns(3)

    with energy_1:
        bullet_card(
            title="Renewable Diesel",
            bullets=[
                "Used in jobsite equipment except generators",
                "Supported California off-road equipment requirements"
            ]
        )

    with energy_2:
        bullet_card(
            title="Temporary Power",
            bullets=[
                "Used for most welding",
                "Reduced reliance on diesel welding generators"
            ]
        )

    with energy_3:
        bullet_card(
            title="Live Energy Metering",
            bullets=[
                "Approximately 15 systems monitored",
                "Included main gear, welding skids, restrooms, and site trailers",
                "Trends reviewed monthly"
            ]
        )




# ======================================================
# LOWER-CARBON MATERIALS
# Keep all engineering achievements visible, but present
# them after the more relatable zero-waste content.
# ======================================================

st.header("Lower-Carbon Materials")

st.write(
    "Embodied-carbon modeling and product selection were used to reduce impacts "
    "from major building materials and assemblies."
)


# ------------------------------------------------------
# FOUR COMPACT ENGINEERING HIGHLIGHTS
# ------------------------------------------------------

def engineering_highlight_card(
    title,
    bullets,
    metric=None,
    metric_label=None,
    height=260
):
    """
    Create a fixed-height engineering highlight card.
    """

    with st.container(
        border=True,
        height=height
    ):
        st.subheader(title)

        if metric:
            st.metric(
                label=metric_label or "",
                value=metric
            )

        for bullet in bullets:
            st.markdown(f"- {bullet}")

carbon_1, carbon_2, carbon_3, carbon_4 = st.columns(4)

with carbon_1:
    engineering_highlight_card(
        title="Curtainwall EPD",
        metric="15%",
        metric_label="Lower Embodied Carbon",
        bullets=[
            "First U.S. facility-specific curtainwall EPD",
            "Produced by Permasteelisa North America"
        ]
    )

with carbon_2:
    engineering_highlight_card(
        title="EcoSmart Drywall",
        metric="≈20%",
        metric_label="Lower Embodied Carbon",
        bullets=[
            "5/8-inch Firecode X product",
            "Compared with standard Type X drywall"
            
        ]
    )

with carbon_3:
    engineering_highlight_card(
        title="Lower-Carbon Concrete",
        metric="38%",
        metric_label="Lower Embodied Carbon",
        bullets=[
            "Level 3 and above",
            "30% slag replacement"
        ]
    )

with carbon_4:
    engineering_highlight_card(
        title="EC3 Pilot",
        metric="52.31",
        metric_label="kgCO₂e/SF",
        bullets=[
            "Schematic design estimate",
            "As-built estimate underway"
        ]
    )


# ------------------------------------------------------
# CARBON GRAPH AND EAF STEEL
# ------------------------------------------------------

carbon_graph, steel_card = st.columns([1.35, 1])

with carbon_graph:

    materials = [
        "Curtainwall",
        "EcoSmart<br>Drywall",
        "Lower-Carbon<br>Concrete"
    ]

    remaining = [85, 80, 62]
    reduction = [15, 20, 38]

    carbon_fig = go.Figure()

    # Remaining embodied carbon
    carbon_fig.add_trace(
        go.Bar(
            x=materials,
            y=remaining,
            name="Remaining embodied carbon",

            marker=dict(
                color="#0B6E4F"
            ),

            hovertemplate=(
                "<b>%{x}</b><br>"
                "%{y}% of baseline embodied carbon remains"
                "<extra></extra>"
            )
        )
    )

    # Avoided embodied carbon
    carbon_fig.add_trace(
        go.Bar(
            x=materials,
            y=reduction,
            name="Embodied-carbon reduction",

            marker=dict(
                color="#D8DCE5"
            ),

            text=["15% lower", "≈20% lower", "38% lower"],
            textposition="inside",

            textfont=dict(
                family="Arial, sans-serif",
                size=11,
                color="#343743"
            ),

            hovertemplate=(
                "<b>%{x}</b><br>"
                "%{y}% embodied-carbon reduction"
                "<extra></extra>"
            )
        )
    )

    carbon_fig.update_layout(
        barmode="stack",

        title=dict(
            text=(
                "<b>Selected Embodied-Carbon Reductions</b>"
                "<br>"
                "<span style='font-size:12px;color:#747B8D;'>"
                "Performance relative to conventional material baselines"
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

        height=230,

        margin=dict(
            l=45,
            r=20,
            t=78,
            b=42
        ),

        bargap=0.42,

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

    carbon_fig.update_yaxes(
        title=None,

        range=[0, 100],

        tickvals=[0, 25, 50, 75, 100],
        ticksuffix="%",

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

    carbon_fig.update_xaxes(
        title=None,

        tickfont=dict(
            family="Arial, sans-serif",
            size=11,
            color="#5E6878"
        ),

        showgrid=False,
        showline=False,
        ticks="",

        fixedrange=True
    )

    st.plotly_chart(
        carbon_fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True
        }
    )



with steel_card:
    bullet_card(
        title="Electric Arc Furnace Steel",
        bullets=[
            "Most standard steel sections sourced from North American EAF plants",
            "Recycled steel used as feedstock",
            "Included wide flange, hollow tube, and plate sections"
        ]
    )


# ------------------------------------------------------
# PROJECT RESOURCES
# ------------------------------------------------------

# ------------------------------------------------------
# PROJECT RESOURCES
# ------------------------------------------------------

st.header("Project Resources")

st.write(
    "Explore Gateway's official certifications and learn more about the "
    "strategies, systems, and outcomes that supported the project."
)

# ----------------------------------------
# CERTIFICATIONS
# ----------------------------------------

true_col, leed_col = st.columns(2, gap="large")

with true_col:
    with st.container(border=True):
        st.subheader("TRUE Zero Waste Certification")

        st.write(
            "Official TRUE Zero Waste certification awarded by the "
            "U.S. Green Building Council (USGBC)."
        )

        st.button(
            "View Certificate",
            key="true_certificate_button",
            use_container_width=True,
            disabled=True
        )

with leed_col:
    with st.container(border=True):
        st.subheader("LEED Certification")

        st.write(
            "Official LEED certification recognizing Gateway's "
            "sustainable building design and performance."
        )

        st.button(
            "View Certificate",
            key="leed_certificate_button",
            use_container_width=True,
            disabled=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------
# CASE STUDY
# ----------------------------------------

with st.container(border=True):
    st.subheader("Gateway Zero Waste Case Study")

    st.write(
        "An in-depth overview of Gateway's zero waste construction and "
        "operations strategies, implementation process, measurable outcomes, "
        "and lessons learned."
    )

    st.button(
        "Read Case Study",
        key="gateway_case_study_button",
        use_container_width=True,
        disabled=True
    )

# ======================================================
# CLOSING NOTE
# ======================================================

st.divider()

st.caption(
    "Construction figures and descriptions reflect available Gateway project "
    "documentation. Update financial, as-built, and certification information "
    "as final values become available."
)
